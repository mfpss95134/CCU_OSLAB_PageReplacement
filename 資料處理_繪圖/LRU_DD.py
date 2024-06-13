import pickle
import numpy as np
import matplotlib.pyplot as plt

def read_from_bin(file_path):
    # 從二進位檔案中讀取資料
    with open(file_path, "rb") as inputFile:
        loaded_data = pickle.load(inputFile)
    print(f"已載入: {file_path}")
    return loaded_data

def calculate_distances(data):
    # 計算每個訪問時間序列的訪問距離
    distances = []
    for times in data.values():
        distances.extend(np.diff(times))
    return np.array(distances)

def plot_histogram_with_percentage(distances, bins=50):
    # 計算每個bin中的距離數量 和 bin的邊界
    counts, bin_edges = np.histogram(distances, bins=bins)
    total_distances = len(distances)
    percentages = (counts / total_distances) * 100

    # 繪製直方圖，顯示距離佔總距離的百分比
    plt.bar(bin_edges[:-1], percentages, width=np.diff(bin_edges), edgecolor='black', align='edge')
    plt.xlabel('Distance (ns)')
    plt.ylabel('Percentage (%)')
    plt.title('LRU Distance Distribution')
    plt.grid(True)
    
    # 將 X 軸刻度轉換為固定格式
    plt.ticklabel_format(axis='x', style='plain')
    plt.show()

def main(input_file_path="PA_accessed_time_stamps.bin"):
    data = read_from_bin(input_file_path)
    
    # 將時間轉換為納秒
    for phy_addr in data:
        data[phy_addr] = np.array(data[phy_addr]) * 10**9
    
    # 計算訪問距離
    distances = calculate_distances(data)
    
    # 剔除第一個訪問（距離為0）
    distances = distances[distances > 0]
    
    # 繪製直方圖
    plot_histogram_with_percentage(distances)

if __name__ == "__main__":
    main()
