import time

# 判断是否满足疲劳或坐不正确
class Judger:

    # 闭眼
    def __judge_eye_close(self,  param, data):
        res = False
        if param.close_eye_last_time is None:
            param.close_eye_last_time = time.time()
        if data.ear > param.close_eye_threshold:
            param.close_eye_last_time = None
        else:
            if time.time() - param.close_eye_last_time >= param.close_eye_time_gap:
                res = True
        return res

    # 打哈欠
    def __judge_mouth_close(self,  param, data):
        res = False
        if param.open_mouth_last_time is None:
            param.open_mouth_last_time = time.time()
        if data.mar < param.open_mouth_threshold:
            param.open_mouth_last_time = None
        else:
            if time.time() - param.open_mouth_last_time >= param.open_mouth_time_gap:
                res = True
        return res

    # 上下点头
    def __judge_head_up_down(self,  param, data):
        res = False
        if param.up_down_head_last_time is None:
            param.up_down_head_last_time = time.time()
        if data.up_down_head_val < param.up_down_head_threshold_up and data.up_down_head_val > param.up_down_head_threshold_down:
            param.up_down_head_last_time = None
        else:
            if time.time() - param.up_down_head_last_time >= param.up_down_head_time_gap:
                res = True
        return res

    # 低头抬头
    def __judge_keep_head_up_down(self,  param, data):
        res = False
        if param.keep_up_down_head_last_time is None:
            param.keep_up_down_head_last_time = time.time()
        if data.up_down_head_val < param.up_down_head_threshold_up and data.up_down_head_val > param.up_down_head_threshold_down:
            param.keep_up_down_head_last_time = None
        else:
            if time.time() - param.keep_up_down_head_last_time >= param.keep_up_down_head_time_gap:
                res = True
        return res

    # 歪头
    def __judge_wryneck(self,  param, data):
        res = False
        if param.wryneck_last_time is None:
            param.wryneck_last_time = time.time()
        if data.wryneck_val < param.wryneck_threshold_up and data.wryneck_val > param.wryneck_threshold_down:
            param.wryneck_last_time = None
        else:
            if time.time() - param.wryneck_last_time >= param.wryneck_time_gap:
                res = True
        return res

    # 歪肩膀
    def __judge_wryshoulder(self,  param, data):
        res = False
        if param.wryshoulder_last_time is None:
            param.wryshoulder_last_time = time.time()
        if data.wryshoulder_val < param.wryshoulder_threshold_up and data.wryshoulder_val > param.wryshoulder_threshold_down:
            param.wryshoulder_last_time = None
        else:
            if time.time() - param.wryshoulder_last_time >= param.wryshoulder_time_gap:
                res = True
        return res

    # 侧头
    def __judge_lateralize_head(self, param, data):
        res = False
        if param.lateralize_head_last_time is None:
            param.lateralize_head_last_time = time.time()
        if data.lateralize_head_val < param.lateralize_head_threshold:
            param.lateralize_head_last_time = None
        else:
            if time.time() - param.lateralize_head_last_time >= param.lateralize_head_time_gap:
                res = True
        return res

    # 张开手休眠
    def __judge_open_palm_2sleep(self, param, data):
        res = False
        if param.open_palm_2sleep_last_time is None:
            param.open_palm_2sleep_last_time = time.time()
        if data.left_hand_val!='five' and data.right_hand_val!='five':
            param.open_palm_2sleep_last_time = None
        else:
            if time.time() - param.open_palm_2sleep_last_time >= param.open_palm_2sleep_time_gap:
                print("启动休眠")
                res=True
        return res
    # 总判断
    def judge(self,param,data):
        data.eye_closed = self.__judge_eye_close(param,data)
        data.mouth_opened = self.__judge_mouth_close(param, data)
        data.up_down_head = self.__judge_head_up_down(param, data)
        data.keep_up_down_head = self.__judge_keep_head_up_down(param, data)
        data.wryshoulder = self.__judge_wryshoulder(param, data)
        data.wryneck = self.__judge_wryneck(param, data)
        data.lateralize_head = self.__judge_lateralize_head(param, data)
        data.open_palm_2sleep = self.__judge_open_palm_2sleep(param,data)
        return data

