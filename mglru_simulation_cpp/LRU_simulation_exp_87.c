#include <stdio.h>
#include <stdlib.h>
int GEN_NUM = 4;       // 有幾代
int LIST_SLOT_NUM = 8; // 每代(個)List有幾格
struct node *LRU_List = NULL;
struct node *mgLRU_List = NULL;
int TEST_QUEUE[1024];   // 測試資料
int TEST_QUEUE_NUM = 0; // 有幾筆測試資料

typedef struct node // 一個page
{
    int phy_addr;
    int vir_addr; /*這裡應該是要用成list或陣列，之後再改*/
    int ref_time;

    struct node *prev;
    struct node *next;
} node_t;

typedef struct page_item // 一個page
{
    int phy_addr;
    int vir_addr; /*這裡應該是要用成list或陣列，之後再改*/
    int ref_time;

    page_item_t *prev;
    page_item_t *next;
} page_item_t;

void init_lru_list()
{
    LRU_List = (node_t *)malloc(LIST_SLOT_NUM * sizeof(node_t));
    return;
}

void init_mglru_list()
{
    mgLRU_List = (node_t *)malloc(GEN_NUM * LIST_SLOT_NUM * sizeof(node_t));
    return;
}

node_t *search_from_lru_list(int phy_addr)
{
    for (int i = 0; i < LIST_SLOT_NUM; i++)
    {
        if (LRU_List[i].phy_addr == phy_addr)
        {
            return &LRU_List[i];
        }
    }

    return NULL;
}

node_t *search_from_mglru_list(int phy_addr)
{
    for (int i = 0; i < GEN_NUM * LIST_SLOT_NUM; i++)
    {
        if (mgLRU_List[i].phy_addr == phy_addr)
        {
            return &mgLRU_List[i];
        }
    }

    return NULL;
}

node_t *search_from_list(node_t *list, int target)
{
    node_t *cursor = list;
    while (cursor != NULL)
    {
        if (cursor->phy_addr == target)
        {
            return cursor;
        }

        cursor = cursor->next;
    }

    return NULL;
}

void add_to_list(node_t **list, node_t *new_node)
{
    new_node->prev = NULL;
    new_node->next = *list;
    if (*list != NULL)
        (*list)->prev = new_node;
    *list = new_node;
    // printf("%d added to list. \n", new_node->phy_addr);

    return;
}

void del_from_list(node_t **list, node_t *del_node)
{
    // 先檢查被刪除的node是否剛好是第一個
    if (*list == del_node)
    {
        *list = del_node->next;
    }

    if (del_node->next != NULL) // 檢查下一個node是否存在
    {
        del_node->next->prev = del_node->prev;
    }
    if (del_node->prev != NULL) // 檢查上一個node是否存在
    {
        del_node->prev->next = del_node->next;
    }

    free(del_node);

    return;
}

void read_test_queue_data()
{
    FILE *fp;
    if ((fp = fopen("./data.txt", "r")) == NULL)
    {
        printf("[ERROR] Cannot open data.txt.\n\n\n");
    }
    else
    {
        while (!feof(fp))
        {
            fscanf(fp, "%d ", &TEST_QUEUE[TEST_QUEUE_NUM]);
            //
            node_t *tmp_node = (node_t *)malloc(sizeof(node_t));
            tmp_node->phy_addr = TEST_QUEUE[TEST_QUEUE_NUM];
            add_to_list(&LRU_List, tmp_node);
            // add_to_list(&mgLRU_List, tmp_node);
            //
            TEST_QUEUE_NUM++;
        }
    }

    return;
}

void debug_info()
{
    printf("\n==========================================\n\n");

    printf("[INFO] data.txt: ");
    for (int i = 0; i < TEST_QUEUE_NUM; i++)
    {
        printf("%d, ", TEST_QUEUE[i]);
    }
    printf("\n\n");

    printf("[INFO] LRU_List: ");
    node_t *cursor = LRU_List;
    while (cursor != NULL)
    {
        printf("%d, ", cursor->phy_addr);
        cursor = cursor->next;
    }
    printf("\n\n");

    printf("==========================================\n\n");

    return;
}

int main()
{
    /*
        初始化要用到的資料
    */
    // init_lru_list();
    // init_mglru_list();
    read_test_queue_data();
    debug_info();

    return 0;
}