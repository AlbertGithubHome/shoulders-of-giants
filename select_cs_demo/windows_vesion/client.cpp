#define __CLIENT__
#include "common.h"
// 参考：https://blog.csdn.net/dengyejing/article/details/678444
// windows上解决select不能同时等待键盘和套接字输入的问题

// IO多路复用select
void start_select(int client_fd);
// fd变化处理函数
void handle_fd_changed(fd_set *p_read_set, fd_set *p_error_set, int client_fd, char *buffer);
// 处理读数据
void do_read(int fd, int client_fd, char *buffer);
// 处理服务器断开连接
void do_disconnect(int fd);
// 启动监听输入的线程
void start_check_input_thread();
// 监听控制台输入的线程函数
DWORD WINAPI ThreadFunc(LPVOID hSemaphore);

// 中转输入的文件描述符
int input_fd = 0;


int main(int argc, char *argv[])
{
	WSADATA wsaData;
	WORD wVersionRequested = MAKEWORD( 2, 2 );
	if (WSAStartup(wVersionRequested, &wsaData) != 0)
	{
		printf("<server>we could not find a usable WinSock DLL.\n");
		exit(1);
	}

	start_check_input_thread();

	// 创建客户端套接字
	int client_fd = socket(AF_INET, SOCK_STREAM, 0);
	if (-1 == client_fd)
	{
		printf("<client>create client socket error!\n");
		exit(1);
	}

	// 设置服务器IP和Port
	struct sockaddr_in server_addr;
	memset(&server_addr, 0, sizeof(server_addr));
	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(SERVER_PORT);
	server_addr.sin_addr.s_addr	= inet_addr(SERVER_IP);
	//inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr);

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
	start_select(client_fd);

	closesocket(client_fd);
	return 0;
}

void start_select(int client_fd)
{
	char buffer[BUFFER_SIZE] = {0};
	int ready_count;
	fd_set read_set;
	fd_set error_set;

	while(true)
	{
		// 清空原描述符
		FD_ZERO(&read_set);
		FD_ZERO(&error_set);

		FD_SET(STDIN_FILENO, &read_set);
		FD_SET(STDIN_FILENO, &error_set);
		FD_SET(client_fd, &read_set);
		FD_SET(client_fd, &error_set);

		// windows 版本的第一个参数可忽略
		ready_count = select(0, &read_set, NULL, &error_set, NULL);
		if (ready_count > 0)
		{
			handle_fd_changed(&read_set, &error_set, client_fd, buffer);
		}
	}
}

void handle_fd_changed(fd_set *p_read_set, fd_set *p_error_set, int client_fd, char *buffer)
{
	if (FD_ISSET(client_fd, p_read_set))
	{
		do_read(client_fd, client_fd, buffer);
	}
	else if (FD_ISSET(client_fd, p_error_set))
	{
		do_disconnect(client_fd);
	}

	if (FD_ISSET(STDIN_FILENO, p_read_set))
	{
		do_read(STDIN_FILENO, client_fd, buffer);
	}
}

void do_read(int fd, int client_fd, char *buffer)
{
	int read_count = recv(fd, buffer, BUFFER_SIZE, MSG_NOSIGNAL);
	if (-1 == read_count)
	{
		printf("<client>read server msg error!\n");
		closesocket(fd);
		exit(1);
	}
	else if (0 == read_count)
	{
		printf("<client>client[%d] close, no data!\n", fd);
		printf("<client>server closed, client to exit!\n");
		closesocket(fd);
		exit(1);
	}
	else
	{
		buffer[read_count] = '\0';
		if (fd == STDIN_FILENO)
		{
			int write_count = send(client_fd, buffer, strlen(buffer), MSG_NOSIGNAL);
			if (-1 == write_count)
			{
				printf("<client>client[%d] write error!\n", client_fd);
				closesocket(client_fd);
				exit(1);
			}
		}
		else
		{
			printf("<client>receive server response:%s", buffer);
		}
	}
}

void do_disconnect(int fd)
{
	printf("<server>client[%d] disconnect!\n", fd);
	closesocket(fd);
	exit(1);
}

// 以下为windows客户端处理方案（解决select无法监听stdin）
DWORD WINAPI ThreadFunc(LPVOID hSemaphore)
{
	// 创建服务器套接字
	int listen_fd = socket(AF_INET, SOCK_STREAM, 0);
	if (-1 == listen_fd)
	{
		printf("<client>create server listen socket error!\n");
		exit(1);
	}

	/*一个端口释放后会等待两分钟之后才能再被使用, SO_REUSEADDR是让端口释放后立即就可以被再次使用。*/
	int reuse = 1;
	if (-1 == setsockopt(listen_fd, SOL_SOCKET, SO_REUSEADDR, (const char*)&reuse, sizeof(reuse)))
	{
		printf("<client>setsockopt option SO_REUSEADDR failed!\n");
		exit(1);
	}

	// 设置客户端中假服务器IP和Port
	struct sockaddr_in server_addr;
	memset(&server_addr, 0, sizeof(server_addr));
	server_addr.sin_family		= AF_INET;
	server_addr.sin_port		= htons(SEC_SER_PORT);
	server_addr.sin_addr.s_addr	= inet_addr("127.0.0.1");


	// 绑定套接字
	if (-1 == bind(listen_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)))
	{
		printf("<client>bind server socket error!\n");
		exit(1);
	}

	// 监听套接字
	listen(listen_fd, LISTEN_NUM);
	ReleaseSemaphore((HANDLE)hSemaphore, 1,  NULL);
	int conn_fd = accept(listen_fd, NULL, NULL);
	

	char buffer[BUFFER_SIZE] = {0};
	while(fgets(buffer, sizeof(buffer), stdin)) // 接收到控制台输入，发送给本地的客户端连接，触发select
	{
		send(conn_fd, buffer, strlen(buffer), MSG_NOSIGNAL);
	}

	return 0;
} 

void start_check_input_thread()
{
	HANDLE hSemaphore=CreateSemaphore(NULL, 0, 1, NULL);
	HANDLE hThread = CreateThread(NULL, 0,ThreadFunc, hSemaphore, 0, NULL);
	if(NULL == hThread)
	{
		printf("<client>CreateThread failed." );
		exit(1);
	}

	DWORD dwWaitResult = WaitForSingleObject(hSemaphore, INFINITE);
	switch (dwWaitResult)
	{
	case WAIT_OBJECT_0:
		printf("<client>stdin-sock is established!\n");
		break;
	default:
		printf("<client>wait the stdin-sock thread failed!\n");
		exit(1);
	}

	// 创建客户端套接字
	input_fd = socket(AF_INET, SOCK_STREAM, 0);
	if (-1 == input_fd)
	{
		printf("<client>create client check input socket error!\n");
		exit(1);
	}

	// 设置服务器IP和Port
	struct sockaddr_in server_addr;
	memset(&server_addr, 0, sizeof(server_addr));
	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(SEC_SER_PORT);
	server_addr.sin_addr.s_addr	= inet_addr("127.0.0.1");

	// 开始连接
	if (-1 == connect(input_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)))
	{
		printf("<client>connect self check input server error!\n");
		exit(1);
	}
	else
	{
		printf("<client>connect self check input server success!\n");
	}
}
