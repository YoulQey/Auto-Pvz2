from ultralytics import YOLO
import cv2
import numpy as np
import dxcam
import easyocr
from Window import out_text
import var

model = YOLO("best.pt")        #加载YOLO模型

camera = dxcam.create(output_idx=0, output_color="BGR", max_buffer_len=8)
target_fps = 120     # 录制截取的帧数
region = var.pixel  # 画面范围，左上到右下
camera.start(target_fps=target_fps, video_mode=True, region=region)
region_w = region[2] - region[0]
region_h = region[3] - region[1]  # 定义所截取区域长宽

reader = easyocr.Reader(['en'])


def give_sun_xy():      # 直接读取xywhn归一化过的数据

    global region, region_w, region_h, frame

    # 乘算获取的像素坐标
    sunxy = [round(var.sun[0] * (var.pixel[2] - var.pixel[0])), round(var.sun[1] * (var.pixel[3] - var.pixel[1])),
             round(var.sun[2] * (var.pixel[2] - var.pixel[0])), round(var.sun[3] * (var.pixel[3] - var.pixel[1]))]

    if region != var.pixel:     # 窗口变动
        camera.stop()  # 结束截取
        region = var.pixel  # 画面范围，左上到右下
        region_w = region[2] - region[0]
        region_h = region[3] - region[1]  # 定义所截取区域长宽
        camera.start(target_fps=target_fps, video_mode=True, region=region)
        out_text(f"窗口变动，新分辨率:{region}")

    frame = camera.get_latest_frame()
    if frame is not None:  # 防止空值报错
        results = model(source=frame, device="cuda:0")  # 对当前帧进行目标预测, device：运算设备选择
        result = results[0]

        ocr_image = frame[sunxy[1]:sunxy[3], sunxy[0]:sunxy[2]] # 裁剪图像的特定区域
        ocr = reader.readtext(ocr_image)
        if ocr:     # 提取识别结果中的文字        #其实不检测阳光也行
            txt = ocr[0][-2]  # 假设只有一个识别结果，这行代码的意思是从识别结果中提取出识别到的文字。假设只有一个识别结果，这行代码会从 result 列表中获取第一个元素，并从该元素中提取出倒数第二个值，即识别到的文字。
            try:    # 尝试将文字转换为整型
                # print(f"ocr输出，sunxy={sunxy},txt={txt}")
                suns = int(txt)
                # out_text(f"阳光={txt}")
            except ValueError:
                suns = 0
                # out_text(f"ocr识别出现Error错误，转换整型错误,txt={txt}")
        else:
            suns = 0

    else:
        # print("frame为空")
        out_text("frame为空")

    my_list = []
    for box in result.boxes:    # 打印检测到的目标的类别标签，置信度分数和边界框中心坐标
        data = box.data.cpu().numpy()  # 将数据从 GPU 转移到 CPU 并转换为 NumPy 数组
        x1, y1, x2, y2, conf, cls_label = data[0]  # 解包数据
        x1, y1, x2, y2, cls_label = map(int, [x1, y1, x2, y2, cls_label])  # 将除了conf的数据转换为整数
        my_list.extend([cls_label, conf, (x1 + (x2 - x1) / 2) / region_w, (y1 + (y2 - y1) / 2) / region_h])  # 输出归一化并只要中心的比例坐标

    game = 判断是否处于游戏中()  # 根据界面判断是否处于游戏中

    return my_list, result, suns, game


def 判断植物卡是否可用(Card):
    x = round(var.Card_x * (var.pixel[2] - var.pixel[0]) + (var.pixel[2] - var.pixel[0]) * var.color_x)     # x在帧的像素+偏移的像素
    y = round(var.Card[Card][1] + (var.pixel[3] - var.pixel[1]) * var.color_y - var.pixel[1])       # var.Card[Card][1]就是卡片在屏幕的y轴坐标 + 偏移 然后减去已偏移的屏幕坐标var.pixel[1]
    color = frame[y, x]
    if var.Card_T - var.容差 < color[0] < var.Card_T + var.容差:
        tf = 1
    else:
        tf = 0
    return tf


def 判断能量豆是否可用():
    x = round(var.energy_x * (var.pixel[2] - var.pixel[0]))  # 能量豆储存的第一个绿点的坐标
    y = round(var.energy_y * (var.pixel[3] - var.pixel[1]))
    color = frame[y, x]
    if var.energy_T - var.容差 < color[1] < var.energy_T + var.容差:    # 能量豆要看G  有能量豆是227， 没有是50
        tf = True
    else:
        tf = False
    return tf


