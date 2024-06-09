from click import click
import var
from Window import out_text
from rec import 判断能量豆是否可用
攻植防守没阳光 = 0


def number_to_string(number):
    return var.标签.get(number, str(number))


def 拾取(give):
    for i in range(0, len(give), 4):
        cls = give[i]  # 标签  保险起见可以加转换类型float(), int()等
        if cls in var.拾取物:
            conf = give[i + 1]  # 置信值
            if conf > 0.5:  # 置信度阈值
                x = give[i + 2]
                y = give[i + 3]
                if var.拾取区域[0] < x < var.拾取区域[2] and y < var.拾取区域[3]:     # 在拾取区域内
                    if y > var.拾取区域[1] or y <= var.拾取区域[1] and x < var.拾取禁区_右上:     # 如果y小于区域上方，则判断是否处于禁区
                        x1 = round(var.pixel[0] + x * (var.pixel[2] - var.pixel[0]))  # 要点击的实际坐标
                        y1 = round(var.pixel[1] + y * (var.pixel[3] - var.pixel[1]))  # round四舍五入
                        click(x1, y1)
                        return  # 拾取后立即退出def


                else:
                    return  # 立即退出def

                # out_text(f"点击，cls={cls},x={x},y={y}")


def 放置(p, x, fy):   # 植物， 行， 列
    x1 = round(var.Card_x * (var.pixel[2] - var.pixel[0]) + var.pixel[0])   # 要点击的实际坐标
    y1 = round(var.Card[p][1])
    click(x1, y1)
    # out_text(f"拿{p}卡,x:({x1}),y{y1})")
    # print(f"放置x:{x},fy:{fy}")
    x2 = round(var.grid_x[x] * (var.pixel[2] - var.pixel[0]) + var.pixel[0])   # 要点击的实际坐标   grid_x=列的坐标
    y2 = round(var.grid_y[fy] * (var.pixel[3] - var.pixel[1]) + var.pixel[1])   # grid_y=行的坐标
    click(x2, y2)
    str = number_to_string(p)
    out_text(f"放置{str},{x+1}列({x2}),{fy+1}行({y2})")

def 放置光植(grid):

    for p in var.sun_to_sum:
        if var.Card[p][0] == 1:     # 判断是否有光植准备就绪

            for x in var.光植种植列:
                for fy, celly in enumerate(grid):

                    if celly[x]['p'] == 0:
                        放置(p, x, fy)
                        return  # 放置后立即退出def


def 放置攻植(grid, yyy):
    global 攻植防守没阳光
    if yyy != -1:
        for p in var.att_to_sum:
            if var.Card[p][0] == 1:  # 判断是否有攻植准备就绪

                    for x in var.攻植种植列:
                        if grid[yyy][x]['p'] == 0:  # 判断该行的某列是否有空位      # 得弄优先按行！
                            放置(p, x, yyy)
                            return  # 放置后立即退出def
            else:
                攻植防守没阳光 = 1
                str = number_to_string(p)
                # out_text(f"攻植{str},不够阳光")

    else:
        for p in var.att_to_sum:
            if var.Card[p][0] == 1:  # 判断是否有攻植准备就绪

                for x in var.攻植种植列:
                    for fy, celly in enumerate(grid):   # 行

                        if celly[x]['p'] == 0:
                            放置(p, x, fy)
                            return  # 放置后立即退出def


def 放置卷心菜(grid, iny):

    for p in var.boom_to_sum:
        if var.Card[p][0] == 1:  # 判断是否有瞬发植物准备就绪

            for fx, yyy in enumerate(grid[iny]):

                if yyy['z'] == 1:  # 判断某一列是否有僵尸

                    if yyy['p'] == 0:
                        out_text(f"在僵尸脚下-放置卷心菜, 第{iny+1}行,{fx+1}列")
                        放置(p, fx, iny)
                        return  # 放置后立即退出def
                    else:
                        ffx = fx
                        kx = 0
                        while True:
                            ffx = ffx - 1   # 有植物就顺推到左边的列
                            kx = kx + 1  # 仅作判断在僵尸左边多少格
                            if ffx >= 0:
                                if grid[iny][ffx]['p'] == 0:
                                    out_text(f"在僵尸左边{kx}格-放置卷心菜")
                                    放置(p, ffx, iny)
                                    return  # 放置后立即退出def
                            else:
                                out_text(f"放置卷心菜失败，僵尸前面的格子都满了")
                                return
                # else:# out_text(f"尝试放置卷心菜错误，判断没有僵尸")




