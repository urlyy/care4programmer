import math

import cv2
import mediapipe as mp


# config为提前的配置，如目标点的下标
# param用来辅助判断，如上次的时间、阈值等
# data为计算出的值

# 获得摄像头传来的图像，并进行解析和关键点运算
class Observer:
    def __init__(self):
        self.holistic = mp.solutions.holistic.Holistic()
        self.denormalize_coordinates = mp.solutions.drawing_utils._normalized_to_pixel_coordinates
        self.cap = cv2.VideoCapture(0)

    def refresh_camera(self):
        self.cap = cv2.VideoCapture(0)

    # 闭眼
    def __ear(self, all_landmarks, config, img_height, img_width):
        landmarks = all_landmarks['face']
        try:
            # 得到各定位点间的距离
            left_coords_points = self.__denormalize(landmarks, config.face_left_eye, img_height, img_width)
            left_P2_P6 = self.__distance(left_coords_points[1], left_coords_points[5])
            left_P3_P5 = self.__distance(left_coords_points[2], left_coords_points[4])
            left_P1_P4 = self.__distance(left_coords_points[0], left_coords_points[3])
            right_coords_points = self.__denormalize(landmarks, config.face_right_eye, img_height, img_width)
            right_P2_P6 = self.__distance(right_coords_points[1], right_coords_points[5])
            right_P3_P5 = self.__distance(right_coords_points[2], right_coords_points[4])
            right_P1_P4 = self.__distance(right_coords_points[0], right_coords_points[3])
            # EAR公式，计算眼睛纵横比
            left_ear = (left_P2_P6 + left_P3_P5) / (2.0 * left_P1_P4)
            right_ear = (right_P2_P6 + right_P3_P5) / (2.0 * right_P1_P4)
            ear = (left_ear + right_ear) / 2
        except:
            ear = 0.0
        return ear

    # 张嘴
    def __mar(self, all_landmarks, config, img_height, img_width):
        landmarks = all_landmarks['face']
        try:
            coords_points = self.__denormalize(landmarks, config.face_lip, img_height, img_width)
            # 得到各定位点间的距离
            P1_P2 = self.__distance(coords_points[0], coords_points[1])
            P3_P4 = self.__distance(coords_points[2], coords_points[3])
            P5_P6 = self.__distance(coords_points[4], coords_points[5])
            # MAR公式，计算嘴唇纵横比
            mar = (P1_P2 + P3_P4) / (2.0 * P5_P6)
        except:
            mar = 0.0
        return mar

    # 低头
    def __up_down_head_val(self, all_landmarks, config, img_height, img_width):
        landmarks = all_landmarks['pose']
        try:
            coords_points = self.__denormalize(landmarks, config.pose_cheek + config.pose_eye, img_height, img_width)
            cheek_mid_y = (coords_points[0][1] + coords_points[1][1]) / 2
            eye_mid_y = (coords_points[2][1] + coords_points[3][1]) / 2
            # 为负说明脸颊到眼睛上面，即低头了
            up_down_head_val = cheek_mid_y - eye_mid_y
        except:
            up_down_head_val = 0.0
        return up_down_head_val

    # 歪头
    def __wryneck_val(self, all_landmarks, config, img_height, img_width):
        landmarks = all_landmarks['pose']
        try:
            coords_points = self.__denormalize(landmarks, config.pose_cheek, img_height, img_width)
            left_cheek = coords_points[0]
            right_cheek = coords_points[1]
            # 为负说明左倾，为正说明右倾
            wryneck_val = left_cheek[1] - right_cheek[1]
        except:
            wryneck_val = 0.0
        return wryneck_val

    # 歪肩膀
    def __wryshoulder_val(self, all_landmarks, config, img_height, img_width):
        landmarks = all_landmarks['pose']
        try:
            coords_points = self.__denormalize(landmarks, config.pose_shoulder, img_height, img_width)
            left_cheek = coords_points[0]
            right_cheek = coords_points[1]
            # 为负说明左倾，为正说明右倾
            wryshoulder_val = left_cheek[1] - right_cheek[1]
        except:
            wryshoulder_val = 0.0
        return wryshoulder_val

    # 歪肩膀
    def __lateralize_head_val(self, all_landmarks, config, img_height, img_width):
        landmarks = all_landmarks['pose']
        try:
            coords_points = self.__denormalize(landmarks, config.pose_eye+config.pose_cheek, img_height, img_width)
            left_eye = coords_points[0]
            right_eye = coords_points[1]
            left_cheek = coords_points[2]
            right_cheek = coords_points[3]
            val_1 = self.__distance(left_eye,left_cheek)
            val_2 = self.__distance(right_eye,right_cheek)
            val = val_1
            if val_2 > val: val = val_2
        except:
            val = 0.0
        return val

    # 手势识别
    def __hand_val(self, all_landmarks, hand_side, img_height, img_width):
        landmarks = all_landmarks[hand_side]
        hand_local = []
        for i in range(21):
            x = landmarks[i].x * img_height
            y = landmarks[i].y * img_width
            hand_local.append((x, y))
        if hand_local:
            angle_list = self.__hand_angle(hand_local)
            gesture_str = self.__h_gesture(angle_list)
        else:
            gesture_str = None
        return gesture_str

    # 求解二维向量的角度
    def __vector_2d_angle(self,v1, v2):
        v1_x = v1[0]
        v1_y = v1[1]
        v2_x = v2[0]
        v2_y = v2[1]
        try:
            angle_ = math.degrees(math.acos(
                (v1_x * v2_x + v1_y * v2_y) / (((v1_x ** 2 + v1_y ** 2) ** 0.5) * ((v2_x ** 2 + v2_y ** 2) ** 0.5))))
        except:
            angle_ = 65535.
        if angle_ > 180.:
            angle_ = 65535.
        return angle_

    # 获取对应手相关向量的二维角度, 根据角度确定手势
    def __hand_angle(self,hand_):
        angle_list = []
        # ---------------------------- thumb 大拇指角度
        angle_ = self.__vector_2d_angle(
            ((int(hand_[0][0]) - int(hand_[2][0])), (int(hand_[0][1]) - int(hand_[2][1]))),
            ((int(hand_[3][0]) - int(hand_[4][0])), (int(hand_[3][1]) - int(hand_[4][1])))
        )
        angle_list.append(angle_)
        # ---------------------------- index 食指角度
        angle_ = self.__vector_2d_angle(
            ((int(hand_[0][0]) - int(hand_[6][0])), (int(hand_[0][1]) - int(hand_[6][1]))),
            ((int(hand_[7][0]) - int(hand_[8][0])), (int(hand_[7][1]) - int(hand_[8][1])))
        )
        angle_list.append(angle_)
        # ---------------------------- middle 中指角度
        angle_ = self.__vector_2d_angle(
            ((int(hand_[0][0]) - int(hand_[10][0])), (int(hand_[0][1]) - int(hand_[10][1]))),
            ((int(hand_[11][0]) - int(hand_[12][0])), (int(hand_[11][1]) - int(hand_[12][1])))
        )
        angle_list.append(angle_)
        # ---------------------------- ring 无名指角度
        angle_ = self.__vector_2d_angle(
            ((int(hand_[0][0]) - int(hand_[14][0])), (int(hand_[0][1]) - int(hand_[14][1]))),
            ((int(hand_[15][0]) - int(hand_[16][0])), (int(hand_[15][1]) - int(hand_[16][1])))
        )
        angle_list.append(angle_)
        # ---------------------------- pink 小拇指角度
        angle_ = self.__vector_2d_angle(
            ((int(hand_[0][0]) - int(hand_[18][0])), (int(hand_[0][1]) - int(hand_[18][1]))),
            ((int(hand_[19][0]) - int(hand_[20][0])), (int(hand_[19][1]) - int(hand_[20][1])))
        )
        angle_list.append(angle_)
        return angle_list

    '''
        # 二维约束的方法定义手势
        # fist five gun love one six three thumbup yeah
    '''
    def __h_gesture(self,angle_list):
        thr_angle = 65.
        thr_angle_thumb = 53.
        thr_angle_s = 49.
        gesture_str = None
        if 65535. not in angle_list:
            if (angle_list[0] > thr_angle_thumb) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
                    angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
                gesture_str = "fist"
            elif (angle_list[0] > 5) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (
                    angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
                gesture_str = "one"
            elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (
                    angle_list[2] < thr_angle_s) and (angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
                gesture_str = "two"
            elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (
                    angle_list[2] < thr_angle_s) and (angle_list[3] < thr_angle_s) and (angle_list[4] > thr_angle):
                gesture_str = "three"
            elif (angle_list[0] > thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
                    angle_list[3] < thr_angle_s) and (angle_list[4] < thr_angle_s):
                gesture_str = "four"
            elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
                    angle_list[3] < thr_angle_s) and (angle_list[4] < thr_angle_s):
                gesture_str = "five"
            elif (angle_list[0] < thr_angle_s) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
                    angle_list[3] > thr_angle) and (angle_list[4] < thr_angle_s):
                gesture_str = "six"
            elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (
                    angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
                gesture_str = "gun"
            elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (
                    angle_list[3] > thr_angle) and (angle_list[4] < thr_angle_s):
                gesture_str = "love"
            elif (angle_list[0] < thr_angle_s) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
                    angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
                gesture_str = "thumbUp"
            else:
                gesture_str = "None"
        return gesture_str

    '''
    欧式距离
    '''
    def __distance(self, p_1, p_2) -> float:
        dist = sum([(i - j) ** 2 for i, j in zip(p_1, p_2)]) ** 0.5
        return dist


    def __denormalize(self, landmarks, refer_idxs, img_height, img_width):
        coords_points = []
        for i in refer_idxs:
            lm = landmarks[i]
            # 获得新的坐标
            coord = self.denormalize_coordinates(lm.x, lm.y, img_width, img_height)
            coords_points.append(coord)
        return coords_points

    def observe(self, config, param, data):
        if self.cap.isOpened():
            # 读取一帧与识别
            success, img = self.cap.read()

            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgRGB.flags.writeable = False
            results = self.holistic.process(imgRGB)
            all_landmarks = {"face": None, "pose": None, "left_hand": None, "right_hand": None}
            # 这个用来给gui画图
            _all_landmarks = {"face": None, "pose": None, "left_hand": None, "right_hand": None}
            if results.face_landmarks:
                _all_landmarks["face"]= results.face_landmarks
                all_landmarks["face"] = _all_landmarks["face"].landmark
            if results.pose_landmarks:
                _all_landmarks["pose"] = results.pose_landmarks
                all_landmarks["pose"] = _all_landmarks["pose"].landmark
            if results.left_hand_landmarks:
                _all_landmarks["left_hand"] = results.left_hand_landmarks
                all_landmarks["left_hand"] = _all_landmarks["left_hand"].landmark
            if results.right_hand_landmarks:
                _all_landmarks["right_hand"] = results.right_hand_landmarks
                all_landmarks["right_hand"] = _all_landmarks["right_hand"].landmark
            ih, iw, ic = img.shape
            # EAR
            if all_landmarks["face"] is not None:
                data.ear = self.__ear(all_landmarks, config, ih, iw)
                data.mar = self.__mar(all_landmarks, config, ih, iw)
            if all_landmarks["pose"] is not None:
                data.up_down_head_val = self.__up_down_head_val(all_landmarks, config, ih, iw)
                data.wryneck_val = self.__wryneck_val(all_landmarks, config, ih, iw)
                data.wryshoulder_val = self.__wryshoulder_val(all_landmarks, config, ih, iw)
                data.lateralize_head_val = self.__lateralize_head_val(all_landmarks, config, ih, iw)
            if all_landmarks["left_hand"] is not None:
                data.left_hand_val = self.__hand_val(all_landmarks, 'left_hand', ih, iw)
            if all_landmarks["right_hand"] is not None:
                data.right_hand_val = self.__hand_val(all_landmarks, 'right_hand', ih, iw)
            # 姿态检测
            return img, all_landmarks,_all_landmarks, data