import pickle
import pandas as pd
import numpy as np
import plotly.express as px

def read_from_binary():
    # 從二進制文件中讀取數據
    inputFile_path = "access_time_seqs.bin"
    with open(inputFile_path, "rb") as inputFile:
        loaded_data = pickle.load(inputFile)
    print(f"已載入：{inputFile_path}")
    return loaded_data

# 訪問數據
data = read_from_binary()

# 將訪問數據轉換為DataFrame
data_list = []
for phy_addr, times in data.items():
    # 將物理地址（Phy_addr）和對應的時間（times）轉換成DataFrame的列表形式
    data_list.extend([(phy_addr, time) for time in times])
df = pd.DataFrame(data_list, columns=['Phy_addr', 'Time'])

# 計算訪問距離
df['Time'] = pd.to_numeric(df['Time'])
df = df.sort_values(by=['Phy_addr', 'Time'])
df['Distance'] = df.groupby('Phy_addr')['Time'].diff().fillna(0).astype(int)

# 剔除第一個訪問（距離為0）
distances = df['Distance'][df['Distance'] > 0]

# 統計訪問距離的頻率並計算百分比
distance_counts = distances.value_counts()
total_counts = distance_counts.sum()
distance_distribution = (distance_counts / total_counts) * 100

# 獲取佔比前五高的距離及其百分比
top_five_distances = distance_distribution.nlargest(5)
top_five_distances_index = top_five_distances.index
top_five_distances_values = top_five_distances.values

# 使用Plotly繪製LRU距離分布圖
fig = px.bar(x=distance_distribution.index, y=distance_distribution.values, labels={'x': 'Distance (ms)', 'y': 'Percentage (%)'}, title='LRU Distance Distribution')

# 添加文本標籤以顯示佔比前五高的長條的百分比
for distance, value in zip(top_five_distances_index, top_five_distances_values):
    fig.add_annotation(
        x=distance, y=value,
        text=f"{value:.2f}%",  # 文本內容為百分比，保留兩位小數
        showarrow=True,
        arrowhead=1,
        arrowcolor="black",
        arrowsize=1,
        arrowwidth=1,
        ax=0,
        ay=-40
    )

fig.show()
print("圖表已顯示")
