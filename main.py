from Window import 显示窗口, 处理帧与格子, out_text
from play import 拾取, 放置植物, 使用能量豆, 吞噬墓碑
from click import 更新窗口与分辨率
from rec import give_sun_xy
import var
from grid import grid_check
from time import sleep

if __name__ == '__main__':

    grid1 = var.grid
    显示窗口()
    更新窗口与分辨率()

    while True:

        sleep(var.执行延迟)
        更新窗口与分辨率()
        give, result, suns, game = give_sun_xy()

        #game = 判断是否处于游戏中
        if game:        # 如果在游戏中，则执行操作

            var.无光阶段_t = 0

            拾取(give)
            grid1 = grid_check(give, grid1)  # 更新格子状态
            放置植物(grid1, suns)
            吞噬墓碑(give)
            使用能量豆(give)
        else:
            var.无光阶段_t = var.无光阶段_t + 1     #不处于游戏 400tick 后，重置无光阶段
            if var.无光阶段_t > 400:
                out_text(f'重置"无光阶段"')
                var.无光阶段 = 0
                var.无光阶段_t = 0


        处理帧与格子(result, grid1, suns)  # 显示帧与格子


