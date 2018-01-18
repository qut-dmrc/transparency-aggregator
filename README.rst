# Transparency Report Aggregator

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

>'report_start', 'report_end', 'platform', 'property', 'country', 'request_type', 'agency', 'reason', 'num_requests', 'num_complied', 'num_affected'

Initially, the two main types of requests are private information requests and content removal requests.

This script will eventually download as many transparency reports as possible.

## Usage

      transparency_aggregator.py [-vl] --all --output=FILE
      transparency_aggregator.py --version

    Options:
      -h --help     Show this screen.
      -v --verbose  Increase verbosity for debugging.
      -l --nolog    Don't save log to file -- for debugging only.
      -o FILE, --output=FILE     Save results to FILE in CSV format.
      --version  Show version.
      --all     Fetch all available transparency reports


## Troubleshooting

are you getting:
    ssl.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:777)

On MacOS, you want to navigate to "Applications/Python 3.6" and run the "Install Certificates.command" file.

