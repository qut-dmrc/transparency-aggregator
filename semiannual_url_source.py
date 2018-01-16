""" 
Generate twice yearly source data pointing to readable files/urls from the config
"""

from source import Source
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
                },
                {
                    'facebook_period': "H2",
                    'start_month': "jul",
                    'end_month': "dec",
                },
            ]):
                substitutes = {**substitutes, 'report_year': report_year}
                url = url_template.substitute(substitutes)
                if i == 0:
                    start_date = "{}-01-01 00:00:00".format(report_year)
                    end_date = "{}-06-30 23:59:59".format(report_year)
                else:
                    start_date = "{}-07-01 00:00:00".format(report_year)
                    end_date = "{}-12-31 23:59:59".format(report_year)

                period_data = {'url': url, 'report_start': start_date, 'report_end': end_date}

                data.append(period_data)

        return data
