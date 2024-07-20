import time
import os


class Frame:
    def __init__(self, frame_number):
        self.frame_number = frame_number  # 頁框編號
        self.ref_count    = 0             # 訪問次數
        self.last_access_time = None
        self.next_access_time = 0
        self.predicted_delta  = None

    def __eq__(self, other):
        #return self.frame_number == other.frame_number if isinstance(other, Frame) else False
        return isinstance(other, Frame) and self.frame_number == other.frame_number

    def __lt__(self, other):
        return self.next_access_time < other.next_access_time

    def __hash__(self):
        return hash(self.frame_number)

    def __repr__(self):
        #return f"Frame({hex(self.frame_number)}, ref_cnt:{self.ref_count})"
        return f"Frame({hex(self.frame_number)})"

    def evaluate_next_access_time(self, alpha=0.5):
        cur_time = float(time.time())
        
        if self.last_access_time is None:
            self.last_access_time = cur_time
            return
        
        actual_delta = cur_time - self.last_access_time
        self.last_access_time = cur_time
        
        # Predict the next access time based on the smoothed time delta
        if self.predicted_delta is None:
            self.predicted_delta = actual_delta
        else:
            self.predicted_delta = alpha * self.predicted_delta + (1 - alpha) * actual_delta
        
        self.next_access_time = cur_time + self.predicted_delta
        return




class SetAssociativeCache:
    def __init__(self, num_sets: int, num_ways: int):
        self.num_sets = num_sets
        self.num_ways = num_ways
        self.capacity = num_sets * num_ways
        self.sets = {i: [] for i in range(num_sets)}


    def ins(self, frame: Frame):
        set_idx = frame.frame_number % self.num_sets
        tgt_set = self.sets[set_idx]
        tgt_set.insert(0, frame)
        return


    def rmv(self, frame: Frame):
        set_idx = frame.frame_number % self.num_sets
        tgt_set = self.sets[set_idx]
        for f in tgt_set:
            if f == frame:
                tgt_set.remove(f)
        return


    def fnd(self, frame: Frame): #暫時沒用
        set_idx = frame.frame_number % self.num_sets
        tgt_set = self.sets[set_idx]

        for f in tgt_set:
            if f == frame:
                return f
        return None


    def mv_to_head(self, frame: Frame):
        set_idx = frame.frame_number % self.num_sets
        tgt_set = self.sets[set_idx]

        for f in tgt_set:
            if f == frame:
                tgt_set.remove(f)
                tgt_set.insert(0, f)
                return f
        return None


    def rmv_old_frames(self):
        old_frames = []
        for set_idx, tgt_set in self.sets.items():
            while len(tgt_set) > self.num_ways:
                old_frames.append(tgt_set.pop())
        return old_frames




