import pandas as pd
import os
import numpy as np

class DataWrangling:
    def __init__(self):
        # Initialize any necessary attributes or load configurations if needed
        pass

    def process_naics_data(self, pattern_data, naics_expanding):
        """
        Simplifies NAICS codes to the first 4 digits and updates them based on expanded mappings.
        
        Parameters:
            pattern_data (pd.DataFrame): DataFrame containing the NAICS codes and descriptions.
            naics_expanding (dict): Dictionary with new NAICS codes and corresponding details.
        
        Returns:
            pd.DataFrame: Updated DataFrame with simplified and updated NAICS codes and descriptions.
        """
        # Simplify NAICS codes to the first 4 digits and create a description dictionary
        pattern_data['naics'] = pattern_data['naics'].apply(lambda x: x[:4] if len(x) >= 4 else x)
        description_ref = pattern_data.set_index('naics')['DESCRIPTION'].to_dict()

        # Apply expanded mappings
        for new_code, details in naics_expanding.items():
            # Update NAICS codes
            pattern_data.loc[pattern_data['naics'].isin(details['codes']), 'naics'] = new_code
            
            # Create and update descriptions based on mappings
            updated_descriptions = [
                f"{code} ({desc})"
                for code, desc in zip(details['codes'], details['description'])
                if code in description_ref
            ]
            description = ', '.join(updated_descriptions)
            pattern_data.loc[pattern_data['naics'] == new_code, 'DESCRIPTION'] = description

        # Reset index and save the processed DataFrame
        pattern_data.reset_index(drop=True, inplace=True)
        pattern_data.to_pickle('/content/data-driven-modelling/data/processed/df_simplified_naics.pickle')
        
        return pattern_data

# Example usage
if __name__ == '__main__':
    wrangler = DataWrangling()
    naics_expanding = {
        '3330A1': {
            'codes': ['3331', '3332', '3334', '3339'],
            'description': [
                'Agricultural Implement Manufacturing',
                'Industrial Machinery Manufacturing',
                'Metalworking Machinery Manufacturing',
                'Other General Purpose Machinery Manufacturing'
            ]
        },
        # Additional mappings with unique keys...
    }

    df_pattern = pd.DataFrame()  # Your DataFrame loading logic here
    processed_df = wrangler.process_naics_data(df_pattern, naics_expanding)
    print(processed_df)



# import pandas as pd
# import os
# import numpy as np

# # Function to simplify NAICS codes and update them with expanded mappings
# def process_naics_data(pattern_data, naics_expanding):
#     # Simplify NAICS codes to the first 4 digits and create a description dictionary
#     pattern_data['naics'] = pattern_data['naics'].apply(lambda x: x[:4] if len(x) >= 4 else x)
#     description_ref = pattern_data.set_index('naics')['DESCRIPTION'].to_dict()

#     # Apply expanded mappings
#     for new_code, details in naics_expanding.items():
#         # Update NAICS codes
#         pattern_data.loc[pattern_data['naics'].isin(details['codes']), 'naics'] = new_code
        
#         # Create and update descriptions based on mappings
#         updated_descriptions = [
#             f"{code} ({desc})"
#             for code, desc in zip(details['codes'], details['description'])
#             if code in description_ref
#         ]
#         description = ', '.join(updated_descriptions)
#         pattern_data.loc[pattern_data['naics'] == new_code, 'DESCRIPTION'] = description

#     # Reset index and save the processed DataFrame
#     pattern_data.reset_index(drop=True, inplace=True)
#     pattern_data.to_pickle('data/processed_data/pkl/df_simplified_naics.pickle')
    
#     return pattern_data
    
#     naics_expanding = {
#     '3330A1': {
#         'codes': ['3331', '3332', '3334', '3339'],
#         'description': [
#             'Agricultural Implement Manufacturing',
#             'Industrial Machinery Manufacturing',
#             'Metalworking Machinery Manufacturing',
#             'Other General Purpose Machinery Manufacturing'
#         ]
#     },
#     # Additional mappings with unique keys...
# }


# df_pattern = pd.DataFrame()  # Your DataFrame loading logic here
# processed_df = process_naics_data(df_pattern, naics_expanding)
