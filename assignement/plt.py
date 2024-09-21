import pandas as pd
import matplotlib.pyplot as plt

# Assuming already have all the file paths
file_paths = [f"tab{i}" for i in range(40, 58)]

data = pd.DataFrame()

# Read each file and extract the last portion of data
for file in file_paths:
    with open(file, 'r') as f:
        lines = f.readlines()
        # Read each line and skip the lines of data that are not needed.
        data_lines = [line.strip() for line in lines if not line.startswith(('PDS', '^', 'END', 'OBJECT'))]

        # Split each line and construct a DataFrame.
        temp_data = [line.split() for line in data_lines]

        # Print the information of the current file.
        print(f"File: {file}, Rows: {len(temp_data)}, Columns: {len(temp_data[0]) if temp_data else 0}")

        temp_df = pd.DataFrame(temp_data)
        data = pd.concat([data, temp_df], ignore_index=True)

# Determine the number of columns
num_columns = data.shape[1]
print(f"Total columns after merging: {num_columns}")

# Dynamically define column names
columns = [f'Col{i + 1}' for i in range(num_columns)]

# Update the DataFrame's column names to the dynamically defined names
data.columns = columns

# Convert the data type to floating point
data = data.apply(pd.to_numeric, errors='coerce')

# Delete rows containing -1.00
data_cleaned = data[(data != -1.00).all(axis=1)]

# Create a 3D scatter plot
fig = plt.figure(figsize=(12, 8))

# figure1: Density and sigma density at different altitudes and latitudes.
ax1 = fig.add_subplot(121, projection='3d')
scatter1 = ax1.scatter(data_cleaned['Col1'], data_cleaned['Col2'], data_cleaned['Col3'],
                       c=data_cleaned['Col7'], cmap='hot', s=50, alpha=0.8)  
ax1.plot(data_cleaned['Col1'], data_cleaned['Col2'], data_cleaned['Col3'], color='black', alpha=0.5)  
ax1.set_xlabel('Latitude')
ax1.set_ylabel('Longitude')
ax1.set_zlabel('Altitude (km)')
ax1.set_title('Density and Sigma Density')
fig.colorbar(scatter1, ax=ax1, label='Density')

# figure2: Scale height and sigma scale height at different altitudes and latitudes.
ax2 = fig.add_subplot(122, projection='3d')
scatter2 = ax2.scatter(data_cleaned['Col1'], data_cleaned['Col2'], data_cleaned['Col3'],
                       c=data_cleaned['Col9'], cmap='cool', s=50, alpha=0.8)  
ax2.plot(data_cleaned['Col1'], data_cleaned['Col2'], data_cleaned['Col3'], color='black', alpha=0.5)  
ax2.set_xlabel('Latitude')
ax2.set_ylabel('Longitude')
ax2.set_zlabel('Altitude (km)')
ax2.set_title('Scale Height and Sigma Scale Height')
fig.colorbar(scatter2, ax=ax2, label='Scale Height')

plt.show()
