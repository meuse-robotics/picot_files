from machine import Pin, PWM
import time

SV_FREQ = 50.0  # サーボ信号周波数
MAX_DUTY = 65025.0 # 周期内の分割数
MIN_SV_PULSE = 0.6  # 最小パルス幅　0°
MAX_SV_PULSE = 2.4  # 最大パルス幅 180°

correction = [0,0, 0,0,0,0, 0,0,0,0, 0,0]
servo = []
temp_angle = [90, 90,  90, 90, 90, 90,  90, 90, 90, 90,  90, 90]
angle = [
    [90, 90,  90, 90, 90, 90,  90, 90, 90, 90,  90, 90],#イニシャル 
    [90, 90,  90, 90, 90, 80,  80, 90, 90, 90,  90, 90],#左体重
    [90, 90,  90, 90, 90, 80,  80, 90, 90, 90,  90, 90],#ステップ
    [90, 90,  90, 90, 90, 90,  90, 90, 90, 90,  90, 90],#イニシャル
    [90, 90,  90, 90, 90,100, 100, 90, 90, 90,  90, 90],#右体重
    [90, 90,  90, 90, 90,100, 100, 90, 90, 90,  90, 90]#ステップ
]

divide = 10 # フレーム間の分割数
div_counter = 0 # 分割を数える
key_frame = 0 # 現在のキーフレーム
next_key_frame = 1 # 次回のフレーム

# パルス幅を計算する関数
def get_pulse_width(angle):
    pulse_ms = MIN_SV_PULSE + (MAX_SV_PULSE - MIN_SV_PULSE) * angle / 180.0
    x = (int)(MAX_DUTY * (pulse_ms * SV_FREQ / 1000.0))
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

while True: # 繰り返し
    # キーフレームを更新
    div_counter += 1
    if div_counter >= divide:
        div_counter = 0
        key_frame = next_key_frame
        next_key_frame += 1
        if next_key_frame > 5:
            next_key_frame = 0 #angle 0行に戻る
    # 角度計算
    for i in range(12):
        temp_angle[i] = angle[key_frame][i] +\
(angle[next_key_frame][i] - angle[key_frame][i])\
* div_counter / divide
    # サーボ駆動
    for i in range(12):
        servo[i].duty_u16(get_pulse_width(int(temp_angle[i]) + correction[i]))
    time.sleep(0.03) # 0.03秒待ち
