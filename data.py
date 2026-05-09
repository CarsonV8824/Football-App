import os

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

def get_data() -> tuple[np.ndarray, np.ndarray]:

    college_stats = [
        'college_games',
        'college_pass_yds', 'college_pass_td', 'college_pass_int', 'college_pass_cmp_pct',
        'college_rush_yds', 'college_rush_td',
        'college_rec_yds', 'college_rec_td',
        'college_tackles', 'college_sacks', 'college_ints', 'college_fumbles'
    ]

    nfl_stats = [
        'g',
        'pass_cmp', 'pass_att', 'pass_yds', 'pass_td', 'pass_int',
        'rush_att', 'rush_yds', 'rush_td',
        'rec', 'rec_yds', 'rec_td',
        'tackles_solo', 'def_int', 'sacks',
        'career_av'
    ]

    combine_measurements = [
        'wonderlic', '40_yard', 'bench_press', 'vert_leap', 'broad_jump', 
        'shuttle', '3_cone', '60yd_shuttle'
    ]

    physical_attributes = [
        'height', 'weight', 'arm_length', 'hand_size'
    ]

    college_and_nfl = college_stats + nfl_stats

    path = "nfl_data.csv"
    data = pd.read_csv(path, sep=";")
    college = data[college_stats]
    nfl = data[nfl_stats]
    
    # Remove rows where all values are NaN, then impute remaining NaNs
    combined = pd.concat([college, nfl], axis=1)
    combined = combined.dropna(how='all')  # Drop rows that are entirely NaN
    
    # Impute missing values with mean
    imputer = SimpleImputer(strategy='mean')
    combined_imputed = imputer.fit_transform(combined)
    
    # Split back into college and nfl
    college = combined_imputed[:, :len(college_stats)]
    nfl = combined_imputed[:, len(college_stats):]

    print(f"Cleaned and imputed data: {len(college)} rows")
    
    return college, nfl

if __name__ == "__main__":
    get_data()