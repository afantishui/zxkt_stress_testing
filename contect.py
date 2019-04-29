from socket import *
import canvas_message_pb2
import binascii
from struct import *
import time
import ctypes
import math
import random
import xlrd
import xlwt
import threading


# --------------------------------------------------------------------
# 注册TCP连接
def register_packet(uid, name, token, memtype, classid):
    canvas = canvas_message_pb2.MemRegisterRequest()
    canvas.uId = uid  # "789b31de-4ede-4417-9f20-2bbad9a8911f"   # 学生id、教师id
    canvas.memName = name  # "在线二"  # 学生姓名、教师姓名
    canvas.token = token  # "8a48e33ce47e9f39d4082c3f8297d671"  # token
    canvas.memType = int(memtype)  # 1：学生 2：教师
    canvas.classId = classid  # "898801de-b57e-446f-8835-35bf07a8c2a3"    # 课堂Id（课表Id）
    canvas = canvas.SerializeToString()     # 将需要发送的数据结构序列化成字符串

    head = -21415431
    module = 1
    type = 1
    size = canvas.__len__()
    header = pack('ihhi', head, module, type, size)
    header += canvas
    return header


def recon_packet(uid, classid):
    canvas = canvas_message_pb2.MemberReconnect()
    canvas.uId = uid  # "789b31de-4ede-4417-9f20-2bbad9a8911f"
    canvas.classId = classid  # "898801de-b57e-446f-8835-35bf07a8c2a3"
    canvas.action = "ready"
    canvas = canvas.SerializeToString()  # 将需要发送的数据结构序列化成字符串

    head = -21415431
    module = 1
    type = 6
    size = canvas.__len__()
    header = pack('ihhi', head, module, type, size)
    header += canvas
    return header


def pen_down_packet(lid):
    canvas = canvas_message_pb2.CanvasPenDown()
    canvas.cid = '5000'  # 笔画id
    canvas.lid = '%d'%lid    # 每次要不一样 给自增
    x = int(random.uniform(10, 100))  # 10-100随机坐标
    y = int(random.uniform(10, 100))  # 10-100随机坐标
    weight = round(random.uniform(0.1, 1), 1)  # 随机画笔大小,粗细程度: 0~1
    colorArr = [0xffffffff, 0xffffffff, 0xff000000, 0xffff0000, 0xffff4500, 0xffffff00, 0xff006400, 0xff800080]
    color = colorArr[random.randint(0, 7)]  # 随机颜色
    canvas.x = x  # x坐标 float
    canvas.y = y  # y坐标 float
    canvas.weight = weight    # 粗细程度: 0~1
    canvas.color = color  # 颜色。
    canvas = canvas.SerializeToString()  # 将需要发送的数据结构序列化成字符串

    head = -21415431
    module = 2
    type = 2000
    size = canvas.__len__()
    header = pack('ihhi', head, module, type, size)
    header += canvas
    return header


def pen_draw_packet(lid):
    canvas = canvas_message_pb2.CanvasPenDraw()
    canvas.cid = '5000'
    canvas.lid = '%d'%lid   # 哪个轨迹在画 每次要不一样 给自增
    x = int(random.uniform(10, 100))  # 10-100随机坐标
    y = int(random.uniform(10, 100))  # 10-100随机坐标
    canvas.coordinate.append(x)  # 点坐标, x0,y0,x1,y1,x2,y2.....
    canvas.coordinate.append(y)
    canvas = canvas.SerializeToString()  # 将需要发送的数据结构序列化成字符串

    head = -21415431
    module = 2
    type = 2001
    size = canvas.__len__()
    header = pack('ihhi', head, module, type, size)
    header += canvas
    return header


