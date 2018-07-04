#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#include <WinSock2.h>
#pragma comment(lib, "ws2_32.lib")

/*
struct sockaddr_in: #include <WinSock2.h>
*/
extern int input_fd;

#define SERVER_IP       "192.168.1.105"
#define SERVER_PORT     8899
#define SEC_SER_PORT	8898	// 在本地启动一个假服务器，用于将控制台输入发送到本地客户端
#define LISTEN_NUM      10

#ifdef __SERVER__
#define FD_MAX_SIZE		128
#else
#define FD_MAX_SIZE		4
#endif
#define BUFFER_SIZE     1024
#define MSG_NOSIGNAL	0
#define STDIN_FILENO	input_fd