class RBTree:
    class Node:
        def __init__(self, frame, color='black', nil=None):
            self.frame = frame
            self.color = color
            self.left = self.right = self.parent = nil if nil is None else nil
    def __init__(self):
        self.nil = self.Node(None)
        self.root = self.nil
        self.node_cnt = 0


    def ins(self, frame: Frame):
        node = self.Node(frame, 'red', self.nil)
        parent = self.nil
        current = self.root
        while current != self.nil:
            parent = current
            if frame < current.frame:
                current = current.left
            else:
                current = current.right

        node.parent = parent
        if parent == self.nil:
            self.root = node
        elif frame < parent.frame:
            parent.left = node
        else:
            parent.right = node

        self.ins_fix(node)
        self.node_cnt +=1 #++


    def rmv(self, frame: Frame): #移除包含frame的紅黑樹節點
        z = self.fnd(frame)
        if z is None:
            return  # Node not found
        y = z
        y_original_color = y.color
        if z.left == self.nil:
            x = z.right
            self.tsp(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self.tsp(z, z.left)
        else:
            y = self.min(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.tsp(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.tsp(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 'black':
            self.rmv_fix(x)
        self.node_cnt -=1 #--


    def ins_fix(self, node):
        while node != self.root and node.parent.color == 'red':
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color == 'red':
                    node.parent.color = 'black'
                    uncle.color = 'black'
                    node.parent.parent.color = 'red'
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.rotate_left(node)
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    self.rotate_right(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.color == 'red':
                    node.parent.color = 'black'
                    uncle.color = 'black'
                    node.parent.parent.color = 'red'
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.rotate_right(node)
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    self.rotate_left(node.parent.parent)
        self.root.color = 'black'


    def rmv_fix(self, x):
        while x != self.root and x.color == 'black':
            if x == x.parent.left:
                w = x.parent.right
                if w.color == 'red':
                    w.color = 'black'
                    x.parent.color = 'red'
                    self.rotate_left(x.parent)
                    w = x.parent.right
                if w.left.color == 'black' and w.right.color == 'black':
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.right.color == 'black':
                        w.left.color = 'black'
                        w.color = 'red'
                        self.rotate_right(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = 'black'
                    w.right.color = 'black'
                    self.rotate_left(x.parent)
                    x = self.root
            else:
                # Symmetric to the above code for the left side
                w = x.parent.left
                if w.color == 'red':
                    w.color = 'black'
                    x.parent.color = 'red'
                    self.rotate_right(x.parent)
                    w = x.parent.left
                if w.right.color == 'black' and w.left.color == 'black':
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.left.color == 'black':
                        w.right.color = 'black'
                        w.color = 'red'
                        self.rotate_left(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = 'black'
                    w.left.color = 'black'
                    self.rotate_right(x.parent)
                    x = self.root
        x.color = 'black'


    def tsp(self, u, v):
        if u.parent == self.nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent


    def min(self, x):
        if x.frame is None:
            return x  # 或其他適當的處理方式，如拋出錯誤
        while x.left != self.nil:
            x = x.left
        return x


    def max(self): #用來找LRU_node的，寫法和min稍有不同
        cur_node = self.root
        if cur_node == self.nil:
            return None  # 樹是空的
        while cur_node.right != self.nil:
            cur_node = cur_node.right
        return cur_node



    def fnd(self, frame: Frame): #找到包含frame的紅黑樹節點
        cur_node = self.root
        while cur_node != self.nil:
            if cur_node.frame == frame:
                return cur_node
            elif cur_node.frame > frame:
                cur_node = cur_node.left
            else:
                cur_node = cur_node.right
        return None


    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y


    def rotate_right(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.nil:
            x.right.parent = y
        x.parent = y.parent
        if y.parent == self.nil:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x


    # 遞迴計算節點數量，太費時了，不使用
    def count_nodes(self, node=None):
        if node is None:
            node = self.root
        if node == self.nil:
            return 0
        return 1 + self.size(node.left) + self.size(node.right)


    def print_tree(self):
        def in_order_traversal(node):
            if node != self.nil:
                in_order_traversal(node.left)
                print("\t" + node.frame.__repr__() + f":{node.frame.next_access_time}")
                in_order_traversal(node.right)
        in_order_traversal(self.root)
        ##print(f"Node_cnt: {self.node_cnt}")




class MyCache:
    def __init__(self):
        self.layer0 = []                         # 第0層：過濾層，用來過濾掉那些短時間內只會存取一次的Frame
        self.layer1 = SetAssociativeCache(4, 8)  # 第1層：主要的記錄層，用來快速搜尋用的
        self.layer2 = RBTree()                   # 第2層：
        self.swap   = []                         # Swap Space：滿了之後要丟到這裡面來
        self.swapout_cnt = 0      # 換出次數(swap out次數)
        self.refault_cnt = 0      # 


    def access(self, frame_number):
        cur_time = float(time.time())
        print(f"Accessing Frame:{hex(frame_number)}", end=f', Time:{cur_time}\n')

        found_layer, found_frame = self.search(frame_number)
        #found_frame.ref_count += 1
        #found_frame.last_access_time = cur_time
        if found_layer == 0:
            # 已在第0層，移動到下一層
            found_frame.ref_count += 1
            found_frame.last_access_time = cur_time

            print(f"{found_frame} Found in Layer 0, Moving to Layer 1...")
            self.layer0.remove(found_frame)
            self.layer1.ins(found_frame)
        elif found_layer == 1:
            # 已在第1層某set中
            found_frame.ref_count += 1
            found_frame.last_access_time = cur_time
            # 移動到所在set的頭部
            print(f"{found_frame} Found in Layer 1, Updating to Head...")
            self.layer1.mv_to_head(found_frame)
        elif found_layer == 2:
            # 已在第2層，
            found_frame.ref_count += 1
            found_frame.last_access_time = cur_time
            # 用"指數平滑"估算Frame下一次被存取的時間，計算完後應該要調整紅黑數的平衡
            l2_root = self.layer2.root
            l2_min_node = self.layer2.min(l2_root)
            if found_frame == l2_min_node.frame:
                #紅黑樹中，最近期會被存取的
                print(f"{found_frame} Found in Layer 2, Promoting to Layer 1...")
                self.layer2.rmv(found_frame)
                self.layer1.ins(found_frame)
            else:
                print(f"{found_frame} Found in Layer 2, Evaluating next access time...")
                self.layer2.rmv(found_frame)
                found_frame.evaluate_next_access_time()
                self.layer2.ins(found_frame)
        elif found_layer == 3:
            # 已在swap中，代表太久沒被使用，所以被踢出到swap去了
            found_frame.ref_count += 1
            found_frame.last_access_time = cur_time
            # 重新加入到第1層
            print(f"{found_frame} Found in Swap, Promoting to Layer 1...")
            self.swap.remove(found_frame)
            self.layer1.ins(found_frame)
            self.refault_cnt += 1
        else:
            # 不在任一層，第一次被存取，加入到第0層
            print("Firstly accessed, Adding to Layer 0...")
            new_frame = Frame(frame_number)
            new_frame.ref_count += 1
            new_frame.last_access_time = cur_time
            self.layer0.insert(0, new_frame)


        # 檢查第0層有沒有多餘的Frame，有的話就捨棄掉
        while len(self.layer0) > (100 - self.layer1.capacity): #限制容量為100，多餘的就捨棄掉
            self.layer0.pop()
        # 檢查第1層有沒有多餘的Frame，有的話把多餘的移出來放到第2層
        old_frames = self.layer1.rmv_old_frames()
        for f in old_frames:
            f.evaluate_next_access_time()
            self.layer2.ins(f)
        # 檢查第2層有沒有多餘的Frame，有的話就丟到swap去（相當於Swap Out）
        while self.layer2.node_cnt > 824:
            LRU_node = self.layer2.max()
            self.layer2.rmv(LRU_node.frame)
            self.swap.append(LRU_node.frame)
            self.swapout_cnt += 1
            print(f"Swapped out: {LRU_node.frame}")
        # 最後收尾印出來
        print("\n")
        self.print_layers()
        print("------------------------------------------------------------------------------------------------------------------------")
        #time.sleep(2)  #模擬存取延遲，不然測試估計的存取時間看起來會不明顯
        return


    def search(self, frame_number):
        # 在layer0搜尋到
        for f in self.layer0:
            if f.frame_number == frame_number:
                return 0, f
        # 在layer1搜尋到
        set_idx = frame_number % self.layer1.num_sets
        tgt_set = self.layer1.sets[set_idx]
        for f in tgt_set:
            if f.frame_number == frame_number:
                return 1, f
        # 在layer2搜尋到
        found_node = self.layer2.fnd(Frame(frame_number))
        if found_node:
            return 2, found_node.frame
        # 在swap搜尋到
        for f in self.swap:
            if f.frame_number == frame_number:
                return 3, f
        # 搜尋不到
        return None, None
        """
        cur_node = self.layer2.root
        while cur_node != self.layer2.nil:
            if cur_node.frame.frame_number == frame_number:
                return 2, cur_node.frame
            if cur_node.frame.frame_number < frame_number: #不知道為什麼比較邏輯要相反才正確
                cur_node = cur_node.left
            else:
                cur_node = cur_node.right
        """
        

    def print_layers(self):
        print("Layer 0:")
        print(f"\t{self.layer0}")
        print("Layer 1:")
        for set_idx, frames in self.layer1.sets.items():
            print(f"\tSet #{set_idx}: {frames}")
        print("Layer 2:")
        self.layer2.print_tree()
        print(f"Swap: {self.swap}")
        return




# Example usage
cache = MyCache()
test_sequence = [1, 5, 9, 13, 17, 21, 25, 29, 1, 5, 1, 9, 13, 17, 21, 25, 29, 33, 33, 37, 37, 1,5,1,5,1,5 ,13,13,13,13,13 ,17]
for frame_number in test_sequence:
    cache.access(frame_number)


print("------------------------------------------------------------------------------------------------------------------------")
print(f"SWAP_OUT: {cache.swapout_cnt}")
print(f" REFAULT: {cache.refault_cnt}")