def 放置植物(grid, suns):
    global 攻植防守没阳光
    攻植防守没阳光 = 0

    for i in var.Card:
        if i[0] == 1:   #如果有就绪的植物

            for iny, yy in enumerate(grid):
                for inx, xx in enumerate(yy):
                    if xx['z'] == 1:     # 如果某格有僵尸
                        if not any(d['p'] == 1 for d in grid[iny]):     # 如果某一行没有攻植
                            放置卷心菜(grid, iny)
                            放置攻植(grid, iny)
                            return  # 放置后立即退出def， 没放置就等阳光

                        elif var.攻植 >= 5:
                            for p in var.boom_to_sum:
                                if var.Card[p][0] == 1:  # 判断是否有瞬发植物准备就绪
                                    放置卷心菜(grid, iny)
                                    return

                        # else:
                        #     out_text(f"有僵尸，但是有攻植，放置光植")
                        #     if var.光植 < var.光植目标数量:
                        #         放置光植(grid)
                        #         return  # 放置后立即退出def， 没放置就等阳光

            if 攻植防守没阳光 != 1:

                if not suns >= var.阳光阈值:    #如果不大于
                    if var.光植 < var.光植目标数量 and var.无光阶段 != 1:
                        放置光植(grid)
                        return  # 放置后立即退出def， 没放置就等阳光
                    else:
                        放置攻植(grid, -1)  # -1为 没判断到僵尸时放
                        return  # 放置后立即退出def， 没放置就等阳光
                else:
                    var.无光阶段 = 1
                    强制放置攻植(grid)
                    return  # 放置后立即退出def， 没放置就等阳光



def 使用能量豆(give):
    tf = 判断能量豆是否可用()    # 值为True 或 False
    if tf:
        能量豆产阳光(give)


def 能量豆产阳光(give):

    for i in range(0, len(give), 4):
        cls = give[i]  # 标签  保险起见可以加转换类型float(), int()等
        if cls in var.sun_to_sum:   # 等于光植
            x = give[i + 2]
            y = give[i + 3]
            conf = give[i + 1]  # 置信值
            if conf > 0.5 and var.grid_Scale_x1 < x < var.grid_Scale_x + var.grid_Scale_x1 and var.grid_Scale_y1 < y < var.grid_Scale_y + var.grid_Scale_y1:  # 置信度阈值，且在格子内  因为var.grid_Scale_x(y)是范围，所以加回去
                x1 = round(var.energy_x * (var.pixel[2] - var.pixel[0]) + var.pixel[0])  # 能量豆储存的第一个绿点的坐标  其实不用准确点击叶子，点击绿点也可以
                y1 = round(var.energy_y * (var.pixel[3] - var.pixel[1]) + var.pixel[1])

                x2 = round(var.pixel[0] + x * (var.pixel[2] - var.pixel[0]))  # 要点击的实际坐标
                y2 = round(var.pixel[1] + y * (var.pixel[3] - var.pixel[1]))  # round四舍五入
                click(x1, y1)   # 点击能量豆
                click(x2, y2)   # 点击光植（向日葵）
                out_text(f"能量豆-向日葵产能，x={x2},y={y2}")


def 吞噬墓碑(give):
    for p in var.Swallower_to_sum:
        if var.Card[p][0] == 1:  # 如果墓碑吞噬者就绪

            for i in range(0, len(give), 4):
                cls = give[i]  # 标签
                if cls in var.Tombstone_to_sum:  # 等于墓碑
                    x = give[i + 2]
                    y = give[i + 3]
                    conf = give[i + 1]  # 置信值
                    if conf > 0.5 and var.grid_Scale_x1 < x < var.grid_Scale_x + var.grid_Scale_x1 and var.grid_Scale_y1 < y < var.grid_Scale_y + var.grid_Scale_y1:  # 置信度阈值，且在格子内  因为var.grid_Scale_x(y)是范围，所以加回去
                        x1 = round(var.Card_x * (var.pixel[2] - var.pixel[0]) + var.pixel[0])  # 要点击的卡片坐标
                        y1 = round(var.Card[p][1])

                        x2 = round(var.pixel[0] + x * (var.pixel[2] - var.pixel[0]))  # 要点击的实际坐标
                        y2 = round(var.pixel[1] + y * (var.pixel[3] - var.pixel[1]))  # round四舍五入
                        out_text(f"吞噬墓碑x{x2}, y{y2}")
                        click(x1, y1)  # 点击 墓碑卡
                        click(x2, y2)  # 点击墓碑


def 强制放置攻植(grid):
    for p in var.att_to_sum:
        if var.Card[p][0] == 1:  # 判断是否有攻植准备就绪

            for x in var.攻植种植列:
                for fy, celly in enumerate(grid):  # 行

                    if grid[fy][x]['p'] == 2 or grid[fy][x]['p'] == 3:   #如果为光植 或 生菜
                        铲除(x, fy)
                        放置(p, x, fy)
                        return  # 放置后立即退出def
        else:
            放置攻植(grid, -1)
            return  # 放置后立即退出def


def 铲除(x, fy):
    x1 = round(var.shovel_x * (var.pixel[2] - var.pixel[0]) + var.pixel[0])  # 铲子的坐标
    y1 = round(var.shovel_y * (var.pixel[3] - var.pixel[1]) + var.pixel[1])

    x2 = round(var.grid_x[x] * (var.pixel[2] - var.pixel[0]) + var.pixel[0])  # 要点击的实际坐标   grid_x=列的坐标
    y2 = round(var.grid_y[fy] * (var.pixel[3] - var.pixel[1]) + var.pixel[1])  # grid_y=行的坐标
    out_text(f"强制放置攻植，铲除植物-{fy+1}行, {x+1}列")
    click(x1, y1)  # 点击 铲子
    click(x2, y2)  # 点击 对应植物

