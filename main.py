import requests
import json
import re
import time
import os
from faker import Faker
def getApi(bv):
    url = "https://www.bilibili.com/video/"+bv
    headers={
        'user-agent': Faker().user_agent()
    }
    res = requests.get(url,headers=headers).text.replace(" ", "")
    jsonstr = re.findall(r'"videoData":(.*),"upData"', res)[0]
    data = json.loads(jsonstr)
    return data["pages"]
''''
返回的内容为字典格式
cid:获取视频音频地址需要用到的参数
page:视频的序号(分p情况的序号,从1开始)
part:视频的标题
'''
def getFileurl(cid,bv):
    url=f"https://api.bilibili.com/x/player/playurl?cid={cid}&qn=0&otype=json&fourk=1&bvid={bv}&fnver=0&fnval=976"
    headers = {
        'user-agent': Faker().user_agent()
    }
    res=requests.get(url,headers=headers).json()["data"]
    datapack=[]
    datapack.append(res["accept_description"])
    datapack.append(res["dash"]["video"])
    datapack.append(res["dash"]["audio"])
    return datapack
def Download( url, filename=""):
    header={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        'referer':f'https://www.bilibili.com/video/{BV}'
    }
    start = time.time()  # 下载开始时间
    response = requests.get(url, stream=True,headers=header)  # stream=True必须写上
    size = 0  # 初始化已下载大小
    chunk_size = 1024  # 每次下载的数据大小
    content_size = int(response.headers['content-length'])  # 下载文件总大小
    try:
        if response.status_code == 200:  # 判断是否响应成功
            print('Start Download,[File size]:{size:.2f} MB\n\n'.format(
                size=content_size / chunk_size / 1024))  # 开始下载，显示下载文件大小
            if filename == "":
                filepath = url[url.rfind("/") + 1:]
            else:
                filepath = filename
            with open(filepath, 'wb') as file:  # 显示进度条
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
                    print('\r'+ '[下载进度]:%s%.2f%%'% (
                    '>'* int(size * 50 / content_size), float(size / content_size * 100)), end='')
                print("")
                end = time.time()  # 下载结束时间
            print('Download completed!,times: %.2f秒'% (end - start))  # 输出下载用时时间
        else:
            print('服务器无响应,请检查你的网络环境后再重新下载')
            return False
    except Exception as error:
        print("下载失败\n错误代码:", error)
        return False
def runcode(code):      #执行命令行
        popen = os.popen(code)
        res = popen.read()
        popen.close()
        return res
if __name__ == '__main__':
    BV="BV1Sq4y197En"
    ApiJson=getApi(BV)
    for info in ApiJson:
        data=getFileurl(info['cid'],BV)
        time.sleep(1)
        print("准备下载视频文件")
        Download(data[1][0]["baseUrl"],"video.mp4")     #下载视频文件,命名为video.mp4
        print("\n\n准备下载音频文件")
        Download(data[2][0]["baseUrl"],"audio.mp4")     #下载音频文件,命名为audio.mp4
        runcode(f"ffmpeg -i video.mp4 -i audio.mp4 -vcodec copy -acodec copy {info['part']}.mp4")#将合并后的文件重命名为原来的名字
        print("----------------下载完毕----------------")
        os.remove("video.mp4") #删除无用的视频文件
        os.remove("audio.mp4") #删除无用的音频文件

