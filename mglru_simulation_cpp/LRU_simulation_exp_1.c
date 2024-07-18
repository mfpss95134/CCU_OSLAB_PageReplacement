#include<stdio.h>
#include<malloc.h>
//定义内存中最大的内存块的数量
const int MAX_BLOCK_NUM = 5;
//定义节点，block_id为内存块号，next为下一个节点的指针
typedef struct Node
{
    int block_id;
    struct Node *next;
}Node;


//定义链表头结点的指针
struct Node *List = NULL;
//定义链表中节点的数量
int BLOCK_NUM = 0;
//输入链表中的所有结点


void display()
{
    if(List == NULL)
        return;
    Node *p = NULL;
    p = List->next;
    while(p != NULL)
    {
        printf("%d ",p->block_id);
        p = p->next;
    }
}


//查询链表中是否存在id，若存在则返回id的序号，否则返回-1
int query(int id)
{
    if(List==NULL)
        return -1;
    Node *p = NULL;
    p = List->next;
    int num = -1;
    while(p != NULL)
    {
        num++;
        if(p->block_id == id)
            return num;
        p = p->next;
    }
    return -1;
}


//给定某节点的指针，如果不位null插入链表最前面，否则返回
void insertToFirst(struct Node *newnode)
{
    if(newnode == NULL || List == NULL)
        return;
    Node *p = NULL;
    p = List->next;
    List->next = newnode;
    List->next->next = p;
    BLOCK_NUM++;
}


//删除链表中最后的结点
void deleteLastNode()
{
    Node *p = NULL;
    p = List;
    while(p->next->next != NULL)
    {
        p = p->next;
    }
    free(p->next);
    p->next = NULL;
    BLOCK_NUM--;
}


//给定id(0<= id && id < MAX_BLOCK_NUM) 返回序号为id的节点的指针,并删除该结点，
Node* getNode(int id)
{
    Node *p = NULL;
    Node *node = NULL;
    p = List;
    int num = -2;
    //找到id对应结点的前一个节点，方便删除
    while(p != NULL)
    {
        num++;
        if(num == id -1)
            break;
       p = p->next;
    }
    //找到id对应节点
    node = p->next;
    //删除id对应节点
    p->next = p->next->next;
    //清除node—>next已存的信息；
    node->next = NULL;
    BLOCK_NUM--;
    return node;
}


//创建一个节点
Node* createNode(int block_id)
{
    Node *p = NULL;
    p = (Node*)malloc(sizeof(Node));
    p->block_id = block_id;
    p->next = NULL;
    return p;
}


void LRU()
{
    //创建链表
    List = createNode(0);
    //block_id 用于存放内存块号
    int block_id;
    //用于存放 block_id 对应的结点
    Node* block = NULL;
    while(1){
        printf("input the number of the block\n");
        scanf("%d",&block_id);
        block = createNode(block_id);
        //判断block是否在链表中；
        if(query(block_id) >= 0)
        {
            //存在该结点，则将获取该节点并移动到最前边；
            insertToFirst(getNode(query(block_id)));
            free(block);
        }
        else
        {
            //不存在该结点。将该节点插入链表最前边，并维护链表的长度为MAX_BLOCK_NUM
            insertToFirst(block);
            //维护链表的长度为MAX_BLOCK_NUM
            while(BLOCK_NUM > MAX_BLOCK_NUM)
                deleteLastNode();
        }
        block = NULL;
        printf("there are all the blocks：");
        display();
        putchar('\n');
        putchar('\n');
    }
}




int main(int argc, char* argv[])
{
    LRU();
    return 0;
}