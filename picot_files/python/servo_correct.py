from machine import Pin, PWM

SV_FREQ = 50.0  # サーボ信号周波数
MAX_DUTY = 65025.0 # 周期内の分割数
MIN_SV_PULSE = 0.6  # 最小パルス幅　0°
MAX_SV_PULSE = 2.4  # 最大パルス幅 180°

correction = [0,0, 0,0,0,0, 0,0,0,0, 0,0]
servo = []

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
