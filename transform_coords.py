import csv
from pyproj import CRS, Transformer

# Define the projection
# Converting from UTM (zone 30N) to WGS84
input_proj = CRS('epsg:32630')  # input projection
output_proj = CRS('epsg:4326')  # WGS84

# Create a transformer object for transforming coordinates
transformer = Transformer.from_crs(input_proj, output_proj, always_xy=True)

# Open the input CSV file and read data
with open('dirgennouniv.csv', mode='r') as infile, open('dirgennouniv_with_latlong.csv', mode='w', newline='') as outfile:
    reader = csv.reader(infile, delimiter=';')
    writer = csv.writer(outfile, delimiter=';')

    # Read the header from the original file
    header = next(reader)
    
    # Add new headers for Latitude and Longitude
    header.extend(['Latitude', 'Longitude', 'Address'])
    writer.writerow(header)

    # Process each row
    for row in reader:
        try:
            x = float(row[14])
            y = float(row[15])
            ad= row[11]+", "+row[6]+", "+row[7]

            # Convert X, Y to Latitude, Longitude
            lon, lat = transformer.transform(x, y)
                
            # Append the Latitude, Longitude and Address to the row
            row.extend([lat, lon, ad])

        except ValueError:
            print(f"Skipping row with invalid coordinates: {row}")
            # Optionally, you can append empty latitude/longitude if the conversion fails
            row.extend(['', ''])

        # Write the updated row to the new file
        writer.writerow(row)
