import pandas as pd
import numpy as np

def convert_sqft(x):
    try:
        if isinstance(x, str):
            if '-' in x:
                a, b = x.split('-')
                return (float(a) + float(b)) / 2
            return float(x)
        return float(x)
    except:
        return None

def extract_bhk(size):
    try:
        return int(size.split()[0])
    except:
        return None

def load_and_prepare_data(path):
    df = pd.read_csv(path)

    # Keep required columns
    df = df[
        ['location', 'total_sqft', 'price', 'bath', 'size', 'availability']
    ]

    # Extract bhk from size
    df['bhk'] = df['size'].apply(extract_bhk)
    df.drop(columns=['size'], inplace=True)

    # Drop missing values
    df.dropna(inplace=True)

    # Convert sqft
    df['total_sqft'] = df['total_sqft'].apply(convert_sqft)
    df.dropna(inplace=True)

    # Target variable
    df['price_per_sqft'] = (df['price'] * 100000) / df['total_sqft']

    # Remove extreme outliers
    df = df[df['price_per_sqft'] < df['price_per_sqft'].quantile(0.95)]

    # Location density
    location_counts = df['location'].value_counts()
    df['location_density'] = df['location'].map(location_counts)

    # Reduce rare locations
    df['location'] = df['location'].apply(
        lambda x: x if location_counts[x] > 10 else 'other'
    )

    # Infrastructure score (proxy)
    df['infrastructure_score'] = df['bath'] + df['bhk']

    # Log transform
    df['log_total_sqft'] = np.log(df['total_sqft'])

    return df
