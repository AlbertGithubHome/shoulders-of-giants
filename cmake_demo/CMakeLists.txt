# 指定cmake版本
cmake_minimum_required(VERSION 3.5)

# 指定项目的名称，一般和项目的文件夹名称对应
project(testcmake)

# 设置根目录变量
set(RootDir ${PROJECT_SOURCE_DIR})

# 设置输出目录变量
set(OutDir ${PROJECT_SOURCE_DIR}/bin)

# 添加c++ 11标准支持
set(CMAKE_CXX_FLAGS "-std=c++11" )

# 头文件目录
include_directories(
    ${RootDir}/src/myadd
    ${RootDir}/src/mysub
)

# 库文件目录
link_directories(lib)

# 指定子目录
add_subdirectory(src)





