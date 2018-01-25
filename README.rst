==============================
Transparency Report Aggregator
==============================
Overview
--------
Our research tracks the impact of telecommunications firms on human rights. We need to be able to track how different
governments around the world apply pressure on tech companies and telecommunication providers to hand over identifying
user information or block content.

Major technology companies and telecommunications providers release 'transparency reports' on an annual, bi-annual,
quarterly, or monthly basis. These transparency reports contain aggregate information about how many requests have
been made to block data or hand over user information, and the proportion of those requests that have been complied
with.

The reports are released in many different formats, including HTML, PDF, and CSV. There is no uniform way to compare
across platforms -- or even necessarily on the same platform over time.

There are currently 68 companies releasing this data. A reasonably complete list of reports is maintained by Access Now at: https://www.accessnow.org/transparency-reporting-index/

This script is designed to scrape tables from CSV, PDF, or HTML reports and aggregate data from different companies into
a single common format. The output format contains the following fields:

  'report_start', 'report_end', 'platform', 'property', 'country', 'request_type', 'request_subtype', 'num_requests', 'num_accounts_specified', 'num_requests_complied', 'num_accounts_complied', 'agency', 'reason'

Initially, the two main types of requests are private information requests and content removal requests.

This script will eventually download as many transparency reports as possible.

Usage
-----
| main.py [-vl] --csv-output=FILE (--get=SOURCE | --get-all)
| main.py --version
| main.py --help

-h, --help                  Show this screen.
-v, --verbose               Increase verbosity for debugging.
-l, --nolog                 Don't save log to file -- for debugging only.
-c FILE, --csv-output=FILE  Save results to FILE in CSV format.
--version                   Show version.
-a, --get-all               Fetch all available transparency reports
-s, --get=SOURCE            Fetch data from SOURCE (e.g. facebook)

Cache
-----

We recommend clearing the cache before generating a report, except while
developing new code.

You can clear the cache with:
    ``make clear_cache``

Downloaded data is cached in the ./cache/ directory. Results with error codes
(e.g. 404) are not cached.  The cache needs to be cleared before changes to
sites are detected.  For sites that publish each report at a different URL,
this works fine.  For sites where everything is at one URL (e.g. Linkedin), or
where the data on a page changes (e.g. the most recent snapchat URL), these
changes will be missed.


Troubleshooting
---------------
are you getting:
    ``ssl.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:777)``

On MacOS, you want to navigate to "Applications/Python 3.6" and run the "Install Certificates.command" file.

Testing
-------
You can run the unit tests with:
    ``make test``

You can run the system tests with:
    ``make system_test``

The system tests use the program to download and process all data (using the cached data if available) and then checks a small
subset of the results agree with data copied off the website by hand.

You can use use the ``SYSTEM_TEST_USE_OLD_OUTPUT`` environment variable to skip creating an output file
This is useful when writing new system tests.

``SYSTEM_TEST_USE_OLD_OUTPUT=1 make system_test``

