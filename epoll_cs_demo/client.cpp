#include "common.h"


// IO多路复用epoll
void start_epoll(int client_fd);
// 操作epoll的描述符监控情况
void epoll_control(int epoll_fd, int mode, int fd, int state);
// 事件处理函数
void handle_events(int epoll_fd, struct epoll_event *events, int num, int client_fd, char *buffer);
// 处理读数据
void do_read(int epoll_fd, int fd, int client_fd, char *buffer);



int main(int argc, char *argv[])
{
    // 创建客户端套接字
    int client_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (-1 == client_fd)
    {
        printf("<client>create client socket error!\n");
        exit(1);
    }

    // 设置服务器IP和Port
    struct sockaddr_in server_addr;
    bzero(&server_addr, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(SERVER_PORT);
    inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr);

    // 开始连接
    if (-1 == connect(client_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)))
    {
        printf("<client>connect server error!\n");
        exit(1);
    }
    else
    {
        printf("<client>client[%d] connect server success!\n", client_fd);
    }

    // 开启IO多路复用
    start_epoll(client_fd);

    close(client_fd);
    return 0;
}

void start_epoll(int client_fd)
{
    struct epoll_event wait_events[WAIT_EVENT_NUM];
    char buffer[BUFFER_SIZE] = {0};
    int event_count;

    // 创建一个epoll操作的文件描述符
    int epoll_fd = epoll_create(EPOLL_SIZE);
    // 监控标准输入的事件
    epoll_control(epoll_fd, EPOLL_CTL_ADD, STDIN_FILENO, EPOLLIN);
    // 经停服务器消息
    epoll_control(epoll_fd, EPOLL_CTL_ADD, client_fd, EPOLLIN);
    while(true)
    {
        // 等待准备好的描述符事件
        event_count = epoll_wait(epoll_fd, wait_events, WAIT_EVENT_NUM, -1);
        handle_events(epoll_fd, wait_events, event_count, client_fd, buffer);
    }
    close(epoll_fd);
}

void epoll_control(int epoll_fd, int mode, int fd, int state)
{
    struct epoll_event ev;
    ev.events = state;
    ev.data.fd = fd;
    epoll_ctl(epoll_fd, mode, fd, &ev);
}

void handle_events(int epoll_fd, struct epoll_event *events, int num, int client_fd, char *buffer)
{
    for (int count = 0; count < num; count++)
    {
        int socket_fd = events[count].data.fd;
        if (events[count].events & EPOLLIN)
            do_read(epoll_fd, socket_fd, client_fd, buffer);
    }
}

void do_read(int epoll_fd, int fd, int client_fd, char *buffer)
{
    int read_count = read(fd, buffer, BUFFER_SIZE);
    if (-1 == read_count)
    {
        printf("<client>read server msg error!\n");
        close(fd);
        epoll_control(epoll_fd, EPOLL_CTL_DEL, fd, EPOLLIN);
    }
    else if (0 == read_count)
    {
        printf("<client>client[%d] close, no data!\n", fd);
        close(fd);
        //epoll_control(epoll_fd, EPOLL_CTL_DEL, fd, EPOLLIN);
        printf("<client>server closed, client to exit!\n");
        exit(1);
    }
    else
    {
        buffer[read_count] = '\0';
        if (fd == STDIN_FILENO)
        {
            int write_count = write(client_fd, buffer, strlen(buffer));
            if (-1 == write_count)
            {
                printf("<client>client[%d] write error!\n", client_fd);
                close(client_fd);
                epoll_control(epoll_fd, EPOLL_CTL_DEL, client_fd, EPOLLIN);
            }
        }
        else
        {
            printf("<client>receive server response:%s", buffer);
        }
    }
}