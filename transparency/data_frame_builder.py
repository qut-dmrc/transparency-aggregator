""" This class develops generic methods to create the list of dicts of transparency data
	and upload them to Google BigQuery.
	
	Most of these methods will need to be overwritten to handle specific reporting formats.
	 
"""
from transparency.utils import str_to_date


class DataFrameBuilder:
    def __init__(self, df_in, df_out, platform, platform_property, report_start, report_end):
        self.df_in = df_in
        self.df_out = df_out
        self.fixed_columns = {
            'platform': platform,
            'property': platform_property,
            'report_start': str_to_date(report_start, "%Y-%m-%d %H:%M:%S"),
            'report_end': str_to_date(report_end, "%Y-%m-%d %H:%M:%S"),
        }

        self.fixed_columns = {k: v for k, v in self.fixed_columns.items() if v}

    def get_df(self):
        return self.df_out

    def extract_columns(self, request_type, request_subtype, num_requests_col,
                        num_accounts_specified_col, num_complied_col, jurisdiction_col='country'):
        """ Take a dataframe with the columns num_requests_col and num_complied_col
            and return a new dataframe in our normal form format.
        """

        df_out = self.df_in[[jurisdiction_col, num_requests_col, num_complied_col, num_accounts_specified_col]].copy()

        # These are static: fill each row of the DF with these values
        for key, value in self.fixed_columns.items():
            df_out[key] = value

        df_out['request_type'] = request_type
        df_out['request_subtype'] = request_subtype

        col_map = {num_complied_col: 'num_complied',
                   num_requests_col: 'num_requests',
                   num_accounts_specified_col: 'num_accounts_specified_col',
                   jurisdiction_col: 'country',
                   }

        df_out.rename(columns=col_map, inplace=True)

        self.df_out = self.df_out.append(df_out)

        return True
