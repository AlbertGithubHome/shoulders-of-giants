aux_source_directory(. SRC_LIST)        #将此目录的源文件集合设置为变量SRC_LIST
add_library(mysub SHARED ${SRC_LIST})   #库的名称，库的类型，动态库的源文件列表

set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)  #库的输出路径为根目录下的lib文件夹