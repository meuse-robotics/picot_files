from machine import Pin, PWM
import time

MAX_DUTY = 65025.0

buz = PWM(Pin(14))
buz.freq(400)
buz.duty_u16(int(MAX_DUTY/2))
time.sleep(1)
buz.duty_u16(0)
