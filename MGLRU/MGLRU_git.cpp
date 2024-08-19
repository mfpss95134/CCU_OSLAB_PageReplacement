#include <iostream>
#include <list>
#include <unordered_map>
#include <vector>

class LRUCache {
private:
    struct CacheNode {
        unsigned int key;
    };

    int capacity;
    std::list<CacheNode> cacheList;
    std::unordered_map<unsigned int, std::list<CacheNode>::iterator> cacheMap;

public:
    LRUCache(int capacity) : capacity(capacity) {}

    int get(unsigned int key) {
        if (cacheMap.find(key) == cacheMap.end()) {
            return -1;
        } else {
            cacheList.splice(cacheList.begin(), cacheList, cacheMap[key]);
            return cacheMap[key]->key;
        }
    }

    void put(unsigned int key) {
        if (cacheMap.find(key) != cacheMap.end()) {
            cacheList.splice(cacheList.begin(), cacheList, cacheMap[key]);
            return;
        }

        if (cacheList.size() == capacity) {
            unsigned int lastKey = cacheList.back().key;
            cacheList.pop_back();
            cacheMap.erase(lastKey);
        }

        cacheList.push_front(CacheNode{key});
        cacheMap[key] = cacheList.begin();
    }

    unsigned int evict() {
        unsigned int lastKey = cacheList.back().key;
        cacheList.pop_back();
        cacheMap.erase(lastKey);
        return lastKey;
    }

    bool isFull() {
        return cacheList.size() >= capacity;
    }

    void display() {
        for (auto& node : cacheList) {
            std::cout << node.key << " ";
        }
        std::cout << "\n";
    }
};

class MGLRUCache {
private:
    std::vector<LRUCache> lrus;
    std::unordered_map<unsigned int, int> keyIndexMap;
    int length;
    int capacity;
    int hitCount = 0;
    int missCount = 0;

public:
    MGLRUCache(int length, int capacity) : length(length), capacity(capacity), lrus(length, LRUCache(capacity)) {}

    int get(unsigned int key) {
        if (keyIndexMap.find(key) != keyIndexMap.end()) {
            int idx = keyIndexMap[key];
            lrus[idx].get(key);
            hitCount++;
            balance();
            return key;
        } else {
            missCount++;
            put(key);
            return -1;
        }
    }

    void put(unsigned int key) {
        if (keyIndexMap.find(key) != keyIndexMap.end()) {
            int idx = keyIndexMap[key];
            lrus[idx].get(key);
        } else {
            lrus[0].put(key);
            keyIndexMap[key] = 0;
            balance();
        }
    }

    void balance() {
        for (int i = 0; i < length - 1; i++) {
            while (lrus[i].isFull()) {
                unsigned int evicted = lrus[i].evict();
                keyIndexMap.erase(evicted);
                lrus[i + 1].put(evicted);
                keyIndexMap[evicted] = i + 1;
            }
        }
    }

    void displayAllLRUs() {
        for (int i = 0; i < length; ++i) {
            std::cout << "LRU " << i << ": ";
            lrus[i].display();
        }
        std::cout << "-----------------\n";
    }

    void displayCounts() {
        std::cout << "Hits: " << hitCount << ", Misses: " << missCount << "\n";
    }
};

int main() {
    MGLRUCache mglru(4, 3);  // 4 LRUs, each with a capacity of 2
    mglru.get(1);
    mglru.get(2);
    mglru.get(3);
    mglru.get(4);
    mglru.get(5);
    mglru.displayAllLRUs();
    mglru.displayCounts();

    return 0;
}
