def extract_PA_and_Times(file_path):
    PA_accessed_times = {}
    PA_valid_count = 0
    Time_valid_count = 0
    DATA_total_count = 0

    try:
        with open(file_path, 'r') as file:
            for line in file:
                DATA_total_count += 1
                print(f"目前第：{DATA_total_count}筆", end = '\r')
                time, virtual_address, physical_address = line.split()
                time = time.strip(':')

                # 跳過虛擬位址為0或實體位址為0的行
                if physical_address == '0' or virtual_address == '0':
                    continue

                # 將實體位址補到16位
                physical_address = physical_address.zfill(16)

                if physical_address not in PA_accessed_times:
                    PA_accessed_times[physical_address] = []
                    PA_valid_count += 1
                
                if time not in PA_accessed_times[physical_address]:
                    PA_accessed_times[physical_address].append(time)
                    Time_valid_count += 1

    except FileNotFoundError:
        print(f"找不到檔案： {file_path}")
    except Exception as e:
        print(f"發生錯誤： {e}")

    return PA_accessed_times, PA_valid_count, Time_valid_count, DATA_total_count


# 使用檔案路徑來呼叫函式
logfile_path = 'log.txt'
PA_accessed_times, PA_valid_count, Time_valid_count, DATA_total_count = extract_PA_and_Times(logfile_path)


# 按鍵排序並印出結果 & 打開檔案進行寫入
outfile_path = 'out.txt'
with open(outfile_path, 'w') as output_file:
    PA_print_count = 0
    Time_print_count = 0
    for phy_addr in sorted(PA_accessed_times):
        time_ns = PA_accessed_times[phy_addr]
        output_line = f"實體位址: {phy_addr} 被存取過的時間點: {time_ns}\n"
        print(output_line)
        output_file.write(output_line)
        PA_print_count += 1
        Time_print_count += len(time_ns)

    # 原始資料總量
    total_data_line = f"\n總資料量：{DATA_total_count}\n"
    print(total_data_line, end='')
    output_file.write(total_data_line)

    # 讀入的有效實體位址個數
    valid_pa_line = f"有效實體位址個數：{PA_valid_count}\n"
    print(valid_pa_line, end='')
    output_file.write(valid_pa_line)

    # 讀入的有效存取時間（點）個數
    valid_time_line = f"有效存取時間個數：{Time_valid_count}\n"
    print(valid_time_line, end='')
    output_file.write(valid_time_line)

    # dict中實體位址個數
    dict_pa_line = f"dict中實體位址個數：{PA_print_count}\n"
    print(dict_pa_line, end='')
    output_file.write(dict_pa_line)

    # dict中虛擬位址個數
    dict_va_line = f"dict中虛擬位址個數：{Time_print_count}\n"
    print(dict_va_line, end='')
    output_file.write(dict_va_line)

print(f"已輸出到：{outfile_path}")
