import happybase
import pandas as pd

# Connect to HBase
connection = happybase.Connection('localhost')  # Replace with your HBase server address
connection.open()

# Load dataset
file_path = '/mnt/data/EBEWE_cleaned_energy_data.txt'  # Adjust to the correct path
data = pd.read_csv(file_path, delimiter='\t')

# Create table if not exists
def create_table():
    tables = connection.tables()
    if b'Building_Efficiency' not in tables:
        connection.create_table(
            'Building_Efficiency',
            {
                'Building_Info': dict(),
                'Energy_Performance': dict(),
                'Emissions_Compliance': dict()
            }
        )
        print("Table 'Building_Efficiency' created.")
    else:
        print("Table already exists.")

create_table()

# Insert data into HBase
def insert_data():
    table = connection.table('Building_Efficiency')
    for _, row in data.iterrows():
        row_key = str(row['BUILDING ID'])
        table.put(
            row_key,
            {
                'Building_Info:GROSS_BUILDING_FLOOR_AREA': str(row['GROSS BUILDING FLOOR AREA']),
                'Building_Info:PROPERTY_TYPE': row['PROPERTY TYPE'],
                'Energy_Performance:SITE_EUI': str(row['SITE ENERGY USE INTENSITY (EUI)']),
                'Energy_Performance:WEATHER_NORMALIZED_SITE_EUI': str(row['WEATHER NORMALIZED SITE ENERGY USE INTENSITY (EUI)']),
                'Building_Info:YEAR_BUILT': str(row['YEAR BUILT']),
                'Emissions_Compliance:CARBON_DIOXIDE_EMISSIONS': str(row['CARBON DIOXIDE EMISSIONS']),
                'Building_Info:LADBS_Building_Category': row['LADBS Building Category']
            }
        )
        print(f"Inserted data for BUILDING_ID: {row_key}")

insert_data()
connection.close()