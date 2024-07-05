from machine import Pin, PWM, Timer
import time
import remote
import motion
import oled

# ***** Face *****
def face(mode):
    if mode == 10:
        oled.display.fill(0)
        oled.draw_circle(32, 22, 20) #右目
        oled.fill_circle(32, 22, 12, 1)
        oled.draw_circle(96, 22, 20) #左目
        oled.fill_circle(96, 22, 12, 1)
        oled.display.line(32, 55, 64, 60, 1) #口
        oled.display.line(64, 60, 96, 55, 1)
        oled.display.show()
    elif mode == 11:
        oled.display.fill(0)
        oled.draw_circle(32, 22, 20) #右目
        oled.fill_circle(32, 22, 12, 1)
        oled.draw_circle(96, 22, 20) #左目
        oled.fill_circle(96, 22, 12, 1)
        oled.display.line(32, 60, 64, 55, 1) #口
        oled.display.line(64, 55, 96, 60, 1)
        oled.display.line(56, 0, 56, 15, 1)
        oled.display.line(70, 0, 70, 15, 1)
        oled.display.show()
face_mode = 10
face(10)

# ***** Action *****
action_type=['STOP','FWRD','BWRD','LTRN','RTRN','LEFT','RGHT','KICK']
SV_FREQ = 50.0  # サーボ信号周波数
MAX_DUTY = 65025.0 # 周期内の分割数
MIN_SV_PULSE = 0.6  # 最小パルス幅　0°
MAX_SV_PULSE = 2.4  # 最大パルス幅 180°

correction = [4,0, -4,-4,8,-14, 8,-10,4,-12, -12,0]
servo = []
temp_angle = [90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90]

div_counter = 0
key_frame = 0
next_key_frame = 1
rows = 0
action = []
action_mode = 'STOP'
servo_flag = False
tim = Timer()

# 30Hzのタイマー割り込み
def tick(timer):
    global servo_flag
    servo_flag = True

tim.init(freq=30, mode=Timer.PERIODIC, callback=tick)

# パルス幅を計算する関数
def get_pulse_width(angle):
    pulse_ms = MIN_SV_PULSE + (MAX_SV_PULSE - MIN_SV_PULSE) * angle / 180.0
    x = (int)(MAX_DUTY * (pulse_ms * SV_FREQ /1000.0))
    return x

# 12個のservoを追加
servo.append(PWM(Pin(0))) #Right Shoulder Roll
servo.append(PWM(Pin(1))) #Right Shoulder Pitch
servo.append(PWM(Pin(2))) #Right Hip Roll
servo.append(PWM(Pin(3))) #Right Hip Pitch
servo.append(PWM(Pin(8))) #Right Ankle Pitch
servo.append(PWM(Pin(9))) #Right Ankle Roll
servo.append(PWM(Pin(20))) #Left Ankle Roll
servo.append(PWM(Pin(21))) #Left Ankle Pitch
servo.append(PWM(Pin(22))) #Left Hip Pitch
servo.append(PWM(Pin(26))) #Left Hip Roll
servo.append(PWM(Pin(27))) #Left Shoulder Pitch
servo.append(PWM(Pin(28))) #Left Shoulder Roll
# 全てのサーボを順番に駆動
for i in range(12):
    servo[i].freq(50)
    servo[i].duty_u16(get_pulse_width(90 + correction[i]))

# ***** LED *****
led = Pin(25, Pin.OUT)
led.value(0)

# ***** Sound *****
buz = PWM(Pin(14))

def set_action(code):
    global action_mode
    global action
    global rows
    global div_counter
    global key_frame
    global next_key_frame
    if data_code == 248:
        led.value(1)
    elif data_code == 120:
        led.value(0)
    elif data_code == 32:
        action_mode = 'STOP'
    elif data_code == 160:
        action_mode = 'FWRD'
        action.clear()
        action = motion.fwrd.copy()
        rows = len(motion.fwrd)
    elif data_code == 0:
        action_mode = 'BWRD'
        action.clear()
        action = motion.bwrd.copy()
        rows = len(motion.bwrd)
    elif data_code == 177:
        action_mode = 'LTRN'
        action.clear()
        action = motion.ltrn.copy()
        rows = len(motion.ltrn)
    elif data_code == 33:
        action_mode = 'RTRN'
        action.clear()
        action = motion.rtrn.copy()
        rows = len(motion.rtrn)
    elif data_code == 16:
        action_mode = 'LEFT'
        action.clear()
        action = motion.left.copy()
        rows = len(motion.left)
    elif data_code == 128:
        action_mode = 'RGHT'
        action.clear()
        action = motion.rght.copy()
        rows = len(motion.rght)
    elif data_code == 129:
        action_mode = 'DANCE'
        action.clear()
        action = motion.dance.copy()
        rows = len(motion.dance)
    div_counter = 0
    key_frame = 0
    next_key_frame = 1

while True:
    # *** Remote ***
    if remote.rm_received == True:    #リモコン受信した
         remote.rm_received = False    #初期化
         remote.rm_state = 0      #初期化
         #図とは左右が逆であることに注意
         custom_code = remote.rm_code & 0xffff   #下16bitがcustomCode
         data_code = (remote.rm_code & 0xff0000) >> 16   #下16bitを捨てたあとの下8bitがdataCode
         inv_data_code = (remote.rm_code & 0xff000000) >> 24    #下24bitを捨てたあとの下8bitがinvDataCode
         if (data_code + inv_data_code) == 0xff:    #反転確認
             print("data_code="+str(data_code))
             set_action(data_code)
    # *** Servo ***
    if servo_flag == True:
        servo_flag = False
        if action_mode != 'STOP':
            # キーフレームを更新
            div_counter += 1
            if div_counter >= action[key_frame][12]:
                div_counter = 0
                key_frame = next_key_frame
                next_key_frame += 1
                if next_key_frame > rows-1:
                    next_key_frame = 0
                if action[next_key_frame][12] == 127:
                    action_mode = 'STOP'
                """if action[next_key_frame][13] == 0: #無音
                    buz.duty_u16(0)
                elif action[next_key_frame][13] == 1: #「ド」
                    buz.duty_u16(int(MAX_DUTY/2))
                    buz.freq(262)
                elif action[next_key_frame][13] == 2: #「ソ」
                    buz.duty_u16(int(MAX_DUTY/2))
                    buz.freq(392)"""
                if action[next_key_frame][13] != face_mode:
                    face_mode = action[next_key_frame][13]
                    face(face_mode)
            # 角度計算
            for i in range(12):
                temp_angle[i] = action[key_frame][i] +\
(action[next_key_frame][i] - action[key_frame][i])\
* div_counter / action[key_frame][12]
        else:
            buz.duty_u16(0)
            for i in range(12):
                temp_angle[i] = 90
        # サーボ駆動
        for i in range(12):
            servo[i].duty_u16(get_pulse_width(int(temp_angle[i]) + correction[i]))
