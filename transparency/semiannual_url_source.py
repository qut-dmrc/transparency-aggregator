""" 
Generate twice yearly source data pointing to readable files/urls from the config
"""

from transparency.source import Source
from string import Template


class SemiannualUrlSource(Source):
    def get(self):

        url_template = Template(self.config['url_template'])
        start_year = int(self.config['start_year'])
        end_year = int(self.config['end_year'])

        data = []

        for report_year in range(start_year, end_year + 1):

            for i, substitutes in enumerate([
                {
                    'facebook_period': "H1",
                    'start_month': "jan",
                    'end_month': "jun",
                    'end_day_month': "06-30",
                },
                {
                    'facebook_period': "H2",
                    'start_month': "jul",
                    'end_month': "dec",
                    'end_day_month': "12-31",
                },
            ]):
                date_end = f"{report_year}-{substitutes['end_day_month']}"
                substitutes = {**substitutes, 'report_year': report_year, 'date_end': date_end}
                url = url_template.substitute(substitutes)
                if i == 0:
                    report_start = "{}-01-01 00:00:00".format(report_year)
                    report_end = "{}-06-30 23:59:59".format(report_year)
                else:
                    report_start = "{}-07-01 00:00:00".format(report_year)
                    report_end = "{}-12-31 23:59:59".format(report_year)

                period_data = {'url': url, 'report_start': report_start, 'report_end': report_end}

                data.append(period_data)

        return data
