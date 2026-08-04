**Unreleased**

* Resolved app issues related to Python 3.13 upgrade
* Escaped values embedded in widget JavaScript context (PSAAS-30709)
* Validated and encoded Rule IDs before using them in Chronicle API paths (PSAAS-31072)
* Bounded pagination and stopped when upstream cursors do not advance (PSAAS-32036, PSAAS-32084)
* Returned an action error when the rules pagination safety cap is exhausted (PSAAS-32036)
* Reused only ingestion containers recorded in the current asset's state (PSAAS-32005)
* Preserved poll checkpoints and deduplication state when result ingestion fails (PSAAS-32349)
* Used the User Alerts checkpoint window when fetching User Alerts (PSAAS-32349)
