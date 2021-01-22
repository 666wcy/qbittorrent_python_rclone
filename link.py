#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

def mkdir(path):
    # 引入模块
    import os

    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)

    # 判断结果
    if not isExists:
        os.makedirs(path)

        print (path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (path+' 目录已存在')
        return False

def creat_link(dir,to_dir):
    mkdir(to_dir)

    to_dir = to_dir.rstrip('\\')
    to_dir = to_dir.rstrip('/')

    dir = dir.rstrip('\\')
    dir = dir.rstrip('/')

    command=f"cp -l \"{dir}\" \"{to_dir}\" -R"
    print(command)
    os.system(command)

    print( "创建硬链接成功!!")