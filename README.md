# 介绍
基于 Python、tornado 制作的星火应用商店下载量统计后端  
# 如何运行？  
```bash
sudo apt install git python3 python3-tornado
git clone https://gitee.com/gfdgd-xi/spark-store-download
cd spark-store-download
# 这里忽略参数设置内容，一定要设置，否则可能运行会有很大问题
# 如何设置参数？直接编辑 main.py 即可，有注释进行引导
python3 main.py
```
# 如何调用这个接口？
使用 http 的库使用 post 调用：
```commandline
http://IP:端口号/自定义路径
```
或者  
```commandline
https://IP:端口号/自定义路径
```
post 内容：  
```json
{
    "spk": "SPK 分享链接"
}
```

# ©2022~Now