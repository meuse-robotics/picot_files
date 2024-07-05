fwrd = [
    [75, 95,  90,110,110, 90,  90,110,110, 90,  95, 95, 8, 0],
    [80, 90,  90,110,110, 80,  80,100,100, 90,  90,100, 8, 0],
    [85, 85,  90, 90, 90, 90,  80, 90, 90, 90,  85,105, 4, 1],
    [90, 80,  90, 70, 70, 90,  80, 80, 80, 90,  80,110, 4, 1],
    [85, 85,  90, 70, 70, 90,  90, 70, 70, 90,  85,105, 8, 0],
    [80, 90,  90, 80, 80,100, 100, 70, 70, 90,  90,100, 8, 0],
    [75, 95,  90, 90, 90,100,  90, 90, 90, 90,  95, 95, 4, 2],
    [70,100,  90,100,100,100,  90,110,110, 90, 100, 90, 4, 2]
]
bwrd = [
    [75, 95,  90,110,110, 90,  90,110,110, 90,  95, 95, 8, 0],
    [70,100,  90,100,100,100,  90,110,110, 90, 100, 90, 4, 1],
    [75, 95,  90, 90, 90,100,  90, 90, 90, 90,  95, 95, 4, 1],
    [80, 90,  90, 80, 80,100, 100, 70, 70, 90,  90,100, 8, 0],
    [85, 85,  90, 70, 70, 90,  90, 70, 70, 90,  85,105, 8, 0],
    [90, 80,  90, 70, 70, 90,  80, 80, 80, 90,  80,110, 4, 2],
    [85, 85,  90, 90, 90, 90,  80, 90, 90, 90,  85,105, 4, 2],
    [80, 90,  90,110,110, 80,  80,100,100, 90,  90,100, 8, 0]
]
ltrn = [
    [75, 95,  90,110,110, 90,  90,110,110, 90,  95, 95, 8, 0],
    [80, 90,  90,110,110, 80,  80,100,100, 90,  90,100, 8, 0],
    [85, 85,  90, 90, 90, 90,  80, 90, 90, 90,  85,105, 4, 1],
    [90, 80,  90, 70, 70, 90,  80, 80, 80, 90,  80,110, 4, 1],
    [85, 85,  90, 70, 70, 90,  90, 70, 70, 90,  85,105, 8, 0],
    [80, 90,  90, 80, 80, 90,  90, 70, 70, 90,  90,100, 8, 0],
    [75, 95,  90, 90, 90, 90,  90, 90, 90, 90,  95, 95, 4, 2],
    [70,100,  90,100,100, 90,  90,110,110, 90, 100, 90, 4, 2]
]
rtrn = [
    [75, 95,  90,110,110, 90,  90,110,110, 90,  95, 95, 8, 0],
    [80, 90,  90,110,110, 90,  90,100,100, 90,  90,100, 8, 0], 
    [85, 85,  90, 90, 90, 90,  90, 90, 90, 90,  85,105, 4, 1],
    [90, 80,  90, 70, 70, 90,  90, 80, 80, 90,  80,110, 4, 1],
    [85, 85,  90, 70, 70, 90,  90, 70, 70, 90,  85,105, 8, 0],
    [80, 90,  90, 80, 80,100, 100, 70, 70, 90,  90,100, 8, 0],
    [75, 95,  90, 90, 90,100,  90, 90, 90, 90,  95, 95, 4, 2],
    [70,100,  90,100,100,100,  90,110,110, 90, 100, 90, 4, 2]
]
left = [
    [90, 90,  90, 90, 90, 90,  90, 90, 90, 90,  90, 90, 6, 0],
    [90, 90,  90, 90, 90,100, 100, 90, 90, 90,  90, 90, 6, 0], 
    [90, 90,  80, 90, 90,100, 100, 90, 90,100,  90, 90, 6, 1],
    [90, 90,  80, 90, 90, 80,  80, 90, 90, 90,  90, 90, 6, 0], 
    [90, 90,  90, 90, 90, 80,  80, 90, 90, 90,  90, 90, 6, 0],
    [90, 90,  90, 90, 90, 90,  90, 90, 90, 90,  90, 90, 6, 2]
]
rght = [
    [90, 90,  90, 90, 90, 90,  90, 90, 90, 90,  90, 90, 6, 0],
    [90, 90,  90, 90, 90, 80,  80, 90, 90, 90,  90, 90, 6, 0], 
    [90, 90,  80, 90, 90, 80,  80, 90, 90,100,  90, 90, 6, 1],
    [90, 90,  90, 90, 90,100, 100, 90, 90,100,  90, 90, 6, 0], 
    [90, 90,  90, 90, 90,100, 100, 90, 90, 90,  90, 90, 6, 0],
    [90, 90,  90, 90, 90, 90,  90, 90, 90, 90,  90, 90, 6, 2]
]
kick = [
    [90, 90,  90, 90, 90, 90,  90, 90, 90, 90,  90, 90, 12, 0],
    [90, 90,  90, 90, 90, 70,  75, 90, 90, 90,  90, 90, 12, 0],
    [90, 70,  90,120,110, 90,  75, 90, 90,100,  70, 90,  8, 0],
    [90, 70,  90,120,110, 90,  75, 90, 90,100,  70, 90,  8, 0],
    [90,110,  90, 30, 40, 90,  75, 90, 90,100, 110, 90, 12, 0],
    [90,110,  90, 30, 40, 90,  75, 90, 90,100, 110, 90, 12, 0],
    [90, 90,  90, 90, 90, 90,  90, 90, 90, 90,  90, 90,  8, 0],
    [90, 90,  90, 90, 90, 90,  90, 90, 90, 90,  90, 90,127, 0]
]
