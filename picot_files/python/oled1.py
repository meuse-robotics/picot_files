from machine import Pin, I2C
import ssd1306

# using default address 0x3C
i2c = I2C(0, sda=Pin(16), scl=Pin(17))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

def draw_circle(x,y,rad): #円を描く
    cx = rad
    cy = 0
    d = -2 * rad + 3
    while cx >= cy:
        display.pixel(x+cx, y+cy, 1)
        display.pixel(x-cx, y+cy, 1)
        display.pixel(x+cx, y-cy, 1)
        display.pixel(x-cx, y-cy, 1)
        display.pixel(x+cy, y+cx, 1)
        display.pixel(x-cy, y+cx, 1)
        display.pixel(x+cy, y-cx, 1)
        display.pixel(x-cy, y-cx, 1)
        if d >= 0:
            cx = cx-1
            d = d - 4 * cx
        cy = cy + 1
        d = d + 4 * cy + 2

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))
    
def fill_circle(x,y,rad): #円を塗りつぶす
    cx = rad
    cy = 0
    d = -2 * rad + 3
    while cx >= cy:
        display.line(constrain(x+cy,0,127), y+cx, constrain(x-cy,0,127), y+cx,1)
        display.line(constrain(x+cx,0,127), y+cy, constrain(x-cx,0,127), y+cy,1)
        display.line(constrain(x-cy,0,127), y-cx, constrain(x+cy,0,127), y-cx,1)
        display.line(constrain(x-cx,0,127), y-cy, constrain(x+cx,0,127), y-cy,1)
        if d >= 0:
            cx = cx - 1
            d = d - 4*cx
        cy = cy+1
        d = d + (4*cy+2)

draw_circle(32, 22, 20)
fill_circle(32, 22, 12)
draw_circle(96, 22, 20)
fill_circle(96, 22, 12)
display.line(32, 60, 96, 60, 1)
display.show()

