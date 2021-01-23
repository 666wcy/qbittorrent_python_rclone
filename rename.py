import re
import os
os.chdir(os.path.dirname(__file__))
'''重命名的正则表达式'''

def edit_s4(title):
    title=str(title)
    title=title.replace("FIN","").replace("FIN","").replace("BeanSub&FZSD-","").replace("FIN","").replace("FIN","").replace("yuv420p10","").replace(".rev","").replace("END","")
    title=title.replace(" S4","")

    strinfo = re.compile("第(.*?)話",)
    if len(strinfo.findall(title))!=0:
        title=strinfo.sub(f"{strinfo.findall(title)[0]} ",title)

    strinfo = re.compile("第(.*?)话",)
    if len(strinfo.findall(title))!=0:
        title=strinfo.sub(f"{strinfo.findall(title)[0]} ",title)

    strinfo = re.compile("v\d",)
    if len(strinfo.findall(title))!=0:
        title=strinfo.sub(f"",title)


    strinfo = re.compile("\D([0-9][0-9])\W",)
    if len(strinfo.findall(title))!=0:
        title=strinfo.sub(f" S04E{strinfo.findall(title)[0]} ",title)

    title=title.replace("  "," ")
    print(title)
    return title

def edit_s3(title):
    title=str(title)
    title=title.replace("FIN","").replace("FIN","").replace("BeanSub&FZSD-","").replace("FIN","").replace("FIN","").replace("yuv420p10","").replace(".rev","").replace("END","")
    title=title.replace(" S3","")

    strinfo = re.compile("第(.*?)話",)
    if len(strinfo.findall(title))!=0:
        title=strinfo.sub(f"{strinfo.findall(title)[0]} ",title)

    strinfo = re.compile("第(.*?)话",)
    if len(strinfo.findall(title))!=0:
        title=strinfo.sub(f"{strinfo.findall(title)[0]} ",title)

    strinfo = re.compile("v\d",)
    if len(strinfo.findall(title))!=0:
        title=strinfo.sub(f"",title)


    strinfo = re.compile("\D([0-9][0-9])\W",)
    if len(strinfo.findall(title))!=0:
        title=strinfo.sub(f" S03E{strinfo.findall(title)[0]} ",title)

    title=title.replace("  "," ")
    print(title)
    return title

def edit_s2(title):
    title=str(title)
    title=title.replace("FIN","").replace("FIN","").replace("BeanSub&FZSD-","").replace("FIN","").replace("FIN","").replace("yuv420p10","").replace(".rev","").replace("END","")
    title=title.replace(" S2","")

    strinfo = re.compile("第(.*?)話",)
    if len(strinfo.findall(title))!=0:
        title=strinfo.sub(f"{strinfo.findall(title)[0]} ",title)

    strinfo = re.compile("第(.*?)话",)
    if len(strinfo.findall(title))!=0:
        title=strinfo.sub(f"{strinfo.findall(title)[0]} ",title)

    strinfo = re.compile("v\d",)
    if len(strinfo.findall(title))!=0:
        title=strinfo.sub(f"",title)


    strinfo = re.compile("\D([0-9][0-9])\W",)
    if len(strinfo.findall(title))!=0:
        title=strinfo.sub(f" S02E{strinfo.findall(title)[0]} ",title)

    title=title.replace("  "," ")
    print(title)
    return title

def edit_s1(title):
    title=str(title)
    title=title.replace("FIN","").replace("FIN","").replace("BeanSub&FZSD-","").replace("FIN","").replace("FIN","").replace("yuv420p10","").replace(".rev","").replace("END","")
    title=title.replace(" S1","")

    strinfo = re.compile("第(.*?)話",)
    if len(strinfo.findall(title))!=0:
        title=strinfo.sub(f"{strinfo.findall(title)[0]} ",title)

    strinfo = re.compile("第(.*?)话",)
    if len(strinfo.findall(title))!=0:
        title=strinfo.sub(f"{strinfo.findall(title)[0]} ",title)

    strinfo = re.compile("v\d",)
    if len(strinfo.findall(title))!=0:
        title=strinfo.sub(f"",title)


    strinfo = re.compile("\D([0-9][0-9])\W",)
    if len(strinfo.findall(title))!=0:
        title=strinfo.sub(f" S01E{strinfo.findall(title)[0]} ",title)

    title=title.replace("  "," ")
    print(title)
    return title

if __name__ == '__main__':

    title=" [VCB-Studio] Re：Zero kara Hajimeru Isekai Seikatsu [01][Ma10p_1080p][x265_flac_aac].mkv"
    edit_s1(title)