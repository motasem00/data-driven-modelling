

    # # Convert 6-digit NAICS codes to 4-digit
    # expanded_rows = pattern_data[pattern_data['naics'].str.endswith('//') & (pattern_data['naics'].str.count('/') == 2)].copy()
    # expanded_rows.loc[:, 'naics'] = pattern_data['naics'].str.replace('/', '', regex=False)

    # # Create a dictionary for the old NAICS codes and their descriptions
    # naics_description_dict = expanded_rows.set_index('naics')['DESCRIPTION'].to_dict()

    # for new_naics, old_naics_list in naics_expanding.items():
    #     # Assign the new `naics` code
    #     expanded_rows.loc[expanded_rows['naics'].isin(old_naics_list), 'naics'] = new_naics
            
    #     # Create a description for all old codes in the format "code (description)"
    #     old_descriptions = [
    #         f"{code} ({naics_description_dict[code]})"
    #         for code in old_naics_list
    #         if code in naics_description_dict
    #     ]
            

    #     # Create the description as a concatenated string
    #     description = ', '.join(old_descriptions)
            
    #     # Set the description for all rows with the new `naics` code
    #     expanded_rows.loc[expanded_rows['naics'] == new_naics, 'DESCRIPTION'] = description

    #     # Reset index and save the processed DataFrame
    #     expanded_rows.reset_index(drop=True, inplace=True)
    #     expanded_rows.to_pickle('/content/data-driven-modelling/data/processed/df_pattern_expanded.pickle')
        
    # return pd.DataFrame(expanded_rows)


class DataWrangling:
    @staticmethod
    def expand_naics_details(pattern_data, naics_expanding):
        """
        Expands composite NAICS codes (6 digits) into detailed codes (4 digits) for consistent analysis.

        Args:
            pattern_df (DataFrame): DataFrame with NAICS codes and descriptions.
            naics_mapping (dict): Mapping of composite NAICS codes to detailed codes and descriptions.

        Returns:
            DataFrame: Updated DataFrame with expanded NAICS details.
        """
        expanded_rows = []
        for _, row in pattern_data.iterrows():
            if row['naics'] in naics_expanding:
                for code, desc in zip(naics_expanding[row['naics']]['codes'],naics_expanding[row['naics']]['description']):
                    new_row = row.copy()
                    new_row['naics'] = code
                    new_row['DESCRIPTION'] = desc
                    expanded_rows.append(new_row)
            else:
                expanded_rows.append(row)
        return pd.DataFrame(expanded_rows)

    @staticmethod
    def merge_and_clean_data(gdp_df, pattern_df, naics_expanding):
        """
        Merges GDP and expanded pattern data, filtering necessary columns.

        Args:
            gdp_df (DataFrame): GDP dataset.
            pattern_df (DataFrame): Pattern dataset.
            naics_mapping (dict): Mapping for NAICS codes.

        Returns:
            DataFrame: Cleaned and merged DataFrame.
        """
        expanded_pattern_df = DataWrangling.expand_naics_details(pattern_df, naics_expanding)

        merged_df = pd.merge(gdp_df, expanded_pattern_df, on='FIPS', how='inner')

        filtered_columns = ['FIPS', 'NAICS', 'DESCRIPTION', 'EMP', 'QP1', 'AP', 'EST', '2022']
        return merged_df[filtered_columns]

    @staticmethod
    def summarize_by_fips(merged_df):
        """
        Aggregates data by FIPS for metrics like employment, payroll, and GDP.

        Args:
            merged_df (DataFrame): Merged dataset.

        Returns:
            DataFrame: Summarized dataset with aggregated metrics.
        """
        summary = merged_df.groupby('FIPS').agg({
            'EMP': 'sum',
            'QP1': 'sum',
            'AP': 'sum',
            'EST': 'sum',
            '2022': 'sum'
        }).reset_index()

        summary.rename(columns={
            'EMP': 'Total_Employment',
            'QP1': 'Quarterly_Payroll',
            'AP': 'Annual_Payroll',
            'EST': 'Total_Establishments',
            '2022': 'GDP_2022'
        }, inplace=True)

        return summary

    @staticmethod
    def process_occupation_metrics(occupation_df, priority_occupations):
        """
        Filters and aggregates occupation data for specific occupations.

        Args:
            occupation_df (DataFrame): Occupation dataset.
            priority_occupations (list): List of occupation codes to prioritize.

        Returns:
            DataFrame: Processed occupation metrics.
        """
        filtered_df = occupation_df[occupation_df['OCC_CODE'].isin(priority_occupations)]

        grouped_df = filtered_df.groupby(['FIPS', 'OCC_CODE']).agg({
            'EMP_OCCUPATION': 'sum'
        }).reset_index()

        return grouped_df

    @staticmethod
    def integrate_all_data(aggregated_data, occupation_data):
        """
        Combines aggregated GDP-pattern data with occupation metrics.

        Args:
            aggregated_data (DataFrame): Aggregated GDP and pattern data.
            occupation_data (DataFrame): Processed occupation metrics.

        Returns:
            DataFrame: Final dataset integrating all metrics.
        """
        final_df = pd.merge(aggregated_data, occupation_data, on='FIPS', how='left')

        final_df['EMP_OCCUPATION'] = final_df['EMP_OCCUPATION'].fillna(0)

        return final_df
