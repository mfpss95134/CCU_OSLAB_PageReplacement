#include <iostream>
#include <unordered_map>
#include <list>
using namespace std;

class LRUCache
{
private:
    int capacity;
    unordered_map<int, pair<int, list<int>::iterator>> cache;
    list<int> lru;

    void touch(int key)
    {
        lru.erase(cache[key].second);
        lru.push_front(key);
        cache[key].second = lru.begin();
    }

public:
    LRUCache(int capacity) : capacity(capacity) {}

    int get(int key)
    {
        if (cache.find(key) != cache.end())
        {
            touch(key);
            return cache[key].first;
        }
        return -1;
    }

    void put(int key, int value)
    {
        if (cache.find(key) != cache.end())
        {
            touch(key);
        }
        else
        {
            if (cache.size() == capacity)
            {
                cache.erase(lru.back());
                lru.pop_back();
            }
            lru.push_front(key);
        }
        cache[key] = {value, lru.begin()};
    }
};

int main()
{
    LRUCache lruCache(2);
    lruCache.put(1, 1);
    lruCache.put(2, 2);
    cout << lruCache.get(1) << endl; // returns 1
    lruCache.put(3, 3);              // evicts key 2
    cout << lruCache.get(2) << endl; // returns -1 (not found)
    lruCache.put(4, 4);              // evicts key 1
    cout << lruCache.get(1) << endl; // returns -1 (not found)
    cout << lruCache.get(3) << endl; // returns 3
    cout << lruCache.get(4) << endl; // returns 4
    return 0;
}