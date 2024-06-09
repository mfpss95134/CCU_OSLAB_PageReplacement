import pickle
import numpy as np
import matplotlib.pyplot as plt

def read_from_binary():
    inputFile_path = "access_time_seqs.bin"
    with open(inputFile_path, "rb") as inputFile:
        loaded_data = pickle.load(inputFile)
    print(f"已載入：{inputFile_path}")
    return loaded_data

# 訪問數據
data = read_from_binary()

# 將時間轉換為納秒
for phy_addr in data:
    data[phy_addr] = np.array(data[phy_addr]) * 10**9

# 計算訪問距離
distances = []
for times in data.values():
    distances.extend(np.diff(times))
distances = np.array(distances)

# 剔除第一個訪問（距離為0）
distances = distances[distances > 0]

# 繪製直方圖
plt.hist(distances, bins=50, edgecolor='black')
plt.xlabel('Distance (ns)')
plt.ylabel('Frequency')
plt.title('LRU Distance Distribution')
plt.grid(True)
plt.savefig("lru_distance_distribution_hist.png")  # 儲存圖片到圖片檔
plt.show()