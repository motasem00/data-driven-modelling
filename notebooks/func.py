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
                'Agriculture, Construction, and Mining Machinery Manufacturing',
                'Industrial Machinery Manufacturing',
                'Ventilation, Heating, Air-Conditioning, and Commercial Refrigeration Equipment Manufacturing',
                'Other General Purpose Machinery Manufacturing'
            ]
        },

         '3330A1': {
            'codes': ['3323', '3324'],
            'description': [
                'Architectural and Structural Metals Manufacturing',
                'Boiler, Tank, and Shipping Container Manufacturing',
            ]
        },

        '3320A1': {
            'codes': ['3321', '3322', '3325', '3326', '3329'],
            'description': [
                'Forging and Stamping',
                'Cutlery and Handtool Manufacturing',
                'Hardware Manufacturing',
                'Spring and Wire Product Manufacturing',
                'Other Fabricated Metal Product Manufacturing'
            ]
        },
        
        '3250A1': {
            'codes': ['3251', '3252', '3253', '3259'],
            'description': [
                'Basic Chemical Manufacturing',
                'Resin, Synthetic Rubber, and Artificial and Synthetic Fibers and Filaments Manufacturing',
                'Pesticide, Fertilizer, and Other Agricultural Chemical Manufacturing',
                'Other Chemical Product and Preparation Manufacturing'
            ]
        },

        '3370A1': {
            'codes': ['3371', '3372'],
            'description': [
                'Household and Institutional Furniture and Kitchen Cabinet Manufacturing',
                'Office Furniture (including Fixtures) Manufacturing'
            ]
        },
    }

    df_pattern = pd.DataFrame()  # Your DataFrame loading logic here
    processed_df = wrangler.process_naics_data(df_pattern, naics_expanding)
    print(processed_df)
