class Frame:
    def __init__(self, frame_number):
        self.frame_number = frame_number  # 頁框編號
        self.ref_count = 0                # 訪問次數
        self.age_gen = 3                  # 初始設置在第三代中

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
        self.evict_cnt = 0     # 淘汰數量計數
        self.gens = {i: [] for i in range(1, num_gens + 1)}  # 初始化每代


    def access(self, frame_number):
        print(f"Accessing Frame:{hex(frame_number)}")

        found_gen_num, found_frame = self.search(frame_number)
        if found_gen_num:
            # 已存在於某gen中，往上層提升
            print(f"{found_frame} Found in Gen {found_gen_num}, Promoting...")
            found_frame.ref_count += 1
            self.promote(found_gen_num, found_frame)
        else:
            # 不存在於gen中，是新的Frame，插入到gen[2]
            print("Firstly accessed, Adding to Gen 2...")
            new_frame = Frame(frame_number)
            new_frame.ref_count += 1
            self.gens[2].insert(0, new_frame)

        # 收尾整理所有的gen然後輸出檢視
        self.handle_gens_overflow()
        self.print_gens()


    def search(self, frame_number):
        # 尋找特定框架，若找到則返回
        for gen_num, gen in self.gens.items():
            for f in gen:
                if f.frame_number == frame_number:
                    return gen_num, f
        return None, None


    def promote(self, cur_gen_num, frame):
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


    def handle_gens_overflow(self):
        # 處理每代的溢出情況，進行框架的遷移或淘汰
        for i in range(1, self.num_gens + 1):
            while len(self.gens[i]) > self.gen_size:
                oldest_frame = self.gens[i].pop()
                if i == self.num_gens:
                    # 已經是最底層，直接置換掉
                    self.evict_cnt += 1
                    print(f"Evicted: {oldest_frame}")
                else:
                    # 往下層移動
                    oldest_frame.age_gen += 1
                    self.gens[i+1].insert(0, oldest_frame)


    def print_gens(self):
        # 打印當前所有代的狀態
        print("\n")
        for gen_num, gen in self.gens.items():
            print(f"Gen {gen_num}:")
            for f in gen:
                print(f"\t{f}")
        print("-------------------------------------------------------------")




# Example usage
mglru = MGLRU()
test_sequence = [1, 2, 3, 4, 5, 6, 7, 8, 8, 7, 7, 6,   7,7]
for frame_number in test_sequence:
    mglru.access(frame_number)
