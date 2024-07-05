from machine import Pin, I2C
import ssd1306


# using default address 0x3C
i2c = I2C(0, sda=Pin(16), scl=Pin(17),freq=400000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)

def draw_circle(x,y,rad):
    cx=rad
    cy=0
    d=-2*rad+3
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
            cx=cx-1
            d = d - 4 * cx
        cy=cy+1
        d = d + 4 * cy + 2
        
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))
    
def fill_circle(x,y,rad,w):
    cx=rad
    cy=0
    d=-2*rad+3
    while cx >= cy:
        display.line(constrain(cy + x,0,127), cx + y, constrain(-cy + x,0,127), cx + y,w)
        display.line(constrain(cx + x,0,127), cy + y, constrain(-cx + x,0,127), cy + y,w)
        display.line(constrain(-cy + x,0,127), -cx + y, constrain(cy + x,0,127), -cx + y,w)
        display.line(constrain(-cx + x,0,127), -cy + y, constrain(cx + x,0,127), -cy + y,w)
        if d >= 0:
            cx = cx - 1
            d = d - 4*cx
        cy = cy+1
        d = d + (4*cy+2)

