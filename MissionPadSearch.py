from time import sleep
from djitellopy import Tello
symbols = {
    '1' : '0000r0000000r0000000r0000000r0000000r0000000r0000000r0000000r000',
    '2' : '00bbbb0000000b0000000b0000bbbb0000b0000000b0000000b0000000bbbb00',
    '3' : '00pppp0000000p0000000p0000pppp0000000p0000000p0000000p0000pppp00',
    '4' : '00r00r0000r00r0000r00r0000rrrr0000000r0000000r0000000r0000000r00',
    '5' : '00bbbb0000b0000000b0000000bbbb0000000b0000000b0000000b0000bbbb00',
    '6' : 'ppppppppp0000000p0000000ppppppppp000000pp000000pp000000ppppppppp',
    '7' : 'rrrrrrrr000000r000000r000000r000000r000000r000000r000000r0000000',
    '8' : 'bbbbbbbbb000000bb000000bbbbbbbbbb000000bb000000bb000000bbbbbbbbb'
}
def show_symbol(symbol):
    if symbol in symbols:
        return 'EXT mled g '+symbols[symbol]
    else:
        return -1
def handle_mid(drone, mid):
    print(mid)
    if mid > 0:
        comm = show_symbol(str(mid))
        if comm != -1:
            drone.send_command_without_return(comm)
        drone.go_xyz_speed_mid(0, 0, 30, 20, mid)
        return True
    return False
# Настройки
# Подключение к дрону
drone = Tello()
# Переход в режим программирования
drone.connect()
# Включение обнаружение mission pad
drone.enable_mission_pads()
# Обнаружение mission pad с помощью нижней камеры
drone.set_mission_pad_detection_direction(0)
drone.takeoff()
drone.move_down(abs(drone.get_height()-30))
# Длина стороны квадратной области
square_side = 100
# Шаг облёта области
step = 25
print("Battery = "+str(drone.get_battery()))
flag = False
for i in range(round(square_side/step)):
    if flag:
        break
    for j in range(round(square_side/step)):
        mid = drone.get_mission_pad_id()
        flag = handle_mid(drone, mid)
        if i % 2 == 0:
            drone.move_forward(step)
        else:
            drone.move_back(step)
    drone.move_right(step)
    
drone.land()

