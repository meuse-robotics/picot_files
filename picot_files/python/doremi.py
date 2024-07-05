from machine import Pin, PWM
import time

MAX_DUTY = 65025.0 # 周期内の分割数
frq = [262, 294, 330, 349, 392, 440, 494, 523]
buz = PWM(Pin(14))
buz.duty_u16(int(MAX_DUTY/2))

for i in range(8):
    buz.freq(frq[i])
    time.sleep(0.5)
buz.duty_u16(0)
