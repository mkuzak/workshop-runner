# WORKSHOP RUNNER

The goal of this tool is to facilitate setting up the workshop in which students are using remote vm's.
It should be easy to collect all ip addresses of running machines and collect public keys from students to allow password-less login.

Current implementation uses:
- google spreadsheet to collect ip addresses and public keys
- [gspread](https://gspread.readthedocs.org) to talk to spreadsheet with Python script
	- this requires authentication with OAuth2, the details can be read [here](https://gspread.readthedocs.org/en/latest/oauth2.html)
	
Unfortunately the solution suffers from race conditions when multiple vms want to edit spreadsheet at the same time.
More reliable and robust solution, instead of spreadsheet `hack` is needed.