def 判断是否处于游戏中():

    if not 找色块(var.暂停1, var.暂停1_C):         #暂停的黄色
        return False
    if not 找色块(var.暂停2, var.暂停2_C):         #暂停的蓝色
        return False
    if not 找色块(var.加号1, var.加号1_C):         # 金币加号
        return False
    if not 找色块(var.叶绿素, var.叶绿素_C):       # 叶绿素加号
        return False
    return True


def 找色块(g, b):
    x = round(g[0] * (var.pixel[2] - var.pixel[0]))  # g的坐标
    y = round(g[1] * (var.pixel[3] - var.pixel[1]))
    color = frame[y, x]
    # print(f"x:{x},y:{y},识别到的color:{color}，需要对应的颜色{b},位置的值x:{g[0]},y:{g[1]}")
    if np.all(np.abs(color - b) <= var.三色容差):   #判断是否在容差内， b为目标颜色
        return True
    else:
        return False


#####################################################################################################################
def give_xy():      # 直接读取xywhn归一化过的数据， 效率比直接读取data慢40%，原因不明
    frame = camera.get_latest_frame()
    if frame is not None:  # 防止空值报错
        results = model(source=frame, device="cuda:0")  # 对当前帧进行目标预测, device：运算设备选择
        result = results[0]
        # print("预测成功")
    else:
        print("frame为空")

    my_list = []
    for box in result.boxes:    # 打印检测到的目标的边界框坐标、置信度分数和类别标签
        cls = int(box.cls[0].cpu().numpy())     # 在GPU计算再传到cpu上
        conf = box.conf[0].cpu().numpy()
        x, y = box.xywh[0][:2].cpu().numpy()   # 将数据从 GPU 转移到 CPU 并转换为 NumPy 数组 解包数据，并且只解包前2个
        my_list.extend([cls, conf, x, y])  # 输出归一化的 中心比例坐标
    return my_list, result


def give_data():        # 使用解包data并自己归一化
    frame = camera.get_latest_frame()
    if frame is not None:  # 防止空值报错
        results = model(source=frame, device="cuda:0")  # 对当前帧进行目标预测, device：运算设备选择
        result = results[0]
        print("预测成功")
    else:
        print("frame为空")

    my_list = []
    for box in result.boxes:    # 打印检测到的目标的边界框坐标、置信度分数和类别标签
        data = box.data.cpu().numpy()   # 将数据从 GPU 转移到 CPU 并转换为 NumPy 数组
        x1, y1, x2, y2, conf, cls_label = data[0]   #解包数据
        x1, y1, x2, y2, cls_label = map(int, [x1, y1, x2, y2, cls_label])   # 将除了conf的数据转换为整数
        my_list.extend([(x1+(x2-x1)/2) / region_w, (y1+(y2-y1)/2) / region_h, cls_label, conf])  # 输出归一化并只要中心的比例坐标
        # my_list.extend([x1, y1, x2, y2, cls_label, conf])     # 输出坐标
        # my_list.extend([x1/var.pixel[2], y1/var.pixel[3], x2/var.pixel[2], y2/var.pixel[3], cls_label, conf])       # 输出归一化比例坐标
    return my_list


def give_test(ran):
    frame = camera.get_latest_frame()
    if frame is not None:  # 防止空值报错
        results = model(source=frame, device="cuda:0")  # 对当前帧进行目标预测, device：运算设备选择
        result = results[0]
        frame = results[0].plot(line_width=1)  # 绘制预测框线
        cv2.imshow("YOLOv8 推理", frame)
        print("预测成功")
    else:
        print("frame为空")

    my_list = []
    for box in result.boxes:    # 打印检测到的目标的边界框坐标、置信度分数和类别标签
        data = box.data.cpu().numpy()   # 将数据从 GPU 转移到 CPU 并转换为 NumPy 数组
        x1, y1, x2, y2, conf, cls_label = data[0]   #解包数据
        x1, y1, x2, y2, cls_label = map(int, [x1, y1, x2, y2, cls_label])   # 将除了conf的数据转换为整数
        if ran == 4:
            my_list.extend([(x1+(x2-x1)/2) / region_w, (y1+(y2-y1)/2) / region_h, cls_label, conf])  # 输出归一化并只要中心的比例坐标
        else:
            my_list.extend([x1, y1, x2, y2, cls_label, conf])     # 输出坐标
            # my_list.extend([x1/var.pixel[2], y1/var.pixel[3], x2/var.pixel[2], y2/var.pixel[3], cls_label, conf])       # 输出归一化比例坐标

    print(f"图像宽：{region_w}，高：{region_h}")
    camera.stop()   # 结束截取
    return my_list


