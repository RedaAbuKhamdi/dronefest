from djitellopy import tello    
import keyboard
import time
import cv2
symbols = {
    '1' : '0000r0000000r0000000r0000000r0000000r0000000r0000000r0000000r000',
    '2' : '00bbbb0000000b0000000b0000bbbb0000b0000000b0000000b0000000bbbb00',
    '3' : '00pppp0000000p0000000p0000pppp0000000p0000000p0000000p0000pppp00',
    '4' : '00r00r0000r00r0000r00r0000rrrr0000000r0000000r0000000r0000000r00',
    '5' : '00bbbb0000b0000000b0000000bbbb0000000b0000000b0000000b0000bbbb00',
    '6' : 'ppppppppp0000000p0000000ppppppppp000000pp000000pp000000ppppppppp',
    '7' : 'rrrrrrrr000000r000000r000000r000000r000000r000000r000000r0000000',
    '8' : 'bbbbbbbbb000000bb000000bbbbbbbbbb000000bb000000bb000000bbbbbbbbb',
    'smile' : '00bb00bb0000bb00bb0000000000000bb0000bb000bb00bb00000bbbb0000000000000'
}

def show_symbol(symbol, drone):
    if symbol in symbols:
        drone.send_command_without_return('EXT mled g '+symbols[symbol])
me = tello.Tello()
me.connect()
print(me.get_battery())
global img_original
me.streamon()

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50
    if keyboard.is_pressed("left"):
        lr = -speed

    elif keyboard.is_pressed("right"):
        lr = speed

    if keyboard.is_pressed("up"):
        fb = speed

    elif keyboard.is_pressed("down"):
        fb = -speed

    if keyboard.is_pressed("w"):
        ud = speed

    elif keyboard.is_pressed("s"):
        ud = -speed

    if keyboard.is_pressed("a"):
        yv = -speed

    elif keyboard.is_pressed("d"):
        yv = speed

    if keyboard.is_pressed("q"): me.land(); time.sleep(3)

    if keyboard.is_pressed("e"):  me.takeoff()
    if keyboard.is_pressed(']'): show_symbol('smile', me)
    if keyboard.is_pressed("z"):
        cv2.imwrite(f'{time.time()}.jpg', img_original)
        time.sleep(0.3)

    return [lr, fb, ud, yv]


while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img_original = me.get_frame_read().frame
    img = cv2.resize(img_original, (360, 240))
    cv2.imshow("Image", img)
    cv2.waitKey(1)