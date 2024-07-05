from machine import Pin, PWM
import time

SV_FREQ = 50.0  # サーボ信号周波数
MAX_DUTY = 65025.0 # 周期内の分割数
MIN_SV_PULSE = 0.6  # 最小パルス幅　msec at 0°
MAX_SV_PULSE = 2.4  # 最大パルス幅  msec at 180°

# パルス幅を計算する関数
def get_pulse_width(angle):
    pulse_ms= MIN_SV_PULSE + (MAX_SV_PULSE - MIN_SV_PULSE) * angle /180.0
    x = (int)(MAX_DUTY * (pulse_ms * SV_FREQ /1000.0))
    return x

servo0 = PWM(Pin(0)) # 0ピンにPWMを出す機能 servo0という名前
servo0.freq(50) # PWMの周波数は50Hz
servo0.duty_u16(get_pulse_width(60)) # 90度のPWMを出力

while True:# 繰り返し
    servo0.duty_u16(get_pulse_width(60))# 60度のPWMを出力
    print('angle=60')
    time.sleep(1)# 1秒待ち
    servo0.duty_u16(get_pulse_width(120))# 120度のPWMを出力
    print('angle=120')
    time.sleep(1)# 1秒待ち

