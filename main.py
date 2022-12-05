import traceback

import yaml

from observer import Observer
from judger import Judger
from gui import Window


# 负责调度各模块
class Director:
    def __init__(self):
        with open('config.yml', 'r', encoding="utf-8") as f:
            file_data = f.read()
        config = yaml.load(file_data, Loader=yaml.FullLoader)
        self.config = Config(config)
        self.data = Data()
        self.param = Param()
        self.window = Window(self.param)
        self.observer = Observer()
        self.judger = Judger()

    def start(self):
        img, landmarks, _landmarks = None,None,None
        self.param.is_started = True
        # 项目正在进行中
        while self.param.is_started:
            try:
                # 重新加载主题
                if self.param.restart_gui == True:
                    self.window = Window(self.param)
                    self.param.restart_gui = False
                # 解析当前图像
                if self.param.gui_started == True:
                    img, landmarks, _landmarks, self.data = self.observer.observe(self.config, self.param, self.data)
            except:
                # 此处抛异常是未检测到摄像头
                # 于是进行弹窗提醒
                self.param = self.window.remind_camera_not_found(self.param)
                # 重新加载摄像头
                if self.param.is_started == True:
                    self.observer.refresh_camera()
            else:
                # 正常流程
                # 先给解析到的结果给judger，得到是否有疲劳、坐姿不正确现象
                if self.param.gui_started == True:
                    self.data = self.judger.judge(self.param, self.data)
                # 把数据更新到图形界面上
                self.param = self.window.update(img,  _landmarks, self.param, self.data)
                # 每一帧都重置数据
                self.data.clear()
        print("结束")

# 配置文件中的参数
class Config:
    def __init__(self, data):
        self.face_left_eye = data['face_left_eye']
        self.face_right_eye = data['face_right_eye']
        self.face_lip = data['face_lip']
        self.pose_mouth = data['pose_mouth']
        self.pose_nose = data['pose_nose']
        self.pose_eye = data['pose_eye']
        self.face_cheek = data['face_cheek']
        self.pose_cheek = data['pose_cheek']
        self.pose_shoulder = data['pose_shoulder']
        self.finger = data['finger']


# 一些辅助用的参数
class Param:
    def __init__(self):
        # 系统开关
        self.is_started = None
        self.gui_started = None
        self.restart_gui = False
        # 疲劳检测
        ## 闭眼
        self.close_eye_time_gap = 3
        self.close_eye_last_time = None
        self.close_eye_threshold = 0.2
        ## 打哈欠
        self.open_mouth_threshold = 0.50
        self.open_mouth_time_gap = 1
        self.open_mouth_last_time = None
        ## 上下动头
        self.up_down_head_threshold_down = 12
        self.up_down_head_threshold_up = 37
        self.up_down_head_time_gap = 3
        self.up_down_head_last_time = None
        # 坐姿检测
        ## 一直低头抬头
        self.keep_up_down_head_time_gap = 8
        self.keep_up_down_head_last_time = None
        ## 歪头
        self.wryneck_threshold_up = 10
        self.wryneck_threshold_down = -10
        self.wryneck_time_gap = 1
        self.wryneck_last_time = None
        ## 歪肩膀
        self.wryshoulder_threshold_up = 40
        self.wryshoulder_threshold_down = -40
        self.wryshoulder_time_gap = 3
        self.wryshoulder_last_time = None
        # 侧头
        self.lateralize_head_threshold = 45
        self.lateralize_head_time_gap = 2
        self.lateralize_head_last_time = None
        # 手势识别
        self.allow_identify_hand = True
        self.open_palm_2sleep = True
        self.open_palm_2sleep_time_gap = 5
        self.open_palm_2sleep_last_time = None


# 计算得到的以及要放在页面上的
class Data:
    def __init__(self):
        self.ear = 0
        self.mar = 0
        self.up_down_head_val = 0
        self.wryneck_val = 0
        self.wryshoulder_val = 0
        self.lateralize_head_val = 0
        self.left_hand_val = 'None'
        self.right_hand_val = 'None'
        self.eye_closed = False
        self.mouth_opened = False
        self.up_down_head = False
        self.keep_up_down_head = False
        self.wryneck = False
        self.wryshoulder = False
        self.lateralize_head = False
        self.open_palm_2sleep = False

    def clear(self):
        self.ear = 0
        self.mar = 0
        self.up_down_head_val = 0
        self.wryneck_val = 0
        self.wryshoulder_val = 0
        self.lateralize_head_val = 0
        self.left_hand_val = 'None'
        self.right_hand_val = 'None'
        self.eye_closed = False
        self.mouth_opened = False
        self.up_down_head = False
        self.keep_up_down_head = False
        self.wryneck = False
        self.wryshoulder = False
        self.lateralize_head = False
        self.open_palm_2sleep = False

if __name__ == '__main__':
    director = Director()
    director.start()
    # pyinstaller -F -w main.py -p gui.py -p judger.py -p observer.py --icon=favicon.ico -n main