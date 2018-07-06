#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#include <netinet/in.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#include <sys/epoll.h>
#include <unistd.h>
#include <sys/types.h>

#define SERVER_IP       "192.168.1.214"
#define SERVER_PORT     8899
#define LISTEN_NUM      10

#ifdef __SERVER__
#define FD_MAX_SIZE     128
#else
#define FD_MAX_SIZE     4
#endif
#define BUFFER_SIZE     1024
//#define MSG_NOSIGNAL    0
#define STDIN_FILENO    0

