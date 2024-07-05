from machine import Pin
import time

# 設定
remote_in = Pin(6, Pin.IN, Pin.PULL_UP)

# 変数
rm_received = False  #信号受信完了した
digit = 0            #受信データの桁
rm_state = 0         #信号受信状況
rm_code = 0          #コード全体(32bit)
prev_micros = 0      #時間計測用

# 割り込み関数
def int_handler(pin):
    global rm_state
    global prev_micros
    global digit
    global rm_code
    global rm_received
    global test

    if rm_state != 0:
        #時間間隔を計算
        width = time.ticks_us() - prev_micros    
        if width > 10000:
            rm_state = 0    #長すぎ
        prev_micros = time.ticks_us()

    if rm_state == 0:    #信号未達
        prev_micros = time.ticks_us()    #現在時刻(microseconds)を記憶
        rm_state = 1    #最初のHIGH->LOW信号を検出した
        rm_code = 0
        digit = 0
    elif rm_state == 1:    #最初のLOW状態
        if width > 9500 or width < 8500:    #リーダーコード(9ms)ではない
            rm_state = 0
        else:
            rm_state = 2    #LOW->HIGHで9ms検出
    elif rm_state == 2:    #9ms検出した
        if width > 5000 or width < 4000:    #リーダーコード(4.5ms)ではない
            rm_state = 0
        else:
            rm_state = 3    #HIGH->LOWで4.5ms検出
    elif rm_state == 3:    #4.5ms検出した
        if width > 700 or width < 400:
            rm_state = 0    #データ棄却
        else:
            rm_state = 4    #LOW->HIGHで0.56ms検出した
    elif rm_state == 4:    #0.56ms検出した
        if width > 1800 or width < 400:   #長すぎ 短すぎ
            rm_state = 0    #データ棄却
        else:
            # 新しいデータを上位のビットに格納
            if width > 1000:    #HIGH期間長い -> 1
                rm_code |= (1 << digit)
            else:             #HIGH期間短い -> 0
                rm_code &= ~(1 << digit)
            digit += 1  #次のbit

            if digit > 31:   #完了
                rm_received = True
                return
            rm_state = 3    #次のLOW->HIGHを待つ

remote_in.irq(trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING, handler = int_handler)

"""while True:
    if rm_received == True:    #リモコン受信した
        rm_received = False    #初期化
        rm_state = 0      #初期化
        #図とは左右が逆であることに注意
        #下16bitがcustomCode
        custom_code = rm_code & 0xffff   
        #下16bitを捨てたあとの下8bitがdataCode
        data_code = (rm_code & 0xff0000) >> 16   
        #下24bitを捨てたあとの下8bitがinvDataCode
        inv_data_code = (rm_code & 0xff000000) >> 24    
        #反転確認
        if (data_code + inv_data_code) == 0xff:    
            print('data_code=' + str(data_code))"""
