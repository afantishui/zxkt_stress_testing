# 测试代码

#### 介绍
压测脚本使用python编写socket模拟客户端连接课堂进行画、写操作

#### 软件架构
在线课堂是基于QT框架开发的PC产品，客户端C++,服务端Java


#### 安装教程

1. 需python3环境
2. 涉及到具体业务的两个canvas_message文件内容信息已删除，下载不能调试运行


#### 使用说明

1. content.py执行文件，目前需在代码修改执行的次数
2. conf.xls 配置文件，mentype 1是老师，2是学生

#### 大致思路
1. socket连接服务器，发操作报文（注册TCP、画笔、文本等操作）
2. 报文构成  包头 | 模块号 | 命令号 | 长度 | 数据 
3. 业务数据，客户端服务器使用Protocol Buffer序列化反序列化
4. 组装好每个需发送的业务操作报文
5. 准备好测试数据
6. 使用多线程向服务器发送报文
7. 下面是一个注册TCP报文组成过程
```
def register_packet(uid, name, token, memtype, classid):
    canvas = canvas_message_pb2.MemRegisterRequest()
    canvas.uId = uid  # "789b31de-4ede-4417-9f20-2bbad9a8911f"   # 学生id、教师id
    canvas.memName = name  # "在线二"  # 学生姓名、教师姓名
    canvas.token = token  # "8a48e33ce47e9f39d4082c3f8297d671"  # token
    canvas.memType = int(memtype)  # 1：学生 2：教师
    canvas.classId = classid  # "898801de-b57e-446f-8835-35bf07a8c2a3"    # 课堂Id（课表Id）
    canvas = canvas.SerializeToString()     # 将需要发送的数据结构序列化成字符串

    head = xxx  # 包头
    module = 1  # 模块号
    type = 1    # 命令号
    size = canvas.__len__()  # 长度
    header = pack('ihhi', head, module, type, size)  # 根据格式符，转换为字符串
    header += canvas  # 加入业务数据组成一个报文
    return header
