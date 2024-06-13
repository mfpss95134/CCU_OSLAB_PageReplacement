import pickle


def print_on_screen(target):
    PA_printed_count = 0
    TS_printed_count = 0
    for phy_addr in sorted(target):
        time_stamp = target[phy_addr]
        outputLine = f"實體位址: {phy_addr} 被存取過的時刻: {time_stamp}"
        print(output_line)
        PA_printed_count += 1
        TS_printed_count += len(time_stamp)

    # 統計資料量，供後續驗證
    outputLine = f"\n   資料總筆數: {DATA_total_count}"
    print(outputLine)
    outputLine = f"實體位址有效個數: {PA_valid_count}"
    print(outputLine)
    outputLine = f"時間戳記有效個數: {TS_valid_count}"
    print(outputLine)
    outputLine = f"實體位址印出個數: {PA_printed_count}"
    print(outputLine)
    outputLine = f"時間戳記印出個數: {TS_printed_count}"
    print(outputLine)

    return


def write_to_txt(target, file_path):
    # 按鍵排序並印出結果 & 打開檔案進行寫入
    with open(file_path, 'w') as outputFile:
        PA_written_count = 0
        TS_written_count = 0
        for phy_addr in sorted(target):
            time_stamp = target[phy_addr]
            output_line = f"實體位址: {phy_addr} 被存取過的時刻: {time_stamp}\n"
            outputFile.write(output_line)
            PA_written_count += 1
            TS_written_count += len(time_stamp)

        # 統計資料量，供後續驗證
        output_line = f"\n\t 資料總筆數: {DATA_total_count}\n"
        outputFile.write(output_line)
        output_line = f"實體位址有效個數: {PA_valid_count}\n"
        outputFile.write(output_line)
        output_line = f"時間戳記有效個數: {TS_valid_count}\n"
        outputFile.write(output_line)
        output_line = f"實體位址寫出個數: {PA_written_count}\n"
        outputFile.write(output_line)
        output_line = f"時間戳記寫出個數: {TS_written_count}\n"
        outputFile.write(output_line)

    print(f"已輸出: {file_path}")
    return


def read_from_bin(file_path):
    with open(file_path, "rb") as inputFile:
        loaded_data = pickle.load(inputFile)
    print(f"已載入: {file_path}")
    return loaded_data


def write_to_bin(target, file_path):
    with open(file_path, "wb") as outputFile:
        pickle.dump(target, outputFile)
    print(f"已輸出: {file_path}")
    return


def extract_PA_accessed_time_stamps(file_path):
    PA_accessed_time_stamps = {}
    DATA_total_count = 0
    PA_valid_count   = 0
    TS_valid_count   = 0

    try:
        with open(file_path, 'r') as file:
            for line in file:
                DATA_total_count += 1
                print(f"目前第: {DATA_total_count}筆", end = '\r')
                time_stamp, virtual_address, physical_address = line.split()
                time_stamp = float(time_stamp.strip(':'))

                # 跳過虛擬位址為0或實體位址為0的行
                if physical_address == '0' or virtual_address == '0':
                    continue

                # 將實體位址補到16位
                physical_address = physical_address.zfill(16)

                if physical_address not in PA_accessed_time_stamps:
                    PA_accessed_time_stamps[physical_address] = []
                    PA_valid_count += 1
                
                if time_stamp not in PA_accessed_time_stamps[physical_address]:
                    PA_accessed_time_stamps[physical_address].append(time_stamp)
                    TS_valid_count += 1

    except FileNotFoundError:
        print(f"找不到: {file_path}")
    except Exception as e:
        print(f"錯誤: {e}")

    return PA_accessed_time_stamps, DATA_total_count, PA_valid_count, TS_valid_count


#########################################################################################
# 初始化一些會用到的參數
PA_accessed_time_stamps = {}
DATA_total_count        = 0
PA_valid_count          = 0
TS_valid_count          = 0


# 從原始檔中抓整理出每個實體位址被存取的時間戳記(時刻)
PA_accessed_time_stamps, DATA_total_count, PA_valid_count, TS_valid_count = extract_PA_accessed_time_stamps("./perf.data.txt")


# 輸出到文字檔和二進制檔
write_to_txt(PA_accessed_time_stamps, "./PA_accessed_time_stamps.txt")
write_to_bin(PA_accessed_time_stamps, "./PA_accessed_time_stamps.bin")


# 從現有的二進制檔中讀取
#PA_accessed_time_stamps = read_from_bin("./PA_accessed_time_stamps.bin")
# 印到螢幕上檢視
#print_on_screen(PA_accessed_time_stamps)