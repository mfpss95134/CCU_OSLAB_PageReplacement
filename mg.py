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
    def __init__(self, num_gens=5, gen_size=2):
        self.num_gens = num_gens  # 代數量
        self.gen_size = gen_size  # 每代大小
        self.evict_cnt = 0  # 淘汰數量計數
        self.gens = {i: [] for i in range(1, num_gens + 1)}  # 初始化每代

    def find(self, frame):
        # 尋找特定框架，若找到則返回
        for gen_idx, gen in self.gens.items():
            for f in gen:
                if f == frame:
                    return f
        return None

    def access(self, frame_number):
        # 處理框架的訪問
        frame = Frame(frame_number)
        found_frame = self.find(frame)
        
        if found_frame:
            # 已存在於gen中，是舊的Frame，往上層提升
            print(f"Accessing: {found_frame}")
            found_frame.ref_count += 1
            self.promote(found_frame)
        else:
            # 不存在於gen中，是新的Frame，插入到gen[3]
            print(f"Accessing: {frame}")
            frame.ref_count += 1
            self.gens[3].insert(0, frame)

        # 整理所有的gen然後輸出檢視
        self.handle_gen_overflow()
        self.print_gens()


    def promote(self, frame):
        current_gen_list = self.gens[frame.age_gen]
        idx = current_gen_list.index(frame)
        
        # 移動到所在層的頭部
        current_gen_list.insert(0, current_gen_list.pop(idx))

        # 檢查是否能往上層提升，如果可以的話就往上升
        if frame.age_gen > 1:
            current_gen_list.remove(frame) #從當前層移除
            frame.age_gen -= 1  #層數上升
            self.gens[frame.age_gen].append(frame) #附加到上層的尾部
            print(f"Promoted: {frame}")


    def handle_gen_overflow(self):
        # 處理每代的溢出情況，進行框架的遷移或淘汰
        for gen in range(1, self.num_gens + 1):
            while len(self.gens[gen]) > self.gen_size:
                oldest_frame = self.gens[gen].pop()
                if gen == self.num_gens:
                    # 已經是最底層，直接置換掉
                    self.evict_cnt += 1
                    print(f"Evicted: {oldest_frame}")
                else:
                    # 往下層移動
                    next_gen = gen + 1
                    oldest_frame.age_gen = next_gen
                    self.gens[next_gen].insert(0, oldest_frame)


    def print_gens(self):
        # 打印當前所有代的狀態
        print("\n")
        for gen, frames in self.gens.items():
            print(f"Gen {gen}:")
            for frame in frames:
                print(f"\t{frame}")
        print("-------------------------------------------------------------")




# 示例用法
mglru = MGLRU()
test_sequence = [1, 2, 3, 4, 5, 6, 7, 8, 8, 7, 7, 6]
for frame_number in test_sequence:
    mglru.access(frame_number)
