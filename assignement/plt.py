import pandas as pd
import matplotlib.pyplot as plt

# 假设你已经有所有文件路径
file_paths = [f"tab{i}" for i in range(40, 58)]

data = pd.DataFrame()

# 读取每个文件并提取最后部分数据
for file in file_paths:
    with open(file, 'r') as f:
        lines = f.readlines()
        # 读取每一行并跳过不需要的数据行
        data_lines = [line.strip() for line in lines if not line.startswith(('PDS', '^', 'END', 'OBJECT'))]

        # 分割每一行并构建DataFrame
        temp_data = [line.split() for line in data_lines]

        # 打印当前文件的信息
        print(f"File: {file}, Rows: {len(temp_data)}, Columns: {len(temp_data[0]) if temp_data else 0}")

        temp_df = pd.DataFrame(temp_data)
        data = pd.concat([data, temp_df], ignore_index=True)

# 处理数据
# 确定列数
num_columns = data.shape[1]
print(f"Total columns after merging: {num_columns}")

# 动态定义列名
columns = [f'Col{i + 1}' for i in range(num_columns)]

# 将DataFrame的列名更新为动态列名
data.columns = columns

# 将数据类型转换为浮点型
data = data.apply(pd.to_numeric, errors='coerce')

# 删除包含-1.00的行
data_cleaned = data[(data != -1.00).all(axis=1)]

# 绘制3D散点图
fig = plt.figure(figsize=(12, 8))

# 图1: 密度和标准密度
ax1 = fig.add_subplot(121, projection='3d')
scatter1 = ax1.scatter(data_cleaned['Col1'], data_cleaned['Col2'], data_cleaned['Col3'],
                       c=data_cleaned['Col7'], cmap='hot', s=50, alpha=0.8)  # 假设第七列是密度
ax1.plot(data_cleaned['Col1'], data_cleaned['Col2'], data_cleaned['Col3'], color='black', alpha=0.5)  # 绘制三维线
ax1.set_xlabel('Latitude')
ax1.set_ylabel('Longitude')
ax1.set_zlabel('Altitude (km)')
ax1.set_title('Density and Sigma Density')
fig.colorbar(scatter1, ax=ax1, label='Density')

# 图2: 尺度高度和标准尺度高度
ax2 = fig.add_subplot(122, projection='3d')
scatter2 = ax2.scatter(data_cleaned['Col1'], data_cleaned['Col2'], data_cleaned['Col3'],
                       c=data_cleaned['Col9'], cmap='cool', s=50, alpha=0.8)  # 假设第九列是尺度高度
ax2.plot(data_cleaned['Col1'], data_cleaned['Col2'], data_cleaned['Col3'], color='black', alpha=0.5)  # 绘制三维线
ax2.set_xlabel('Latitude')
ax2.set_ylabel('Longitude')
ax2.set_zlabel('Altitude (km)')
ax2.set_title('Scale Height and Sigma Scale Height')
fig.colorbar(scatter2, ax=ax2, label='Scale Height')

plt.show()
