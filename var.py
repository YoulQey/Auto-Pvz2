import sys
import numpy as np
import pyautogui
import time
s_time = time.perf_counter()  # 定义时间戳
a_time = time.perf_counter() + 0.01
执行延迟 = 0    # 单位：秒， 执行延迟

screen_w, screen_h = pyautogui.size()   # 获取屏幕分辨率
print(f"屏幕分辨率：宽{screen_w}:,高{screen_h}")

pixel = [1, 36, 1019, 621]   # 画面范围，左上到右下  #不要为0
sun = [0.055, 0.01777, 0.12099, 0.0635]      # 阳光数，左上到右下比例坐标  #不要为0
窗口标题高度 = 35

标签 =  {0: 'Defender', 1: 'Frozen vegetables', 2: 'Miner', 3: 'Penetrationer', 4: 'Pitcher', 5: 'Shooter', 6: 'Sun-Coin', 7: 'Sunner', 8: 'Swallower', 9: 'Tombstone-wall', 10: 'Zombie'}
# 标签 = {0: 'Defender', 1: 'Energy beans', 2: 'Frozen vegetables', 3: 'Miner', 4: 'Penetrationer', 5: 'Pitcher', 6: 'Shooter', 7: 'Sun-Coin', 8: 'Sunner', 9: 'Tombstone-wall', 10: 'Zombie'}
拾取物 = [6]    #后面我把能量豆和太阳，硬币等归为一类了
植物 = [0, 1, 2, 3, 4, 5, 7, 8, 9]   # 墓碑也归为植物吧
僵尸 = [10]

sun_to_sum = [7]     # 光植
att_to_sum = [3, 5, 4]      # 攻植，靠前的优先放置
boom_to_sum = [1]      # 瞬发植物，卷心菜
Swallower_to_sum = [8]  # 墓碑吞噬者
Tombstone_to_sum = [9]
阳光阈值 = 1000   # 超过此阈值则把光植全换成攻植
留冰冻阈值 = 6  # 超过x颗植物后，不留冰冻生菜

光植 = 0
光植_t = 0
光植目标数量 = 10     #放置向日葵到x 颗后停止放
光植种植列 = [0, 1, 2]      # 只种在1, 2, 3, 4列

攻植 = 0
攻植_t = 0
攻植种植列 = [0, 1, 2, 3, 4, 5, 6, 7, 8] # 只种在1, 2, 3, 4, 5, 6, 7, 8, 9列 最后一列留空


# 初始化5x8的格子，每个格子包含植物(p)和僵尸(z)的状态，以及阈值计时器(p_t),(z_t)
grid = [[{'p': 0, 'p_t': 0, 'z': 0, 'z_t': 0} for _ in range(9)] for _ in range(5)]

# 定义每个格子的坐标和范围      #模拟器画面比例与分辨率为  2534x1440(15.84:9)
grid_Scale_x1 = 0.322  # 左上角x  (比例)
grid_Scale_y1 = 0.1357  # 左上角y
grid_Scale_x = 0.9743 - grid_Scale_x1  # 右下角x-左上角x  全部格的大小(比例)
grid_Scale_y = 0.8966 - grid_Scale_y1  # 右下角y-左上角y

# 每列/行格子的坐标
grid_x = [grid_Scale_x1 + grid_Scale_x/18 + i*grid_Scale_x/9 for i in range(9)]     # 要点击的X坐标， 列
grid_y = [grid_Scale_y1 + grid_Scale_y/10 + i*grid_Scale_y/5 for i in range(5)]     # 要点击的Y坐标， 行

# 每列/行格子的范围 计算到右边和下面的范围
grid_range_x = [grid_Scale_x1 + grid_Scale_x/9 + i*grid_Scale_x/9 for i in range(9)]
grid_range_y = [grid_Scale_y1 + grid_Scale_y/5 + i*grid_Scale_y/5 for i in range(5)]


# 初始化卡片的位置与状态， 后面才发现，不检测阳光也行，阳光足够后卡片会马上亮起来
Card = [[0, 0] for i in range(植物[-1]+1)]    # 可用/不可用，y坐标   生成数为植物的最后一位
Card_T = 223        #注意！ frame出来是BGR格式，而不是RGB!  #此处判断的是B
Card_F = 111
Card_tf = [False, False, False, False, False, False, False]    # 七张卡片的可用状态


容差 = 30     # 找色的容差，+或者—
三色容差 =  np.array([25, 25, 25])
color_x = 0.029    #找色距离卡片中心的距离
color_y = 0.035

# 定义卡片栏的坐标和范围
Card_x1 = 0.09756  # x边界
Card_Scale_y1 = 0.129943  # 边界
Card_Scale_y = 0.80791 - Card_Scale_y1  # 下y - 上y
Card_x = 0.055  # 点击卡片的X坐标
Card_y = [Card_Scale_y1 + Card_Scale_y/14 + i*Card_Scale_y/7 for i in range(7)]     # 要点击的Y坐标       昨晚才反应过来可以根据yolo弄动态的
Card_range_y = [Card_Scale_y1 + Card_Scale_y/7 + i*Card_Scale_y/7 for i in range(7)]

plant = [[0, 0] for i in range(植物[-1]+1)]    # 数量，计时器   生成数为植物的最后一位  +1是因为range是从1开始的

energy_x = 0.2062328    # 能量豆坐标
energy_y = 0.9483037    # 注意！ frame出来是BGR格式，而不是RGB!  #此处判断的是B
energy_T = 225       # 能量豆要看G  有能量豆是227， 没有是50

shovel_x = 0.9395      # 铲子坐标
shovel_y = 0.9450727
无光阶段 = 0
无光阶段_t = 0

拾取区域 = [0.256645, 0.1098546, 0.999, 0.939505]    # 左上与右下
拾取禁区_右上 = 0.74243813

# 判断是否处于游戏内
暂停1 = [0.950504125, 0.08400646]     # 蓝色部分
暂停1_C = [150, 184, 120]
暂停2 = [0.9578369, 0.0549273]        # 黄色部分
暂停2_C = [31, 216, 246]          #BGR

加号1 = [0.86984417, 0.04523425]      # 暂停左边的加号
加号1_C = [44, 214, 124]
叶绿素 = [0.183318, 0.936995]       # 叶绿素
叶绿素_C = [61, 226, 160]



def sum_plant(lst, positions):
    """
    计算列表中指定位置的数的和。
    参数:
    lst (list): 要处理的列表。
    positions (list): 包含要相加的元素位置的列表。

    返回:
    int: 指定位置的数的和。
    """
    return sum(lst[pos][0] for pos in positions)    # 将列表对应的第一个索引数相加



