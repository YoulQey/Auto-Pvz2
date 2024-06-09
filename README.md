# 使用效果 / Usage effect
![](https://github.com/YoulQey/U7-File/blob/main/Auto-Pvz-gif1.gif)
## 触发了游戏原本的BUG / Triggered the original bug in the game
![](https://github.com/YoulQey/U7-File/blob/main/Auto-Pvz-gif2.gif)

CN
# 声明
此脚本仅供学习与个人纪念记录。blibili视频：https://www.bilibili.com/video/BV1PZ421g7Rz

# 运行说明
运行环境与库写在了`requirements.txt`
直接运行 `main.py` 即可

# 功能
窗口使用qt5，可实时显示预测结果，帧数，格子状态，卡片冷却状态等
已实现自动收集阳光与使用能量豆，自动部署植物，自动吞噬墓碑，卷心菜准确冰冻，阳光过多-替换向日葵......等

使用比例坐标-分辨率与窗口大小不限，
可在运行时-随时变动分辨率。演示使用分辨率:`2534*1440`（限制 15.84 : 9 比例下使用）

# 说明
目前还只会基本代码，拿pvz2来做练习，Yolo训练模型为143张图片，2543个标注。
模型网站: [pvz2 Dataset > Overview (roboflow.com)](https://universe.roboflow.com/pvz2/pvz2)

从0基础开始学习Python与yolo-v8 到 Pvz2脚本 正式完结耗时10天；肝不动了O_o
使用了 GPT4 与 Claude3 辅助学习

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
EN
# Declaration
This script is for learning and personal commemoration purposes only. Bilibili video: https://www.bilibili.com/video/BV1PZ421g7Rz

# Instructions
The runtime environment and libraries are listed in `requirements.txt`. Simply run `main.py`.

# Features
Window uses Qt5 and can display real-time prediction results, frame rate, grid status, card cooldown status, and more.
Implemented features include automatic collection of sunlight and use of energy beans, automatic plant deployment, automatic tombstone consumption, accurate freezing with cabbage, sunflower replacement when sunlight is excessive, and more.

Using proportional coordinates - resolution and window size are not limited, and resolution can be changed at any time during runtime. Demonstration resolution: `2534*1440` (limited to a 15.84:9 ratio).

# Notes
Currently, I only know basic coding and am using PvZ2 for practice. The Yolo training model consists of 143 images and 2543 annotations. Model website: [pvz2 Dataset > Overview (roboflow.com)](https://universe.roboflow.com/pvz2/pvz2)

It took 10 days to learn Python and Yolo-v8 from scratch to complete the Pvz2 script; I can't keep up anymore O_o. Used GPT-4 and Claude3 for learning assistance.
