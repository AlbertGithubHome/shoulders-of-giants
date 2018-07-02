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
    return 0;
}