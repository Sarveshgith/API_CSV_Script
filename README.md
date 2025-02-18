### Ticket Data Extraction Script

## Overview
This script allows you to extract ticket data from a specified URL and save it to a CSV file. It supports retrieving tickets by event or user and offers integration with various authentication methods.

## Installation

1. **Clone the repository or download the script**.
2. **Install the required libraries** by running the following command:

   ```bash
   pip install requests google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

   - `requests`: For making HTTP requests to the specified URL.
   - `google-auth`, `google-auth-oauthlib`, `google-auth-httplib2`: For handling Google authentication.
   - `google-api-python-client`: For interacting with Google APIs.
   - `csv`: For writing the extracted data to a CSV file.

---
