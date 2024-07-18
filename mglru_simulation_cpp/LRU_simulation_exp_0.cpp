#include<iostream>
using namespace std;


typedef struct node
{
    int loaded;   //记录该物理块存储的页面
    int time;     //记录该物理块没有被使用的时间
} page;


const int MAXSIZE=1000;//定义最大页面数
const int NUM=3;//定义页框数（物理块数）
page pages[NUM];  //定义页框表 （物理块表）
int queue[MAXSIZE];
int QUEUE_NUM;


//初始化结构函数
void initialize()
{
    for(int i=0; i<NUM; i++)
        pages[i].loaded=-1;

    for(int i=0; i<MAXSIZE; i++)
        queue[i]=-1;
    
    QUEUE_NUM=0;
}


//读入页面流
void read_data()
{
    /*
    char fname[20];
    cout<<"请输入页面流文件名:";
    cin>>fname;
    */
    FILE *fp;
    if((fp=fopen("./data copy 2.txt", "r"))==NULL)
    {
        cout << "[ERROR] Cannot open data.txt..." << endl;
    }
    else
    {
        while(!feof(fp))
        {
            fscanf(fp,"%d ",&queue[QUEUE_NUM]);
            QUEUE_NUM++;
        }
    }

    cout << "[INFO] Read from data.txt: " << endl;
    for(int i=0; i<QUEUE_NUM; i++)
    {
        cout << queue[i] << " ";
    }
}


void addTime(){
    for(int i=0;i<NUM;i++){
        pages[i].time++;
    }
}


int findPageByLRU(){
    int i = 0;
    for(int j = 1;j < NUM; j++){
        if (pages[i].time < pages[j].time){
            i = j;
        }
    }
    return i;
}


//最近最少使用调度算法（LRU）
void LRU()
{
    int i,flag;
    int absence=0;  //记录缺页次数
    cout<<endl<<"----------------------------------------------------"<<endl;
    cout<<"最近最少使用调度算法（LRU）页面调出流:";
    for(i=0;i<NUM;i++)  //前3个进入内存的页面
    {
        pages[i].loaded=queue[i];
        pages[i].time=NUM-i;
    }
    absence=3;
    for(i=NUM; i<QUEUE_NUM; i++)
    {
        int j;
        flag=0;
        for(j=0;j<NUM;j++)  //判断当前需求的页面是否在内存
        {
            if(pages[j].loaded==queue[i])
            {
                flag=1;
                break;
            }
        }
        if(flag==0)
        {
            j = findPageByLRU();
            cout<<pages[j].loaded<<" ";
            pages[j].loaded=queue[i];
            absence++;
        }
        pages[j].time=0;

        addTime();
    }
    cout<<endl<<"总缺页数:"<<absence<<endl;
}




int main()
{
    cout<<"     /***********虚拟存储管理器的页面调度***********/"<<endl;
    initialize();
    read_data();
    LRU();

    return 0;
}