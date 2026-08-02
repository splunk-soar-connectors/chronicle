# Copyright (c) 2026 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import importlib
import sys
import types
import unittest
from unittest.mock import MagicMock, patch


def _load_connector_module():
    phantom_package = types.ModuleType("phantom")
    phantom_package.__path__ = []

    phantom_app = types.ModuleType("phantom.app")
    phantom_app.APP_SUCCESS = 0
    phantom_app.APP_ERROR = -1
    phantom_app.is_fail = lambda status: status != 0
    phantom_package.app = phantom_app

    action_result_module = types.ModuleType("phantom.action_result")
    action_result_module.ActionResult = object
    base_connector_module = types.ModuleType("phantom.base_connector")
    base_connector_module.BaseConnector = object

    bs4_module = types.ModuleType("bs4")
    bs4_module.BeautifulSoup = object

    stub_modules = {
        "phantom": phantom_package,
        "phantom.app": phantom_app,
        "phantom.action_result": action_result_module,
        "phantom.base_connector": base_connector_module,
        "bs4": bs4_module,
    }
    with patch.dict(sys.modules, stub_modules):
        sys.modules.pop("chronicle_connector", None)
        return importlib.import_module("chronicle_connector")


class ChroniclePaginationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connector_module = _load_connector_module()

    def test_v2_page_cap_returns_action_error(self):
        connector = self.connector_module.ChronicleConnector.__new__(self.connector_module.ChronicleConnector)
        connector.get_action_identifier = MagicMock(return_value="on_poll")
        connector.debug_print = MagicMock()

        request_count = 0

        def make_rest_call(_action_result, _client, _endpoint):
            nonlocal request_count
            request_count += 1
            return self.connector_module.phantom.APP_SUCCESS, {"rules": [], "nextPageToken": f"token-{request_count}"}

        connector._make_rest_call = make_rest_call
        action_result = MagicMock()
        action_result.set_status.return_value = self.connector_module.phantom.APP_ERROR

        status, results = connector._paginator_for_v2_apis(
            action_result,
            client=object(),
            endpoint="/rules?pageSize=1000",
            data_subject="rules",
            limit=1,
        )

        self.assertEqual(status, self.connector_module.phantom.APP_ERROR)
        self.assertEqual(results, [])
        action_result.set_status.assert_called_once_with(
            self.connector_module.phantom.APP_ERROR,
            "Stopped pagination after the maximum of 11 pages",
        )
