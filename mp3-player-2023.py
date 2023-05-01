import time
import subprocess
import RPi.GPIO as IO

PLAYER = "/usr/bin/mpc"
LAST_EVENT = 0
BUTTON_BOUNCE_GAP = 0.5 #seconds

def mpc(command):
    return subprocess.check_output('mpc %s' % command, shell=True)

def mpc_add_all_to_playlist():
    subprocess.check_output('mpc ls | mpc add', shell=True)

def set_up_playlist():
    mpc('clear')
    mpc_add_all_to_playlist()
    mpc('random on')
    mpc('repeat on')
    mpc('volume 70')

def button_bounce():
    print(time.time() - LAST_EVENT)
    return time.time() - LAST_EVENT < BUTTON_BOUNCE_GAP

def next_track():
    mpc('play')
    print(mpc('next'))

def prev_track():
    print(mpc('prev'))
    
def button_callback(channel):
    global LAST_EVENT
    if not(button_bounce()):
        print("Pressed! %s" % channel)
        LAST_EVENT = time.time()
        if channel in BUTTON_FN:
            BUTTON_FN[channel]()
    else:
        print("Bounce detected")
        
set_up_playlist()

BUTTON_FN = {
    10: next_track,
    8: prev_track,
}

IO.setmode(IO.BOARD)
for b in BUTTON_FN.keys():
    IO.setup(b, IO.IN, pull_up_down=IO.PUD_DOWN)
    IO.add_event_detect(b, IO.RISING, callback=button_callback)

a = raw_input("Press enter to quit\n\n")
IO.cleanup()