def pen_done_packet(lid):
    canvas = canvas_message_pb2.CanvasPenDone()
    canvas.cid = '5000'
    canvas.lid = '%d'%lid
    x = int(random.uniform(10, 100))  # 10-100随机坐标
    canvas.x = x  # x坐标
    canvas.y = x  # y坐标
    canvas = canvas.SerializeToString()  # 将需要发送的数据结构序列化成字符串

    head = -21415431
    module = 2
    type = 2002
    size = canvas.__len__()
    # 包头—4字节,模块号2字节,命令号2字节,长度4字节
    header = pack('ihhi', head, module, type, size)
    header += canvas
    return header


def text_packet(lid):
    x = random.uniform(10, 100)  # 10-100随机坐标
    y = random.uniform(10, 100)  # 10-100随机坐标
    content = "测试test123456789!@#$%^&"
    textadd_canvas = canvas_message_pb2.CanvasTextAdded()
    textadd_canvas.cid = '5000'  # 笔画id
    textadd_canvas.lid = '%d' % lid  # 每次要不一样 给自增
    textadd_canvas.x = x  # x坐标 float
    textadd_canvas.y = y  # y坐标 float
    textadd_canvas.width = 60
    textadd_canvas.height = 20
    textadd_canvas = textadd_canvas.SerializeToString()  # 将需要发送的数据结构序列化成字符串

    textchange_canvas = canvas_message_pb2.CanvasTextChanged()
    textchange_canvas.cid = '5000'  # 笔画id
    textchange_canvas.lid = '%d' % lid  # 每次要不一样 给自增
    textchange_canvas.content = content  # 文本内容
    textchange_canvas.width = 60
    textchange_canvas.height = 20
    textchange_canvas = textchange_canvas.SerializeToString()  # 将需要发送的数据结构序列化成字符串

    textdone_canvas = canvas_message_pb2.CanvasTextDone()
    textdone_canvas.cid = '5000'  # 笔画id
    textdone_canvas.lid = '%d' % lid  # 每次要不一样 给自增
    textdone_canvas.x = x  # x坐标 float
    textdone_canvas.y = y  # y坐标 float
    textdone_canvas.content = content  # 文本内容
    textdone_canvas.width = 60
    textdone_canvas.height = 20
    textdone_canvas = textdone_canvas.SerializeToString()  # 将需要发送的数据结构序列化成字符串

    head = -21415431
    module = 2
    type1 = 3000
    type2 = 3001
    type3 = 3002
    size1 = textadd_canvas.__len__()
    size2 = textchange_canvas.__len__()
    size3 = textdone_canvas.__len__()
    header1 = pack('ihhi', head, module, type1, size1)
    header2 = pack('ihhi', head, module, type2, size2)
    header3 = pack('ihhi', head, module, type3, size3)
    header1 += textadd_canvas
    header2 += textchange_canvas
    header3 += textdone_canvas
    return header1, header2, header3


def text_packet1(lid):
    x = random.uniform(10, 100)  # 10-100随机坐标
    y = random.uniform(10, 100)  # 10-100随机坐标
    content = "测试test123456789!@#$%^&"
    textadd_canvas = canvas_message_pb2.CanvasTextAdded()
    textadd_canvas.cid = '5000'  # 笔画id
    textadd_canvas.lid = '%d' % lid  # 每次要不一样 给自增
    textadd_canvas.x = x  # x坐标 float
    textadd_canvas.y = y  # y坐标 float
    textadd_canvas.width = 60
    textadd_canvas.height = 20
    textadd_canvas = textadd_canvas.SerializeToString()  # 将需要发送的数据结构序列化成字符串

    head = -21415431
    module = 2
    type1 = 3000
    size1 = textadd_canvas.__len__()
    header1 = pack('ihhi', head, module, type1, size1)
    header1 += textadd_canvas
    return header1


