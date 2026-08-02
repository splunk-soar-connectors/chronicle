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
import re
import unittest

from chronicle_consts import GC_RULE_ID_PATTERN


class ChronicleRuleIdPatternTest(unittest.TestCase):
    def test_accepts_documented_identifiers(self):
        for rule_id in (
            "ru_12345678-1234-1234-1234-123456789abc",
            "ru_12345678-1234-1234-1234-123456789abc@-",
            "ru_12345678-1234-1234-1234-123456789abc@v_1_2",
        ):
            with self.subTest(rule_id=rule_id):
                self.assertIsNotNone(re.fullmatch(GC_RULE_ID_PATTERN, rule_id))

    def test_rejects_path_segments(self):
        for rule_id in (
            ".",
            "..",
            "../rules",
            "ru_12345678-1234-1234-1234-123456789abc/../other",
            "ru_12345678-1234-1234-1234-123456789abc%2f..",
        ):
            with self.subTest(rule_id=rule_id):
                self.assertIsNone(re.fullmatch(GC_RULE_ID_PATTERN, rule_id))
