import sys

class Frame:
    def __init__(self, frame_number):
        self.frame_number = frame_number  # 頁框編號
        self.ref_count = 0                # 訪問次數
        self.age_gen = 2                  # 初始設置在第二代中

    def __repr__(self):
        # 提供框架的字符串表示
        return f"Frame({hex(self.frame_number)}, ref_count={self.ref_count}, age_gen={self.age_gen})"

    def __eq__(self, other):
        # 覆寫等於方法，框架編號相同即視為相等
        return isinstance(other, Frame) and self.frame_number == other.frame_number

    def __hash__(self):
        # 允許在集合和字典中使用的哈希方法
        return hash(self.frame_number)




class MGLRU:
    def __init__(self, num_gens=4, gen_size=2):
        self.num_gens = num_gens  # 世代數量
        self.gen_size = gen_size  # 每代大小
        self.gens = {i: [] for i in range(1, num_gens + 1)}  # 初始化1~4代，分別代表年輕到老世代
        self.swap = []                                       # Swap Space，用 5 來代替


    def access(self, frame_number):
        #print(f"Accessing Frame Number: {hex(frame_number)}")
        global HitCount
        global MissCount

        found_gen_num, found_frame = self.search(frame_number)
        if found_gen_num:
            # 存在於1~4代某gen中
            # 提升到最年輕世代的頭部
            #print(f"{found_frame} Found in Gen {found_gen_num}, Promoting to TOP...")
            HitCount += 1
                
            self.promote(found_gen_num, found_frame)
        else:
            # 不存在於任一gen中
            # 是全新的Frame或是被捨棄過的Frame
            #print("Firstly accessed, Adding to Gen 2...")
            MissCount += 1

            # 插入到gen[2]
            new_frame = Frame(frame_number)
            self.gens[2].insert(0, new_frame)

        # 收尾整理所有的gen然後輸出檢視
        self.balance_gens()
        #self.print_gens()
        return


    def search(self, frame_number):
        # 尋找特定框架，若找到則返回
        # 先搜尋各個世代
        for gen_num, gen in self.gens.items():
            for f in gen:
                if f.frame_number == frame_number:
                    return gen_num, f
        # 什麼都沒找到，無功而返
        return None, None


    def promote(self, cur_gen_num, frame):
        cur_gen = self.gens[cur_gen_num]
        cur_gen.remove(frame)

        if cur_gen_num == 1:
            #print(f"A:{cur_gen_num}")
            self.gens[1].insert(0, frame)
        else:
            #print(f"B:{cur_gen_num}")
            frame.age_gen -= 1
            tgt_gen_num = cur_gen_num-1
            #print(f"B:{tgt_gen_num}")
            self.gens[tgt_gen_num].insert(0, frame)
        
        return
        """
        #這段是原本錯誤的promote流程
        cur_gen = self.gens[cur_gen_num]
        frame_idx = cur_gen.index(frame)

        if frame_idx != 0:
            # 移動到所處世代的頭部
            cur_gen.insert(0, cur_gen.pop(frame_idx))
        elif frame_idx == 0:
            # 若是已在某世代的頭部的話就檢查有沒有上層世代可以提升
            # 有上層世代的話就往上升，沒有的話就代表已經在頂層世代的頭部了，不用動
            if cur_gen_num > 1:
                cur_gen.remove(frame) #從當前層移除
                frame.age_gen -= 1    #層數上升
                self.gens[cur_gen_num - 1].append(frame) #附加到上層的尾部，加到頭還尾要再確認
                print(f"Promoted: {frame}")
                return
        """


    def balance_gens(self):
        # 處理每代的溢出情況，進行框架的遷移或淘汰
        for i in range(1, self.num_gens + 1):
            while len(self.gens[i]) > self.gen_size:
                oldest_frame = self.gens[i].pop()
                if i == self.num_gens:
                    # 若已是在最老世代，就直接置換掉(swap out)
                    del(oldest_frame)
                else:
                    # 移動到下個時代的頭部
                    oldest_frame.age_gen += 1
                    self.gens[i+1].insert(0, oldest_frame)
        return


    def print_gens(self):
        print("\n")
        # 印出所有世代的狀態
        for gen_num, gen in self.gens.items():
            print(f"Gen {gen_num}:")
            for f in gen:
                print(f"\t{f}")
        print("-------------------------------------------------------------")
        return




# Example usage
HitCount  = 0
MissCount = 0
if __name__ == "__main__":
    if len(sys.argv) == 2:
        # 有指定要模擬的log檔參數
        phy_addrs = []
        with open(sys.argv[1], 'r') as pmu_log_file:
            for line in pmu_log_file:
                addr_hex = line.strip()  #移除行尾的換行符號和空格
                addr_int = int(addr_hex, 16)  #將16進制轉換為10進制
                phy_addrs.append(addr_int)
        print(f"len(phy_addrs): {len(phy_addrs)}")
        input()
        mglru = MGLRU(4, 65536) ## 4*65536=262144  ## 1GiB記憶體

        for i in range(len(phy_addrs)):
            print(f"{i}/{len(phy_addrs)}: {phy_addrs[i] >> 12}", end="\r\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r")
            mglru.access(phy_addrs[i] >> 12)
    else:
        # 沒指定參數，用預設的簡單測試資料模擬
        mglru = MGLRU()
        test_sequence = [1, 2, 3, 4, 5, 6, 7, 8, 8, 7, 7, 6,   7,7,  4,  1]
        
        for frame_number in test_sequence:
            mglru.access(frame_number)
    
    print("\n------------------------------------------------------------------------------------------------------------------------")
    print(f"HitCount: {HitCount}")
    print(f"MissCount: {MissCount}")
    print(f"HitRation: {(HitCount * 100) / (HitCount + MissCount)} %")
    #print(f"len(Gens) {len(mglru.gens)}")
    #print(f"len(Gen 1) {len(mglru.gens[1])}")
    #print(f"len(Gen 2) {len(mglru.gens[2])}")
    #print(f"len(Gen 3) {len(mglru.gens[3])}")
    #print(f"len(Gen 4) {len(mglru.gens[4])}")
    #mglru.print_gens()