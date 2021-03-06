""" This class develops generic methods to create the list of dicts of transparency data
	and upload them to Google BigQuery.
	
	Most of these methods will need to be overwritten to handle specific reporting formats.
	 
"""
import pandas as pd
from transparency import utils
from transparency.utils import str_to_date



class DataFrameBuilder:
    def __init__(self, df_in, platform, platform_property, report_start, report_end):
        self.df_in = df_in
        self.df_out = pd.DataFrame()
        self.fixed_columns = {
            'platform': platform,
            'property': platform_property,
            'report_start': str_to_date(report_start, "%Y-%m-%d %H:%M:%S"),
            'report_end': str_to_date(report_end, "%Y-%m-%d %H:%M:%S"),
        }

        self.fixed_columns = {k: v for k, v in self.fixed_columns.items() if v}

    def get_df(self):
        return self.df_out

    def extract_columns(
            self,
            request_type,
            request_subtype,
            num_requests_col,
            num_accounts_specified_col='',
            num_requests_complied_col='',
            num_accounts_complied_col='',
            num_accounts_suspended_col='',
            num_content_removed_col='',
            num_content_specified_col='',
            jurisdiction_col='country'
    ):
        """ Take a dataframe with the columns num_requests_col and num_requests_complied_col
            and return a new dataframe in our standard form.
        """

        output_cols = [
            "num_requests",
            "num_requests_complied",
        ]

        if num_accounts_specified_col:
            output_cols.append('num_accounts_specified')
        if num_content_specified_col:
            output_cols.append('num_content_specified')
        if num_accounts_complied_col:
            output_cols.append('num_accounts_complied')
        if num_accounts_suspended_col:
            output_cols.append('num_accounts_enforced')
        if num_content_removed_col:
            output_cols.append('num_content_enforced')

        col_map = {
            num_requests_col: 'num_requests',
            num_accounts_specified_col: 'num_accounts_specified',
            num_content_specified_col: 'num_content_specified',
            num_requests_complied_col: 'num_requests_complied',
            num_accounts_complied_col: 'num_accounts_complied',
            num_content_removed_col: 'num_content_enforced',
            num_accounts_suspended_col: 'num_accounts_enforced',
            jurisdiction_col: 'country',
        }

        #remove empty string key, empty string indicates column not present
        col_map.pop('', None)

        df = self.df_in.copy()
        # These are static: fill each row of the DF with these values
        for key, value in self.fixed_columns.items():
            df[key] = value

        if callable(request_type):
            df['request_type'] = df.apply(request_type, axis=1)
        else:
            df['request_type'] = request_type

        if callable(request_subtype):
            df['request_subtype'] = df.apply(request_subtype, axis=1)
        else:
            df['request_subtype'] = request_subtype

        # TODO: limit extra columns
        df.rename(columns=col_map, inplace=True)

        utils.df_convert_to_lower(df, ["request_type", "request_subtype"])

        utils.df_create_missing_columns(df, output_cols)
        utils.df_convert_to_int(df, output_cols)

        self.df_out = self.df_out.append(df)

        return True