def text_packet2(lid):
    x = random.uniform(10, 100)  # 10-100随机坐标
    y = random.uniform(10, 100)  # 10-100随机坐标
    content = "测试test123456789!@#$%^&"
    textchange_canvas = canvas_message_pb2.CanvasTextChanged()
    textchange_canvas.cid = '5000'  # 笔画id
    textchange_canvas.lid = '%d' % lid  # 每次要不一样 给自增
    textchange_canvas.content = content  # 文本内容
    textchange_canvas.width = 60
    textchange_canvas.height = 20
    textchange_canvas = textchange_canvas.SerializeToString()  # 将需要发送的数据结构序列化成字符串

    head = -21415431
    module = 2
    type2 = 3001

    size2 = textchange_canvas.__len__()
    header2 = pack('ihhi', head, module, type2, size2)
    header2 += textchange_canvas
    return header2


def text_packet3(lid):
    x = random.uniform(10, 100)  # 10-100随机坐标
    y = random.uniform(10, 100)  # 10-100随机坐标
    content = "测试test123456789!@#$%^&"
    textdone_canvas = canvas_message_pb2.CanvasTextDone()
    textdone_canvas.cid = '5000'  # 笔画id
    textdone_canvas.lid = '%d' % lid  # 每次要不一样 给自增
    textdone_canvas.x = x  # x坐标 float
    textdone_canvas.y = y  # y坐标 float
    textdone_canvas.content = content  # 文本内容
    textdone_canvas.width = 60
    textdone_canvas.height = 20
    textdone_canvas = textdone_canvas.SerializeToString()  # 将需要发送的数据结构序列化成字符串

    head = -21415431
    module = 2
    type3 = 3002
    size3 = textdone_canvas.__len__()
    header3 = pack('ihhi', head, module, type3, size3)
    header3 += textdone_canvas
    return header3


# 获取excel数据操作
def getdata_excel(filepath):
    f = xlrd.open_workbook(filepath)
    ex = f.sheets()[0]
    nrows = ex.nrows
    case_uid_list = []   # uid
    case_name_list = []   # 学生/老师姓名
    case_token_list = []   # token
    case_type_list = []   # 1学生 2 老师
    case_classid_list = []   # classid

    for i in range(1, nrows):
        case_uid_list.append(ex.cell(i, 0).value)
        case_name_list.append(ex.cell(i, 1).value)
        case_token_list.append(ex.cell(i, 2).value)
        case_classid_list.append(ex.cell(i, 3).value)
        case_type_list.append(ex.cell(i, 4).value)
    return case_uid_list, case_name_list, case_token_list, case_classid_list, case_type_list, nrows-1


# 发送
def send(host, port, uid, name, token, type, classid, lid, count):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, port))
    register = register_packet(uid, name, token, type, classid)
    reconnect = recon_packet(uid, classid)
    s.send(register)
    time.sleep(0.5)
    s.send(reconnect)
    time.sleep(0.5)
    print("%s注册与重连" % name)

    id = lid
    for i in range(0, count):
        s.send(pen_down_packet(id))
        s.send(pen_draw_packet(id))
        s.send(pen_done_packet(id))
        time.sleep(0.25)
        s.send(text_packet1(id))
        s.send(text_packet2(id))
        s.send(text_packet3(id))
        time.sleep(0.25)
        id += i
        print("%s执行第%s遍操作" % (name, i+1))
    data = s.recv(1024)
    s.close()


if __name__ == '__main__':
    t_start = time.time()
    host = '120.77.198.98'  # 服务器的ip地址 120.77.57.10  120.77.198.98 47.107.208.146
    port = 11233			# 服务器的端口号
    filepath = "E://python//在线课堂压测//conf.xlsx"  # excel配置路径
    count = 3500 # 画笔操作次数
    # 读取excel配置表 读取长度 for循环 传参
    uid, name, token, classid, type, nrow = getdata_excel(filepath)
    lid = 1
    l = []
    # 多线程实现并发客户端
    for i in range(nrow):
        t = threading.Thread(target=send, args=[host, port, uid[i], name[i], token[i], type[i], classid[i], lid, count, ])
        t.start()
        l.append(t)
        print("建立并发送socket链接：%s" % name[i])
    for t in l:
        t.join()
    t2 = time.time()-t_start
    print('ok')
    print("用时：%.2f秒" % t2)