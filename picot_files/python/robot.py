from machine import Pin, PWM, Timer
import time
import motion
import oled

# ***** Face *****
oled.draw_circle(32, 22, 20)
oled.fill_circle(32, 22, 12, 1)
oled.draw_circle(96, 22, 20)
oled.fill_circle(96, 22, 12, 1)
oled.display.text('STOP', 46, 56, 1)
oled.display.show()

# ***** Action *****
action=['STOP','FWRD','BWRD','LTRN','RTRN','LEFT','RGHT','KICK']

SV_FREQ = 50.0  # サーボ信号周波数
MAX_DUTY = 65025.0 # 周期内の分割数
MIN_SV_PULSE = 0.6  # 最小パルス幅　0°
MAX_SV_PULSE = 2.4  # 最大パルス幅 180°

correction = [4,0, 0,0,8,-8, 8,-8,0,-8, -12,0]
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
def tick(tim):
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

# ***** Sound *****
buz = PWM(Pin(14))

def set_action(mode):
    global action_mode
    global action
    global rows
    global div_counter
    global key_frame
    global next_key_frame
    global oled
    
    if mode == 'STOP':
        action_mode = mode
    elif mode == 'FWRD':
        action_mode = mode
        action.clear()
        action = motion.fwrd.copy()
        rows = len(motion.fwrd)
    elif mode == 'BWRD':
        action_mode = mode
        action.clear()
        action = motion.bwrd.copy()
        rows = len(motion.bwrd)
    elif mode == 'LTRN':
        action_mode = mode
        action.clear()
        action = motion.ltrn.copy()
        rows = len(motion.ltrn)
    elif mode == 'RTRN':
        action_mode = mode
        action.clear()
        action = motion.rtrn.copy()
        rows = len(motion.rtrn)
    elif mode == 'LEFT':
        action_mode = mode
        action.clear()
        action = motion.left.copy()
        rows = len(motion.left)
    elif mode == 'RGHT':
        action_mode = mode
        action.clear()
        action = motion.rght.copy()
        rows = len(motion.rght)
    elif data_code == 129:
        action_mode = 'KICK'
        action.clear()
        action = motion.kick.copy()
        rows = len(motion.kick)
    
    div_counter = 0
    key_frame = 0
    next_key_frame = 1
    next_key_frame = 1
    oled.display.fill_rect(46, 56, 78, 64, 0)
    oled.display.text(action_mode, 46, 56, 1)
    oled.display.show()


blink = 0
def drive():
    global action_mode
    global div_counter
    global key_frame
    global next_key_frame
    # *** Servo ***
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
            if action[next_key_frame][13] == 0: #無音
                buz.duty_u16(0)
            elif action[next_key_frame][13] == 1: #「ド」
                buz.duty_u16(int(MAX_DUTY/2))
                buz.freq(262)
            elif action[next_key_frame][13] == 2: #「ソ」
                buz.duty_u16(int(MAX_DUTY/2))
                buz.freq(392)

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
        
