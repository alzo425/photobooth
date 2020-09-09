
### import libraries
import argparse
import time
import random
import board
import adafruit_ws2801

### Example for a Feather M4 driving 25 12mm leds
odata = board.MOSI_1 #MOSI
oclock = board.SCLK_1 #SCLK
numleds = 41 #Number LEDs
bright = 1.0
leds = adafruit_ws2801.WS2801(oclock, odata, numleds, brightness=bright, auto_write=False)
n_leds = len(leds)

######################### HELPERS ################################

# a random color 0 -> 224
def random_color():
    rand = [random.randrange(0, 7) * 36, random.randrange(0, 7) * 36, random.randrange(0, 7) * 36]
    return rand

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return 0, 0, 0
    if pos < 85:
        return int(255 - pos * 3), int(pos * 3), 0
    if pos < 170:
        pos -= 85
        return 0, int(255 - pos * 3), int(pos * 3)
    pos -= 170
    return int(pos * 3), 0, int(255 - (pos * 3))

######################### Modes ##################################
def random_mode(frequency,repeats):
    for idy in range(repeats):
        # fill each led with a random color
        for idx in range(n_leds):
            leds[idx] = random_color()

        # show all leds in led string
        leds.show()
        time.sleep(frequency)

def loading_mode1(color,frequency, repeats): #only vertical lines were moving up and down
    # initialize, all LEDs off
    leds.fill(0)
    leds.show()
    time.sleep(0.05)
    move=range(8)
    
    for idy in range(repeats):
        for idx in move: #move up
            ledright=12+idx
            leds[ledright] = color
            leds[ledright+1] = color
            leds[ledright-1] = 0
            leds[ledright-2] = 0
            
            ledleft=40-idx
            leds[ledleft] = color
            leds[ledleft-1] = color
            if idx>0:
                leds[ledleft+1] = 0
            if idx>1:
                leds[ledleft+2] = 0
            
            leds.show()
            time.sleep(frequency)
            
        for idx in move: #move down
            ledright=20-idx
            leds[ledright] = color
            leds[ledright-1] = color
            leds[ledright+1] = 0
            leds[ledright+2] = 0

            ledleft=32+idx
            leds[ledleft] = color
            leds[ledleft+1] = color
            leds[ledleft-1] = 0
            leds[ledleft-2] = 0
            
            leds.show()
            time.sleep(frequency)

def loading_mode2(color,frequency,repeats): # loading circle
    leds.fill(0)
    leds.show()
    time.sleep(0.05)
    for idy in range(repeats):
        for idx in range(n_leds):
            leds[idx] = color
            leds.show()
            time.sleep(frequency)
        for idx in range(n_leds):
            leds[idx] = 0
            leds.show()
            time.sleep(frequency)

def flash_mode(frequency, flashes,color):
    for i in range(flashes):
        leds.fill(color)
        leds.show()
        time.sleep(frequency)
        leds.fill(0)
        leds.show()
        time.sleep(frequency)
    leds.fill(color)
    leds.show()
    time.sleep(1000)

def rainbow_mode(frequency):
    for i in range(256):
        i = (i + 1) % 256  # run from 0 to 255
        leds.fill(wheel(i))
        leds.show()
        time.sleep(frequency)

def rainbowCycle_mode(frequency,repeats=1):
    for idy in range(repeats):
        for j in range(256): # one cycle of all 256 colors in the wheel
            for i in range(numleds):
                leds[i] =wheel(((i * 256 // numleds) + j) % 256) 
            leds.show()
            time.sleep(frequency)
 
def brightness_change( frequency, color, step):
    if step > 0:
        dr=color[0]/step
        dg=color[1]/step
        db=color[2]/step
    # else
        #error out
    r = 0
    g = 0
    b = 0
    for i in range(step):
        time.sleep(frequency)
        r = int(i*dr)
        g = int(i*dg)
        b = int(i*db)
        leds.fill([r,g,b])
        leds.show()
    r0 =color[0]
    g0 =color[1]
    b0 =color[2]
    leds.fill(color)
    for i in range(step+1):
        r = int(r0-i*dr)
        g = int(g0-i*dg)
        b = int(b0-i*db)
        leds.fill([r,g,b])
        leds.show()
        time.sleep(frequency)

    

######################### MAIN LOOP ##############################
 # Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    parser.add_argument('-home', action='store_true', help='home mode activated for led stripe')
    parser.add_argument('-loading', action='store_true', help='home mode activated for led stripe')
    parser.add_argument('-flashing', action='store_true', help='home mode activated for led stripe')
    parser.add_argument('-gallery', action='store_true', help='home mode activated for led stripe')
    parser.add_argument('-picture', action='store_true', help='home mode activated for led stripe')

    args = parser.parse_args()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            
            
            if args.home:
                #Rainbow Mode
                rainbow_mode(0.05)
                #Rainbow Cycle
                rainbowCycle_mode(0.02,5)


            if args.gallery:
                #Brightnes change
                brightness_change(0.1,random_color(),50)
                
            if args.loading:
                #loading mode 2
                loading_mode2(random_color(),0.05,1)
                
            if args.flashing:
                #Flash mode
                flash_mode(0.5,5,random_color())
                
            if args.picture:
                brightness_change(0.1,[255,255,255],10)

            #loading mode 1
            #loading_mode1(random_color(),0.1,2)
            # Random Mode
            #random_mode(0.25,5)
            

    except KeyboardInterrupt:
            if args.clear:
                leds.fill(0)       
    
