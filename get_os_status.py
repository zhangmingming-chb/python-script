import os
import time
def auto_install_package(packages_name_list):
    installed_package = list()
    not_installed_package = list()
    p = os.popen("pip3 list")  # 获取所有包名 直接用 pip list 也可获取
    pip_list = p.read().lower()  # 读取所有内容
    for package_name in packages_name_list:
        if package_name.lower() in pip_list:
            installed_package.append(package_name)
        else:
            not_installed_package.append(package_name)

    if len(installed_package) != 0:
        for package_name in installed_package:
            print("[INFO] 依赖包 {} 已存在！".format(package_name))
    else:
        print("[INFO] 未检测到任何已安装依赖包！")

    if len(not_installed_package) != 0:
        for package_name in not_installed_package:
            print("[INFO] 检测到 {} 包未安装 正在自动安装中...".format(package_name))
            start_time = time.time()
            p = os.popen("pip3 install {} -i https://pypi.douban.com/simple/".format(package_name))
            if "Success" in p.read():
                spend_time = time.time() - start_time
                print("[INFO Spend_time:{}s] 依赖包 {} 安装成功!".format(round(spend_time,2),package_name))
            else:
                print('[INFO] 依赖包 {} 安装失败! {}'.format(package_name,p.read()))
    else:
        print("[INFO] 引入的全部依赖包已存在！")
auto_install_package(["psutil","requests"])
import psutil
import datetime
import platform
import time
import re
import requests


def get_ip_info():
    res1 = requests.get('http://httpbin.org/ip')
    ip = re.findall('"origin": "(.*?), .*?"', res1.text)[0]
    res2 = requests.get('https://www.hao7188.com/ip/{}.html'.format(ip))
    ip_dress_data = re.findall('<span>(.*?)</span>', res2.text)[2]

    return ip,ip_dress_data
def io_get_bytes(sent=False, recv=False):
    internet = psutil.net_io_counters()
    if internet == None:
        return None
    io_sent = internet.bytes_sent
    io_recv = internet.bytes_recv
    if sent == True and recv == True:
        return [io_sent, io_recv]
    elif sent == True:
        return io_sent
    elif recv == True:
        return io_recv
    else:
        return None


print("************************************************")
print("*               系统检测工具                   *")
print("************************************************")
try:
    net_io = psutil.net_io_counters()
    net_in = psutil.net_io_counters(pernic=True)
    print('[网络信息]')
    print("--------------------------------------------------------")
    print("IP地址:  {}".format(get_ip_info()[0]))
    print("地理位置:", get_ip_info()[1])
    print(f'发送流量: {round(net_io.bytes_sent/1024**2)}M')
    print(f'接收流量: {round(net_io.bytes_recv/1024**2)}M')
    print(f'发送数据包: {round(net_io.packets_sent/1024**1)}')
    print(f'接收数据包: {round(net_io.packets_recv/1024**1)}')
    print("--------------------------------------------------------")
except Exception as e:
    print("网络检测错误:{}".format(e))
try:
    print('[磁盘情况]')
    print("--------------------------------------------------------")
    for i in range(len(psutil.disk_partitions())):
        disk=psutil.disk_partitions()[i].device
        print(psutil.disk_partitions()[i].device)
        print(f"磁盘空间: {round(psutil.disk_usage(disk).used/1024**3)}/{round(psutil.disk_usage(disk).total/1024**3)}G {round(psutil.disk_usage(disk).percent)}%")
        print(f"磁盘可用: {round(psutil.disk_usage(disk).free/1024**3)}G")
    print("--------------------------------------------------------")
except Exception as e:
    print("磁盘检测错误: {}".format(e))
try:
    print("[系统信息]")
    print("--------------------------------------------------------")
    print(f"当前用户: {psutil.users()[0][0]}")
    print(f"电脑名: {platform.node()}")
    print(f"系统版本: {platform.platform()}")
    print(f"CPU核心数: {psutil.cpu_count(logical=False)}")
    print(f"CPU型号: {platform.processor()}")
    print(f"开机时间: {datetime.datetime.fromtimestamp(psutil.users()[0][3])}")
    print(f"运行时间: {datetime.datetime.now()-datetime.datetime.fromtimestamp(psutil.users()[0][3])}")
    print("--------------------------------------------------------")
except Exception as e:
    print("系统检测错误:{}".format(e))


interval = 1  # 每隔 interval 秒获取一次网络IO信息, 数值越小, 测得的网速越准确
unit='s' #时间单位

k = 1024  # 一 K 所包含的字节数
m = 1048576  # 一 M 所包含的字节数
while True:
    byteSent1 = io_get_bytes(sent=True)  # 获取开机以来上传的字节数
    byteRecv1 = io_get_bytes(recv=True)  # 获取开机以来下载的字节数
    time.sleep(interval)  # 间隔 interval 秒
    byteSent2 = io_get_bytes(sent=True)  # 再次获取开机以来上传的字节数
    byteRecv2 = io_get_bytes(recv=True)  # 再次获取开机以来下载的字节数
    sent = byteSent2 - byteSent1  # interval 秒内所获取的上传字节数
    recv = byteRecv2 - byteRecv1  # interval 秒内所获取的下载字节数



    if sent > m:
        sent = sent / m
        sent_unit = 'M/' + unit
    elif sent > k:
        sent = sent / k
        sent_unit = 'K/' + unit
    elif sent >= 0:
        sent_unit = 'B/' + unit


    if recv > m:
        recv = recv / m
        recv_unit = 'M/'  + unit
    elif recv > k:
        recv = recv / k
        recv_unit = 'K/'  + unit
    elif recv >=0:
        recv_unit = 'B/'  + unit
    #
    cpu_percent=psutil.cpu_percent()
    #内存消耗百分比
    memory_spend_percent=psutil.virtual_memory().percent
    #内存消耗
    memory_spend_sum=round(psutil.virtual_memory().used/1024**2)
    #内存总量
    memory_all_sum=round(psutil.virtual_memory().total/1024**2)
    #内存空闲
    memory_free_sum=round(psutil.virtual_memory().free/1024**2)

    print(f'\r[上传速度]: {round(sent,2)} {sent_unit} [下载速度]: {round(recv,2)} {recv_unit} [CPU使用率]:{cpu_percent}% [内存占用]: {memory_spend_percent}%({memory_spend_sum}/{memory_all_sum}M)',end="")
