# 源文件目录
aux_source_directory(. DIR_SRCS)

# 设置环境变量，编译用到的源文件全部都要放到这
set(TEST_CMAKE ${DIR_SRCS})

# 库文件目录
link_directories(lib)

# 头文件目录
include_directories(
    ${RootDir}/myadd
    ${RootDir}/mysub
)

# 指定子目录
add_subdirectory(myadd)
add_subdirectory(mysub)

# 设置输出目录
SET(EXECUTABLE_OUTPUT_PATH ${OutDir})

message(${OutDir})

# 添加要编译的可执行文件
add_executable(${PROJECT_NAME} ${TEST_CMAKE})

# 添加可执行文件所需要的库
target_link_libraries(${PROJECT_NAME} myadd)
target_link_libraries(${PROJECT_NAME} mysub)








