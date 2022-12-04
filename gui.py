import time

import PySimpleGUI as sg
import cv2
import mediapipe as mp
import winsound
import sqlite3


# 图像化窗口
class Window:
    def __init__(self, param):
        # 获取所有可用主题，返回一个列表
        # theme_name_list = sg.theme_list()
        # total = {}
        # for i in theme_name_list:
        #     for j in theme_prefix_list:
        #         if i.startswith(j):
        #             if total.get(j) is None:
        #                 total[j]=[]
        #             total[j].append(i)
        # asdf = []
        # for key,value in total.items():
        #     asdf.append(key)
        #     asdf.append(value)
        # print(asdf)
        '''
        # 主题
        '''
        theme = self.__get_theme()
        if theme is None:
            sg.theme('Default1')
        else:
            sg.theme(theme[1])
        theme_name_list = ['Black', ['Black'], 'Blue', ['BlueMono', 'BluePurple'], 'Bright', ['BrightColors'], 'Brown',
                           ['BrownBlue'], 'Dark',
                           ['Dark', 'Dark2', 'DarkAmber', 'DarkBlack', 'DarkBlack1', 'DarkBlue', 'DarkBlue1',
                            'DarkBlue10', 'DarkBlue11', 'DarkBlue12', 'DarkBlue13', 'DarkBlue14', 'DarkBlue15',
                            'DarkBlue16', 'DarkBlue17', 'DarkBlue2', 'DarkBlue3', 'DarkBlue4', 'DarkBlue5', 'DarkBlue6',
                            'DarkBlue7', 'DarkBlue8', 'DarkBlue9', 'DarkBrown', 'DarkBrown1', 'DarkBrown2',
                            'DarkBrown3', 'DarkBrown4', 'DarkBrown5', 'DarkBrown6', 'DarkBrown7', 'DarkGreen',
                            'DarkGreen1', 'DarkGreen2', 'DarkGreen3', 'DarkGreen4', 'DarkGreen5', 'DarkGreen6',
                            'DarkGreen7', 'DarkGrey', 'DarkGrey1', 'DarkGrey10', 'DarkGrey11', 'DarkGrey12',
                            'DarkGrey13', 'DarkGrey14', 'DarkGrey15', 'DarkGrey2', 'DarkGrey3', 'DarkGrey4',
                            'DarkGrey5', 'DarkGrey6', 'DarkGrey7', 'DarkGrey8', 'DarkGrey9', 'DarkPurple',
                            'DarkPurple1', 'DarkPurple2', 'DarkPurple3', 'DarkPurple4', 'DarkPurple5', 'DarkPurple6',
                            'DarkPurple7', 'DarkRed', 'DarkRed1', 'DarkRed2', 'DarkTanBlue', 'DarkTeal', 'DarkTeal1',
                            'DarkTeal10', 'DarkTeal11', 'DarkTeal12', 'DarkTeal2', 'DarkTeal3', 'DarkTeal4',
                            'DarkTeal5', 'DarkTeal6', 'DarkTeal7', 'DarkTeal8', 'DarkTeal9'], 'Default',
                           ['Default', 'Default1', 'DefaultNoMoreNagging'], 'Gray', ['GrayGrayGray'], 'Green',
                           ['Green', 'GreenMono', 'GreenTan'], 'HotDogStand', ['HotDogStand'], 'Kayak', ['Kayak'],
                           'Light', ['LightBlue', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4', 'LightBlue5',
                                     'LightBlue6', 'LightBlue7', 'LightBrown', 'LightBrown1', 'LightBrown10',
                                     'LightBrown11', 'LightBrown12', 'LightBrown13', 'LightBrown2', 'LightBrown3',
                                     'LightBrown4', 'LightBrown5', 'LightBrown6', 'LightBrown7', 'LightBrown8',
                                     'LightBrown9', 'LightGray1', 'LightGreen', 'LightGreen1', 'LightGreen10',
                                     'LightGreen2', 'LightGreen3', 'LightGreen4', 'LightGreen5', 'LightGreen6',
                                     'LightGreen7', 'LightGreen8', 'LightGreen9', 'LightGrey', 'LightGrey1',
                                     'LightGrey2', 'LightGrey3', 'LightGrey4', 'LightGrey5', 'LightGrey6',
                                     'LightPurple', 'LightTeal', 'LightYellow'], 'Material', ['Material1', 'Material2'],
                           'Neutral', ['NeutralBlue'], 'Purple', ['Purple'], 'Python', ['Python', 'PythonPlus'],
                           'Reddit', ['Reddit'], 'Reds', ['Reds'], 'SandyBeach', ['SandyBeach'], 'System',
                           ['SystemDefault', 'SystemDefault1', 'SystemDefaultForReal'], 'Tan', ['Tan', 'TanBlue'],
                           'TealMono', ['TealMono'], 'Topanga', ['Topanga']]
        '''
        定义菜单栏
        '''
        menu_def = [['切换主题', theme_name_list], ['预览', ['全部主题']]]
        ''' 
        定义窗口布局
        '''
        layout = [
            [sg.Menu(menu_def)],
            [sg.Image(filename='', key='video')],
            [sg.Text('闭眼值'), sg.Text('', key='ear'), sg.Text('下阈值'), sg.Text('', key='ear_threshold'), sg.Text('超时时间'),
             sg.Text('', key='close_eye_time_gap')],
            [sg.Text('张嘴值'), sg.Text('', key='mar'), sg.Text('上阈值'), sg.Text('', key='mar_threshold'), sg.Text('超时时间'),
             sg.Text('', key='open_mouth_time_gap')],
            [sg.Text('低头抬头值'), sg.Text('', key='up_down_head_val'), sg.Text('上阈值'),
             sg.Text('', key='up_down_head_threshold_up'), sg.Text('下阈值'),
             sg.Text('', key='up_down_head_threshold_down'), sg.Text('点头超时时间'),
             sg.Text('', key='up_down_head_time_gap'), sg.Text('低头抬头超时时间'),
             sg.Text('', key='keep_up_down_head_time_gap')],
            [sg.Text('歪脖子值'), sg.Text('', key='wryneck_val'), sg.Text('上阈值'), sg.Text('', key='wryneck_threshold_up'),
             sg.Text('下阈值'), sg.Text('', key='wryneck_threshold_down'), sg.Text('超时时间'),
             sg.Text('', key='wryneck_time_gap')],
            [sg.Text('歪肩膀值'), sg.Text('', key='wryshoulder_val'), sg.Text('上阈值'),
             sg.Text('', key='wryshoulder_threshold_up'), sg.Text('下阈值'), sg.Text('', key='wryshoulder_threshold_down'),
             sg.Text('超时时间'), sg.Text('', key='wryshoulder_time_gap')],
            [sg.Text('侧头值'), sg.Text('', key='lateralize_head_val'), sg.Text('上阈值'),
             sg.Text('', key='lateralize_head_threshold'), sg.Text('超时时间'),
             sg.Text('', key='lateralize_head_time_gap')],
            [sg.Text('左手手势'), sg.Text('', key='left_hand_val')],
            [sg.Text('右手手势'), sg.Text('', key='right_hand_val')],
            # [sg.Text('手掌休眠超时时间'), sg.Text('', key='open_palm_2sleep_time_gap')],
            [sg.Text('警告模式：')],
            [sg.Radio('无', 2, enable_events=True, key="no_warning", size=(10, 1), default=True),
             sg.Radio('蜂鸣', 2, enable_events=True, key="beep_warning", size=(10, 1)),
             sg.Radio('弹窗', 2, enable_events=True, key="popup_warning", size=(10, 1))],
            [sg.Text('展示定位点：')],
            [sg.Radio('无', 1, enable_events=True, key="no_landmarks", size=(10, 1), default=True),
             sg.Radio('全部', 1, enable_events=True, key="all_landmarks", size=(10, 1)),
             sg.Radio('自选', 1, enable_events=True, key="choose_landmarks", size=(10, 1))],
            [sg.Checkbox('脸部', enable_events=True, key="face_landmarks", size=(10, 1), visible=False),
             sg.Checkbox('脸部(网格)', enable_events=True, key="face_mesh_landmarks", size=(10, 1), visible=False),
             sg.Checkbox('姿态', enable_events=True, key="pose_landmarks", size=(10, 1), visible=False),
             sg.Checkbox('手掌', enable_events=True, key="hand_landmarks", size=(10, 1), visible=False)],
            # [sg.Checkbox('开启疲劳检测',default=True), sg.Checkbox('开启坐姿检测',default=True)],
            [sg.Button('开始', size=(10, 1), key="stop_continue_btn"), sg.Button('结束', size=(10, 1), key="end")]
        ]
        '''
        窗口设计
        '''
        self.window = sg.Window('care4程序员',
                                layout,
                                location=(600, 30),
                                finalize=True, grab_anywhere=True)
        '''
        一些参数和画图工具
        '''
        self.previous_time = 0
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_holistic = mp.solutions.holistic
        self.show_landmarks = []
        self.warning_mode = "no_warning"
        '''
        重新加载主题后还要更改暂停继续按钮的初始值为暂停
        '''
        if param.gui_started == True:
            self.window["stop_continue_btn"].update(text="暂停")

    '''
    每一帧更新界面数据
    '''

    def update(self, img, landmarks, _landmarks, param, data):
        # 获取事件
        event, values = self.window.read(timeout=0, timeout_key='no event')
        # 点了叉或结束按钮
        if event is sg.WIN_CLOSED or event == 'end':
            self.window.close()
            param.is_started = False
            return param
        # 点了开始暂停继续按钮
        if event == "stop_continue_btn":
            if self.window["stop_continue_btn"].ButtonText == "开始":
                param.gui_started = True
                self.window["stop_continue_btn"].update(text="暂停")
            elif self.window["stop_continue_btn"].ButtonText == "暂停":
                param.gui_started = False
                self.window["stop_continue_btn"].update(text="继续")
            else:
                param.gui_started = True
                self.window["stop_continue_btn"].update(text="暂停")
        # 展示全部主题
        if event == '全部主题':
            sg.theme_previewer()
        # 选中了某个主题后进行切换
        if event in sg.theme_list():
            self.__save_theme(event)
            self.window.close()
            param.restart_gui = True
            return param
        # 警告模式的选择
        if event == 'no_warning':
            self.warning_mode = 'no_warning'
        elif event == 'beep_warning':
            self.warning_mode = 'beep_warning'
        elif event == 'popup_warning':
            self.warning_mode = 'popup_warning'
        #
        # if param.gui_started == None:
        #     self.window["stop_continue_btn"].update(text="开始")
        # 图形化界面更新ing
        if param.gui_started == True:
            # 获得处理后的图像并展示在界面上
            img = self.__process_img(img, landmarks, _landmarks, param, data, event, values)
            self.window["video"].update(data=cv2.imencode('.png', img)[1].tobytes())
            # 依据judger判断后的结果和警告模式进行警告
            self.warn(data)
        return param

    # 处理图像
    def __process_img(self, img, landmarks, _landmarks, param, data, event, values):
        # 显示各参数值
        # 闭眼值
        self.window["ear"].update(round(data.ear * 10, 2))
        self.window["ear_threshold"].update(round(param.close_eye_threshold * 10, 2))
        self.window["close_eye_time_gap"].update(param.close_eye_time_gap)
        # 张嘴值
        self.window["mar"].update(round(data.mar * 100, 2))
        self.window["mar_threshold"].update(round(param.open_mouth_threshold * 100))
        self.window["open_mouth_time_gap"].update(param.open_mouth_time_gap)
        # 低头抬头值
        self.window["up_down_head_val"].update(data.up_down_head_val - param.up_down_head_threshold_down)
        self.window['up_down_head_threshold_up'].update(
            param.up_down_head_threshold_up - param.up_down_head_threshold_down)
        self.window['up_down_head_threshold_down'].update(
            param.up_down_head_threshold_down - param.up_down_head_threshold_down)
        self.window["up_down_head_time_gap"].update(param.up_down_head_time_gap)
        self.window["keep_up_down_head_time_gap"].update(param.keep_up_down_head_time_gap)
        # 歪脖子值
        self.window["wryneck_val"].update(data.wryneck_val)
        self.window["wryneck_threshold_up"].update(param.wryneck_threshold_up)
        self.window["wryneck_threshold_down"].update(param.wryneck_threshold_down)
        self.window["wryneck_time_gap"].update(param.wryneck_time_gap)
        # 歪肩膀值
        self.window["wryshoulder_val"].update(data.wryshoulder_val)
        self.window['wryshoulder_threshold_up'].update(param.wryshoulder_threshold_up)
        self.window['wryshoulder_threshold_down'].update(param.wryshoulder_threshold_down)
        self.window["wryshoulder_time_gap"].update(param.wryshoulder_time_gap)
        # 侧头值
        self.window["lateralize_head_val"].update(round(data.lateralize_head_val, 2))
        self.window['lateralize_head_threshold'].update(param.lateralize_head_threshold)
        self.window["lateralize_head_time_gap"].update(param.lateralize_head_time_gap)
        # 手势识别结果
        self.window["left_hand_val"].update(data.left_hand_val)
        self.window["right_hand_val"].update(data.right_hand_val)
        # self.window["open_palm_2sleep_time_gap"].update(param.open_palm_2sleep_time_gap)
        # 选择了要显示哪些定位点
        if event == 'all_landmarks':
            self.show_landmarks = ['face', 'pose', 'hand']
            self.window["face_landmarks"].update(visible=False, value=False)
            self.window["face_mesh_landmarks"].update(visible=False, value=False)
            self.window["pose_landmarks"].update(visible=False, value=False)
            self.window["hand_landmarks"].update(visible=False, value=False)
        elif event == 'no_landmarks':
            self.show_landmarks = []
            self.window["face_landmarks"].update(visible=False, value=False)
            self.window["face_mesh_landmarks"].update(visible=False, value=False)
            self.window["pose_landmarks"].update(visible=False, value=False)
            self.window["hand_landmarks"].update(visible=False, value=False)
        elif event == 'choose_landmarks':
            self.show_landmarks = []
            self.window["face_landmarks"].update(visible=True)
            self.window["face_mesh_landmarks"].update(visible=True)
            self.window["pose_landmarks"].update(visible=True)
            self.window["hand_landmarks"].update(visible=True)
        elif event == 'face_landmarks':
            if self.window["face_landmarks"].get():
                self.show_landmarks.append('face')
            else:
                self.show_landmarks.remove('face')
        elif event == 'face_mesh_landmarks':
            if self.window["face_mesh_landmarks"].get():
                self.show_landmarks.append('face_mesh')
            else:
                self.show_landmarks.remove('face_mesh')
        elif event == 'pose_landmarks':
            if self.window["pose_landmarks"].get():
                self.show_landmarks.append('pose')
            else:
                self.show_landmarks.remove('pose')
        elif event == 'hand_landmarks':
            if self.window["hand_landmarks"].get():
                self.show_landmarks.append('hand')
            else:
                self.show_landmarks.remove('hand')
        # 显示手势识别的结果
        if param.allow_identify_hand:
            if data.left_hand_val:
                cv2.putText(img, f'{data.left_hand_val}', (10, 90), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
            if data.right_hand_val:
                cv2.putText(img, f'{data.right_hand_val}', (10, 130), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255),
                            3)
            # 原先做了张开手掌几秒后使电脑休眠的，但是太恶心了就不加了
            # if param.open_palm_2sleep:
            #     if (data.left_hand_val and data.left_hand_val == "five") or (
            #             data.right_hand_val and data.right_hand_val == "five"):
            #         param.is_started = False
            #         time.sleep(5)
            #         os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
        # 显示帧率
        self.__put_fps(img)
        # 人头定位椭圆
        cv2.ellipse(img, (320, 170), (120, 100), 90, 0, 360, (255, 255, 255), 2)
        cv2.putText(img, 'Head', (260, 40), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)
        # 根据选定的显示定位点的值，判断是否展示各部分定位点
        if 'face' in self.show_landmarks:
            if _landmarks['face']:
                self.mp_drawing.draw_landmarks(img, _landmarks['face'], self.mp_holistic.FACEMESH_CONTOURS,
                                               landmark_drawing_spec=None,
                                               connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_contours_style())
        if 'face_mesh' in self.show_landmarks:
            if _landmarks['face']:
                self.mp_drawing.draw_landmarks(img, _landmarks['face'], self.mp_holistic.FACEMESH_CONTOURS,
                                               connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_contours_style())
        if 'pose' in self.show_landmarks:
            if _landmarks['pose']:
                self.mp_drawing.draw_landmarks(img, _landmarks['pose'], self.mp_holistic.POSE_CONNECTIONS,
                                               landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style())
        if 'hand' in self.show_landmarks:
            if _landmarks['left_hand']:
                self.mp_drawing.draw_landmarks(img, _landmarks['left_hand'], self.mp_holistic.HAND_CONNECTIONS)
            if _landmarks['right_hand']:
                self.mp_drawing.draw_landmarks(img, _landmarks['right_hand'], self.mp_holistic.HAND_CONNECTIONS)
        return img

    '''
    计算帧率并放入图片
    '''

    def __put_fps(self, img):
        cur_time = time.time()
        fps = 1 / (cur_time - self.previous_time)
        self.previous_time = cur_time
        cv2.putText(img, f'FPS: {int(fps)}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        return img

    '''
    根据judger判断的结果，返回警告信息
    '''

    def judge_warning(self, data):
        if data.eye_closed:
            return "打起精神！"
        elif data.mouth_opened:
            return "打起精神！"
        elif data.up_down_head:
            return "打起精神！"
        elif data.keep_up_down_head:
            return "注意头要和电脑平行哦！"
        elif data.wryneck:
            return "把头摆正！"
        elif data.wryshoulder:
            return "肩膀别歪了！"
        elif data.lateralize_head:
            return "把头摆正！"
        else:
            return None

    '''
    根据选择的模式进行警告
    '''

    def warn(self, data):
        res = self.judge_warning(data)
        if res != None and self.warning_mode != 'no_warning':
            if self.warning_mode == 'beep_warning':
                self.__beep_warning()
            elif self.warning_mode == 'popup_warning':
                self.__popup_warning(res)

    '''
    弹窗警告
    '''

    def __popup_warning(self, text):
        sg.Popup(text, keep_on_top=True, modal=True, no_titlebar=True,custom_text=("OK"))

    '''
    蜂鸣警告
    '''

    def __beep_warning(self):
        winsound.Beep(3500, 300)

    '''
    读入上一次保存的主题
    '''

    def __save_theme(self, theme):
        conn = sqlite3.connect("care4programmer.db")
        c = conn.cursor()
        # 建表
        sql = "CREATE TABLE IF NOT EXISTS theme(id INTEGER UNIQUE,theme TEXT);"
        c.execute(sql)
        # 插入
        sql = "REPLACE INTO theme(id,theme) VALUES(?,?)"
        data = (1, theme)
        c.execute(sql, data)
        conn.commit()
        c.close()
        conn.close()

    '''
    将主题持久化进数据库
    '''

    def __get_theme(self):
        conn = sqlite3.connect("care4programmer.db")
        c = conn.cursor()
        # 建表
        sql = "CREATE TABLE IF NOT EXISTS theme(id INTEGER UNIQUE,theme TEXT);"
        c.execute(sql)
        # 插入
        sql = "SELECT * FROM theme LIMIT 1;"
        c.execute(sql)
        theme = c.fetchone()
        conn.commit()
        c.close()
        conn.close()
        return theme

    '''
    未检测到摄像头时进行弹窗报错
    '''

    def remind_camera_not_found(self, param):
        event, values = self.window.read(timeout=0, timeout_key='timeout')
        if event is sg.WIN_CLOSED or event == 'end':
            self.window.close()
            param.is_started = False
        else:
            clicked = sg.Popup("未检测到摄像头", keep_on_top=True, modal=True, no_titlebar=True,
                               background_color="pink", text_color='black', custom_text=("retry", "close"))
            if clicked == "close":
                param.is_started = False
        return param
