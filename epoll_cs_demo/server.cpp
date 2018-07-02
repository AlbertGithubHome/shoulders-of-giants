#include "common.h"


// IO多路复用epoll
void start_epoll(int listen_fd);
// 操作epoll的描述符监控情况
void epoll_control(int epoll_fd, int mode, int fd, int state);
// 事件处理函数
void handle_events(int epoll_fd, struct epoll_event *events, int num, int listen_fd, char *buffer);
// 处理新的客户端接入
void do_accpet(int epoll_fd, int listen_fd);
// 处理读数据
void do_read(int epoll_fd, int fd, char *buffer);
// 处理客户端断开连接
void do_disconnect(int epoll_fd, int fd);
// 处理客户端出错
void do_error(int epoll_fd, int fd);



int main(int argc, char * argv[])
{
    // 创建服务器套接字
    struct sockaddr_in server_addr;
    int listen_fd = socket(AF_INET,SOCK_STREAM,0);
    if (-1 == listen_fd)
    {
        printf("<server>create server socket error!\n");
        exit(1);
    }

    // 设置服务器IP和Port
    bzero(&server_addr, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr);
    server_addr.sin_port = htons(SERVER_PORT);

    // 绑定套接字
    if (-1 == bind(listen_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)))
    {
        printf("<server>bind server socket error!\n");
        exit(1);
    }

    // 监听套接字
    listen(listen_fd, LISTEN_NUM);
    printf("<server>server[ip:%s, port:%d] is running...\n", SERVER_IP, SERVER_PORT);

    // 开始IO多路复用
    start_epoll(listen_fd);
    return 0;
}

void start_epoll(int listen_fd)
{
    struct epoll_event wait_events[WAIT_EVENT_NUM];
    char buffer[BUFFER_SIZE] = {0};
    int event_count;

    // 创建一个epoll操作的文件描述符
    int epoll_fd = epoll_create(EPOLL_SIZE);
    // 查看监听描述符是否有新客户端连接
    epoll_control(epoll_fd, EPOLL_CTL_ADD, listen_fd, EPOLLIN);
    while(true)
    {
        // 等待准备好的描述符事件
        event_count = epoll_wait(epoll_fd, wait_events, WAIT_EVENT_NUM, -1);
        handle_events(epoll_fd, wait_events, event_count, listen_fd, buffer);
    }
}

void epoll_control(int epoll_fd, int mode, int fd, int state)
{
    struct epoll_event ev;
    ev.events = state;
    ev.data.fd = fd;
    epoll_ctl(epoll_fd, mode, fd, &ev);
}

void handle_events(int epoll_fd, struct epoll_event *events, int num, int listen_fd, char *buffer)
{
    for (int count = 0; count < num; count++)
    {
        int socket_fd = events[count].data.fd;
        if (events[count].events & EPOLLIN)
        {
            if (socket_fd == listen_fd)
                do_accpet(epoll_fd, socket_fd);
            else
                do_read(epoll_fd, socket_fd, buffer);
        }
        else if (events[count].events & EPOLLHUP)
            do_disconnect(epoll_fd, socket_fd);
        else if (events[count].events & EPOLLERR)
            do_error(epoll_fd, socket_fd);
    }
}

void do_accpet(int epoll_fd, int listen_fd)
{
    struct sockaddr_in client_addr;
    socklen_t  client_addr_len;
    int client_fd = accept(listen_fd, (struct sockaddr*)&client_addr, &client_addr_len);
    if (-1 == client_fd)
    {
        printf("<server>accpet client error!\n");
    }
    else
    {
        printf("<server>accept a new client[%d]: %s:%d\n", client_fd, inet_ntoa(client_addr.sin_addr), client_addr.sin_port);
        epoll_control(epoll_fd, EPOLL_CTL_ADD, client_fd, COMMON_EP_EVENT);
    }
}

void do_read(int epoll_fd, int fd, char *buffer)
{
    int read_count = read(fd, buffer, BUFFER_SIZE);
    if (-1 == read_count)
    {
        printf("<server>read client [%d] msg error!\n", fd);
        close(fd);
        epoll_control(epoll_fd, EPOLL_CTL_DEL, fd, COMMON_EP_EVENT);
    }
    else if (0 == read_count)
    {
        printf("<server>client [%d] close, no data!\n", fd);
        close(fd);
        epoll_control(epoll_fd, EPOLL_CTL_DEL, fd, COMMON_EP_EVENT);
    }
    else
    {
        // 收到消息后反馈到客户端
        buffer[BUFFER_SIZE] = '\0';
        printf("<server>receive message is : %s\n", buffer);
        int write_count = write(fd, buffer, strlen(buffer));
        if (-1 == write_count)
        {
            printf("<server>response to client[%d] error!\n", fd);
            close(fd);
            epoll_control(epoll_fd, EPOLL_CTL_DEL, fd, COMMON_EP_EVENT);
        }
    }
}

void do_disconnect(int epoll_fd, int fd)
{
    printf("<server>client[%d] disconnect!\n", fd);
    close(fd);
    epoll_control(epoll_fd, EPOLL_CTL_DEL, fd, COMMON_EP_EVENT);
}

void do_error(int epoll_fd, int fd)
{
    printf("<server>client[%d] error!\n", fd);
    close(fd);
    epoll_control(epoll_fd, EPOLL_CTL_DEL, fd, COMMON_EP_EVENT);
}