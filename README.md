

# care4programmer
期末python大作业的拙作

一个基于mediapipe的使用摄像头进行实时疲劳检测和坐姿检测的提醒小工具<br>

作者: jsu-lyy<br>

<a href="https://github.com/AnWAmaster/care4programmer">仓库地址</a>
# 环境
python=3.8.5<br>
mediapipe==0.8.9.1<br>
opencv_python==4.5.5.64<br>
PySimpleGUI==4.60.4<br>
PyYAML==6.0<br>

# 打包方式
1. `pip install pyinstaller`

2. 参考下方博客进行mediapipe源码的改动，最后记得添加`import sys`，博主忘写这个了<br>
    <a href="https://blog.csdn.net/weixin_43790779/article/details/125626377?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522167007426816800213011359%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=167007426816800213011359&biz_id=&utm_medium=distribute.pc_search_result.none-task-code-2~all~first_rank_ecpm_v1~rank_v31_ecpm-2-125626377-4-null-null.142^v67^control,201^v3^control,213^v2^t3_esquery_v1&utm_term=FileNotFoundError%3A%20The%20path%20does%20not%20exist.">使用pyinstaller打包Mediapipe项目时遇到FileNotFoundError: The path does not exist的解决方法</a>

3. 执行打包命令 
    `pyinstaller -F -w main.py -p gui.py -p judger.py -p observer.py --icon=favicon.ico -n main`

    该命令意思是：将多个py文件打入一个exe，去除运行时的黑窗，以main.py为入口，并设置icon图标，并设置输出文件为main.exe

4. 将`config.yml`和`mediapipe文件夹`放入dist中

5. 测试运行`main.exe`

6. <font color="red">因为一些历史遗留问题，该可执行文件路径上不要出现中文！</font>
