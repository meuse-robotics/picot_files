from machine import Pin
import remote

# ***** LED *****
led = Pin(25, Pin.OUT)
led.value(0)

while True:
    if remote.rm_received == True:    #リモコン受信した
        remote.rm_received = False    #初期化
        remote.rm_state = 0      #初期化
        #図とは左右が逆であることに注意
        #下16bitがcustomCode
        custom_code = remote.rm_code & 0xffff   
        #下16bitを捨てたあとの下8bitがdataCode
        data_code = (remote.rm_code & 0xff0000) >> 16   
        #下24bitを捨てたあとの下8bitがinvDataCode
        inv_data_code = (remote.rm_code & 0xff000000) >> 24    
        #反転確認
        if (data_code + inv_data_code) == 0xff:    
            print('data_code=' + str(data_code))
            if data_code == 248:
                led.value(1)
            elif data_code == 120:
                led.value(0)

