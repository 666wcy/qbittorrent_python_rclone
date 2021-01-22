import os
from rename import *
'''重命名文件为emby格式要求'''

#获取文件夹下的子文件夹名和父文件夹绝对路径
def get_folder_name(dir):
    dirs = os.listdir( dir )
    print(dirs)
    # 输出所有文件和文件夹
    for file in dirs:
        print (file)
        print(os.path.join(dir, file))
        print(os.path.isdir(os.path.join(dir, file)))
        if os.path.isdir(os.path.join(dir, file))==True:
            return str(dir),str(file)

#重命名目录下子目录名称
def rename_folder(dir,newname):
    folder_dir,folder_name=get_folder_name(dir)  #获取文件夹名和父文件夹绝对路径
    print(folder_dir,folder_name)
    os.rename(os.path.join(folder_dir, folder_name), os.path.join(folder_dir,newname))

#遍历文件重命名
def rename_file(dir,season):
    dirs = os.listdir( dir)
    for file in dirs:
        if os.path.isfile(os.path.join(dir, file))==True:
            if season==2:
                newfile=edit_s2(str(file))
            elif season==3:
                newfile=edit_s3(str(file))
            elif season==4:
                newfile=edit_s4(str(file))
            else:
                newfile=edit_s1(str(file))
            print (file)
            print(newfile)
            if file != newfile:
                os.rename(os.path.join(dir, file), os.path.join(dir,newfile))

def start_rename(dir,season):
    if season==2:
        rename_folder(dir,"Season 02")
        folder_dir,folder_name=get_folder_name(dir)  #获取子文件夹名和父文件夹绝对路径
        folder_son=os.path.join(folder_dir, folder_name)
        print(folder_son)
        rename_file(folder_son,3)
    elif season==3:
        rename_folder(dir,"Season 03")
        folder_dir,folder_name=get_folder_name(dir)  #获取子文件夹名和父文件夹绝对路径
        folder_son=os.path.join(folder_dir, folder_name)
        print(folder_son)
        rename_file(folder_son,3)
    elif season==4:
        rename_folder(dir,"Season 04")
        folder_dir,folder_name=get_folder_name(dir)  #获取子文件夹名和父文件夹绝对路径
        folder_son=os.path.join(folder_dir, folder_name)
        print(folder_son)
        rename_file(folder_son,4)

    else:
        rename_folder(dir,"Season 01")
        folder_dir,folder_name=get_folder_name(dir)  #获取子文件夹名和父文件夹绝对路径
        folder_son=os.path.join(folder_dir, folder_name)
        print(folder_son)
        rename_file(folder_son,1)



if __name__ == '__main__':
    dir="E:\动漫收藏\恋爱小行星"
    start_rename(dir,1)






