import var
from var import 植物, 僵尸, grid_range_x, grid_range_y, grid_Scale_x1, grid_Scale_y1
from rec import 判断植物卡是否可用
from Window import out_text

def grid_check(give, grid):

    for i in range(7):     #将所有卡片显示 变成不可用状态
        var.Card_tf[i] = False

    for i in range(len(var.Card)):     #将所有卡片 变成不可用状态
        var.Card[i] = [0, 0]

    for g in var.plant:
            g[0] = 0

    for row in grid:
        for cell in row:
            if cell['p'] != 0:      # 有植物就计时
                cell['p_t'] += 1

            if cell['z'] == 1:
                cell['z_t'] += 1


    for i in range(0, len(give), 4):
        cls = give[i]       #标签
        conf = give[i + 1]    #置信值   #保险起见可以加转换类型float(), int()等

        if conf > 0.5 and cls != var.拾取物:  # 置信度阈值  以及不等于拾取物
            x = give[i + 2]
            y = give[i + 3]

            # 确定格子坐标
            grid_x_index = next((index for index, value in enumerate(grid_range_x) if grid_Scale_x1 < x <= value), None)     # 生成器，如果满足 坐标x大于格子的左上角x，以及小于等于遍历的grid_range_x，则等于index索引数的格子
            grid_y_index = next((index for index, value in enumerate(grid_range_y) if grid_Scale_y1 < y <= value), None)      # 生成器，如果满足 坐标y大于格子的左上角y，以及小于等于遍历的grid_range_y，则等于index索引数的格子
            # print(f"输出x ={x},y ={y}")
            # print(f"输出grid_x_index ={grid_x_index},grid_y_index ={grid_y_index}")

            if grid_x_index is not None and grid_y_index is not None:   # 如果对象在格子里

                if cls in 植物:  # 如果判断为植物
                    if cls in var.att_to_sum:   # 如果为攻植
                        grid[grid_y_index][grid_x_index]['p'] = 1       # 1为攻植
                    elif cls in var.boom_to_sum:
                        grid[grid_y_index][grid_x_index]['p'] = 3       # 3为瞬发植物，卷心菜等
                    elif cls in var.Tombstone_to_sum:   # 如果为墓碑
                        grid[grid_y_index][grid_x_index]['p'] = 4       # 4为墓碑
                    elif cls in var.sun_to_sum:   # 如果为光植
                        grid[grid_y_index][grid_x_index]['p'] = 2       # 2为光植
                    else:
                        grid[grid_y_index][grid_x_index]['p'] = 5       # 4为其他植物

                    grid[grid_y_index][grid_x_index]['p_t'] = 0  # 重置计数器

                    var.plant[cls][0] = var.plant[cls][0] + 1   #统计植物数量

                elif cls in 僵尸:  # 假设2代表僵尸
                    grid[grid_y_index][grid_x_index]['z'] = 1
                    grid[grid_y_index][grid_x_index]['z_t'] = 0  # 重置计数器
            elif x < var.Card_x1 and cls in var.植物:      # 如果是植物并且在卡片范围
                # 确定卡片坐标
                Card_y_index = next((index for index, value in enumerate(var.Card_range_y) if var.Card_Scale_y1 < y < value), None)  # 生成器，小于等于遍历的Card_range_y，则等于index索引数的格子
                if Card_y_index is not None:
                    var.Card[cls][1] = round(var.Card_y[Card_y_index] * (var.pixel[3] - var.pixel[1]) + var.pixel[1])     # 确定某植物卡片的y坐标
                    var.Card[cls][0] = 判断植物卡是否可用(cls)
                    if var.Card[cls][0] == 1:
                        # print(f"输出：var.Card_tf[{Card_y_index}] = True")
                        var.Card_tf[Card_y_index] = True    #只是为了显示卡片状态
                    else:
                        var.Card_tf[Card_y_index] = False

    p_tick = 12  # 计时器阈值

    # 缓冲光植与攻植变动
    var.攻植_t = var.攻植_t + 1
    var.光植_t = var.光植_t + 1
    # print(f"var.攻植_t:{var.攻植_t},var.光植_t :{var.光植_t }")
    #分类植物
    预光植 = var.sum_plant(var.plant, var.sun_to_sum)      #设定阈值，防止跳动
    预攻植 = var.sum_plant(var.plant, var.att_to_sum)

    if 预光植 >= var.光植:
        var.光植_t = 0
        var.光植 = 预光植
    elif var.光植_t >= p_tick:
        var.光植_t = 0
        var.光植 = 预光植

    if 预攻植 >= var.攻植:
        var.攻植_t = 0
        var.攻植 = 预攻植
    elif var.攻植_t >= p_tick:
        var.攻植_t = 0
        var.攻植 = 预攻植

    tick = 10  # 计时器阈值
    for row in grid:
        for cell in row:
            if cell['p_t'] >= tick:
                cell['p'] = 0
                cell['p_t'] = 0
            if cell['z_t'] >= tick:
                cell['z'] = 0
                cell['z_t'] = 0
    return grid
