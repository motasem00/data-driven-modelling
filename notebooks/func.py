import pandas as pd
import os
import numpy as np

# Function to simplify NAICS codes and update them with expanded mappings
def process_naics_data(pattern_data, naics_expanding):
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
    pattern_data.to_pickle('data/processed_data/pkl/df_simplified_naics.pickle')
    
    return pattern_data

df_pattern = pd.DataFrame()  # Your DataFrame loading logic here
processed_df = process_naics_data(df_pattern, naics_expanding)
