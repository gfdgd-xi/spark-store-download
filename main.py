#!/usr/bin/python3
##########################################
# 星火应用商店下载量统计功能
# 作者：gfdgd xi、为什么您不喜欢熊出没和阿布
# 版本：1.0
# 更新时间：2022年07月01日（期末考试完了！！！）
# 接口详解：
#     1、使用 http post 操作，post 为：
#    {"spk": "SPK链接"}
#    暂不支持包名以及 get 操作
##########################################
###############
# 引入库
###############
import os
import sys
import json
import time
import threading
import traceback
import urllib.parse
import tornado.web
import tornado.ioloop

###############
# 参数设置
###############
# deb 仓库本地地址
packagePath = "/home/gfdgd_xi/Desktop/spark-download"
# 端口号
post = 8000
# 启动/关闭防单 IP 高刷功能
stopConnectOften = True
# IP 黑名单清理时间（永不清理可以设置为负数）
cleanTimeSet = 60 * 60
# 最大访问值
max_post = 30
# 启用/关闭 IP 单一时间访问太大自动保存本地（未实现）
unableUseIpListSave = True
# IP 单一时间访问太大自动保存本地的值
unableUseIP = 100
# 调试模式（未实现）
debug = False


###############
# 非参数设置，请勿乱动
###############
# bug 数量记录
bug = 0
# 黑名单 IP
ip = {}
# 清理时间
cleanTime = 30
# 读取程序路径
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
# 黑名单写入次数
blackWriteTime = 0
# 版本
version = "1.0.0"
# 作者
celebrateUser = ["gfdgd xi", "为什么您不喜欢熊出没和阿布呢"]

###############
# 函数实现
###############
def Clean():
    global cleanTime
    global blackWriteTime
    global unableUseIpListSave
    cleanTime -= 1
    if cleanTime == 0:  # 到达 IP 黑名单清理时间
        # 读取有没有调皮的 IP 访问次数爆炸
        ipFile = open(f"{programPath}/ip.json", "r")
        ipList = json.loads(ipFile.read())
        ipFile.close()
        if unableUseIpListSave:
            black = False
            for key, value in ip.items():
                if value >= unableUseIP and not ip[key] < 0:
                    ipList.append(key)
                    black = True
            if black:
                ipFile = open(f"{programPath}/ip.json", "w")
                ipFile.write(json.dumps(ipList))
                ipFile.close()
                blackWriteTime += 1
                print(f"写入黑名单{blackWriteTime}次")
        ip.clear()
        for i in ipList:
            ip[i] = -1
        cleanTime = cleanTimeSet
    time.sleep(1)
    Clean()

class SPK:
    def __init__(self, spkUrl, savePath):
        self.spkUrl = spkUrl
        package = urllib.parse.urlparse(spkUrl).path[1:]
        self.package = package[package.index("/") + 1:]
        self.savePath = savePath

    def information(self):
        appListFile = open(f"{self.savePath}/applist.json").read()
        appList = json.loads(appListFile)
        for i in appList:
            if i["Pkgname"] == self.package:
                return i

    def save(self):
        for i in ["chat", "development", "games", "image_graphics", "music", "network", "office", "others", "reading", "themes", "tools", "video"]:
            path = f"{self.savePath}/store/{i}/{self.package}/download-times.txt"
            floder = f"{self.savePath}/store/{i}/{self.package}/"
            # 文件不存在的情况
            if not os.path.exists(floder):
                continue
            # 有文件但却没下载量文件的情况
            if not os.path.exists(path):
                os.mknod(path)
                read = 0
            else:
                # 读取文件
                file = open(path, "r")
                read = file.read()
                file.close()
            # 写入文件
            file = open(path, "w")
            # 对文件异常值的判断
            if read == "":
               read = 0
            else:
                read = int(read)
            file.write(str(read + 1))
            file.close()
            return True
        return False

class Save(tornado.web.RequestHandler):
    def get(self):
        self.write('{"ExitCode": 5, "Error": "访问方式错误"}')

    def post(self):
        if stopConnectOften:
            if self.request.headers["Host"] in ip:
                if ip[self.request.headers["Host"]] < 0:
                    self.write('{"ExitCode": 2, "Error": "此 IP 已经被永久封禁，无法继续"}')
                    return
                ip[self.request.headers["Host"]] += 1
            else:
                ip[self.request.headers["Host"]] = 1
            if ip[self.request.headers["Host"]] > max_post:
                self.write('{"ExitCode": 1, "Error": "此IP地址超过最大访问次数，无法继续"}')
                return
        try:
            if not SPK(str(self.get_body_argument("spk")), packagePath).save():
                self.write('{"ExitCode": 4, "Error": "没有找到指定的包"}')
                return
            self.write('{"ExitCode": 0, "Error": ""}')
        except:
            if debug:
                self.write(json.dumps({"ExitCode": 6, "Error": traceback.format_exc()}))
            else:
                self.write('{"ExitCode": 6, "Error": "500 服务器错误"}')
            global bug
            bug += 1
            print(f"#########第{bug}个错误，不影响程序继续运行##########")
            traceback.print_exc()

###############
# 启动事件
###############
if __name__ == "__main__":
    if "--help" in sys.argv:
        print("帮助：")
        print("--about  查看程序信息")
        print("更多内容需要修改程序参数")
        sys.exit()
    if "--about" in sys.argv:
        print(f"程序版本：{version}")
        print(f"程序作者：{'，'.join(celebrateUser)}")
        sys.exit()
    # 读取黑名单 IP
    ipFile = open(f"{programPath}/ip.json", "r")
    for i in json.loads(ipFile.read()):
        ip[i] = -1
    ipFile.close()
    # 启动黑名单清空（如果启用的话）
    if stopConnectOften:
        threading.Thread(target=Clean).start()
    # 开启监听
    app = tornado.web.Application([
        (r"/", Save)
    ])
    app.listen(post)
    tornado.ioloop.IOLoop.current().start()