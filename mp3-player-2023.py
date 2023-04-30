import time
import os
import RPi.GPIO as IO

PLAYER = "/usr/bin/mpc"
LAST_EVENT = 0
BUTTON_BOUNCE_GAP = 0.1 #seconds

IO.setmode(IO.BOARD)
IO.setup(10, IO.IN, pull_up_down=IO.PUD_DOWN)

def mpc(command):
    os.system('mpc %s' % command)

def mpc_add_all_to_playlist():
    os.system('mpc ls | mpc add')

def set_up_playlist():
    mpc('clear')
    mpc_add_all_to_playlist()
    mpc('random off')
    mpc('repeat on')
    mpc('volume 79')

def play_next_mp3():
    mpc('play')
    mpc('next')
    
def button_bounce():
    print(time.time() - LAST_EVENT)
    return time.time() - LAST_EVENT < BUTTON_BOUNCE_GAP

def button_callback(channel):
    global LAST_EVENT
    if not(button_bounce()):
        print("Pressed! %s" % channel)
        LAST_EVENT = time.time()
        if channel == 10: play_next_mp3()
    else:
        print("Bounce")
        
set_up_playlist()

IO.add_event_detect(10, IO.RISING, callback=button_callback)

a = raw_input("Press enter to quit\n\n")
IO.cleanup()

