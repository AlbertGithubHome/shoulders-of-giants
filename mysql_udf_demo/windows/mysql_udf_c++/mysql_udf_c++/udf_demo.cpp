#include <winsock.h>
#include <mysql.h>  

extern "C" {
	__declspec(dllexport) long long udf_add(UDF_INIT *initid, UDF_ARGS *args, char *is_null, char *error)  
	{  
		long long a = *((long long *)args->args[0]);  
		long long b = *((long long *)args->args[1]);  
		return a + b;  
	}  

	__declspec(dllexport) my_bool udf_add_init(UDF_INIT *initid, UDF_ARGS *args, char *message)  
	{  
		return 0;  
	}  

}