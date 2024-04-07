import pygame
from external.airpi import main as airpi


def init_pygame():
    pygame.init()


def wait_for_controller():
    while True:
        pygame.event.get()
        pygame.joystick.init()
        for i in range(pygame.joystick.get_count()):
            if "Xbox" in pygame.joystick.Joystick(i).get_name():
                controller = pygame.joystick.Joystick(i)
                controller.init()
                print("Xbox Controller Connected")
                return controller
        pygame.time.delay(500)


def main():
    init_pygame()
    controller = None

    vid, det, ser = airpi.setup()

    speedAxisThreshold = 0
    directionStickThreshold = 0.001
    speedAxis = [0]
    directionStick = [[0,0]]
    button = [0]

    drive = [[0, 0], [0, 0]]
    speed = 0

    while True:
        if not controller or not pygame.joystick.get_init() or not pygame.joystick.get_count():
            drive[1] = [0, 0]
            controller = wait_for_controller()

        pygame.event.pump()
        speedAxis.append(abs(controller.get_axis(pygame.CONTROLLER_AXIS_TRIGGERRIGHT)+1)/2)
        directionStick.append(controller.get_axis(pygame.CONTROLLER_AXIS_LEFTX))
        button.append(controller.get_button(pygame.CONTROLLER_BUTTON_B))

        if abs(speedAxis[1]) < speedAxisThreshold:
            speedAxis[1] = 0

        if abs(directionStick[1]) < directionStickThreshold:
            directionStick[1] = 0

        if speedAxis[0] != speedAxis[1]:
            speed = int(speedAxis[1] * 100)
            drive[1] = [speed] * 2

        if directionStick[0] != directionStick[1]:
            drive[1] = [speed] * 2
            if directionStick[1] < 0:
                drive[1][0] = int(drive[1][0] * (1 - abs(directionStick[1])))
            elif directionStick[1] > 0:
                drive[1][1] = int(drive[1][1] * (1 - abs(directionStick[1])))

        if button[0] != button[1] and button[1] == 1:
            print(button)
            airpi.inference(vid, det, ser)

        if drive[0][1] != drive[1][1] or drive[0][0] != drive[1][0]:
            outStr = f'D{drive[1][0]};{drive[1][1]}'
            print(outStr)
            ser.write(outStr)
            drive.pop(0)
            drive.append(drive[0])

        speedAxis.pop(0)
        directionStick.pop(0)
        button.pop(0)


if __name__ == "__main__":
    main()
