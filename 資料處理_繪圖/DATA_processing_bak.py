import pickle


def print_on_screen():
    PA_print_count = 0
    TIME_print_count = 0
    for phy_addr in sorted(PA_access_time_seqs):
        time_stamp = PA_access_time_seqs[phy_addr]
        output_line = f"實體位址: {phy_addr} 被存取過的時間點: {time_stamp}\n"
        print(output_line)
        PA_print_count += 1
        TIME_print_count += len(time_stamp)

    # 原始資料總量
    output_line = f"\n資料總筆數：{DATA_total_count}"
    print(output_line)

    # 讀入的有效實體位址個數
    output_line = f"有效實體位址個數：{PA_valid_count}"
    print(output_line)

    # 讀入的有效存取時間（點）個數
    output_line = f"有效存取時間個數：{TIME_valid_count}"
    print(output_line)

    # dict中實體位址個數，檢查用
    output_line = f"印出了 {PA_print_count} 個實體位址"
    print(output_line)

    # dict中時間戳記個數，檢查用
    output_line = f"印出了 {TIME_print_count} 個時間戳記"
    print(output_line)

    return


def output_to_text():
    # 按鍵排序並印出結果 & 打開檔案進行寫入
    outputFile_path = 'access_time_seqs.txt'
    with open(outputFile_path, 'w') as outputFile:
        PA_print_count = 0
        TIME_print_count = 0
        for phy_addr in sorted(PA_access_time_seqs):
            time_stamp = PA_access_time_seqs[phy_addr]
            output_line = f"實體位址: {phy_addr} 被存取過的時間點: {time_stamp}\n"
            outputFile.write(output_line)
            PA_print_count += 1
            TIME_print_count += len(time_stamp)

        # 原始資料總量
        output_line = f"\n資料總筆數：{DATA_total_count}\n"
        outputFile.write(output_line)

        # 讀入的有效實體位址個數
        output_line = f"有效實體位址個數：{PA_valid_count}\n"
        outputFile.write(output_line)

        # 讀入的有效存取時間（點）個數
        output_line = f"有效存取時間個數：{TIME_valid_count}\n"
        outputFile.write(output_line)

        # dict中實體位址個數
        output_line = f"印出了 {PA_print_count} 個實體位址\n"
        outputFile.write(output_line)

        # dict中虛擬位址個數
        output_line = f"印出了數 {TIME_print_count} 個時間戳記\n"
        outputFile.write(output_line)

    print(f"已輸出：{outputFile_path}")
    return


def output_to_binary():
    outputFile_path = "access_time_seqs.bin"
    with open(outputFile_path, "wb") as outputFile:
        pickle.dump(PA_access_time_seqs, outputFile)

    print(f"已輸出：{outputFile_path}")
    return


def read_from_binary():
    inputFile_path = "access_time_seqs.bin"
    with open(inputFile_path, "rb") as inputFile:
        loaded_data = pickle.load(inputFile)

    print(f"已載入：{inputFile_path}")
    return loaded_data


def extract_PA_and_AccessedTIMEStamps(file_path):
    PA_access_time_seqs = {}
    PA_valid_count = 0
    TIME_valid_count = 0
    DATA_total_count = 0

    try:
        with open(file_path, 'r') as file:
            for line in file:
                DATA_total_count += 1
                print(f"目前第：{DATA_total_count}筆", end = '\r')
                time, virtual_address, physical_address = line.split()
                time = float(time.strip(':'))

                # 跳過虛擬位址為0或實體位址為0的行
                if physical_address == '0' or virtual_address == '0':
                    continue

                # 將實體位址補到16位
                physical_address = physical_address.zfill(16)

                if physical_address not in PA_access_time_seqs:
                    PA_access_time_seqs[physical_address] = []
                    PA_valid_count += 1
                
                if time not in PA_access_time_seqs[physical_address]:
                    PA_access_time_seqs[physical_address].append(time)
                    TIME_valid_count += 1

    except FileNotFoundError:
        print(f"找不到檔案： {file_path}")
    except Exception as e:
        print(f"發生錯誤： {e}")

    return PA_access_time_seqs, PA_valid_count, TIME_valid_count, DATA_total_count


# 使用檔案路徑來呼叫函式
logFile_path = 'perf.data.txt'
PA_access_time_seqs = {}
PA_valid_count   = 0
TIME_valid_count = 0
DATA_total_count = 0
PA_access_time_seqs, PA_valid_count, TIME_valid_count, DATA_total_count = extract_PA_and_AccessedTIMEStamps(logFile_path)
loaded_data = {}


# 呼叫
#PA_access_time_seqs = read_from_binary()
output_to_text()
output_to_binary()
#print_on_screen()