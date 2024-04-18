import time
from gpiozero import Button, LED
from signal import pause
# -----------------------------------------------------
red = LED(17)
green = LED(27)
blue = LED(22)

#red.on()
#time.sleep(10)

PUL = LED(16)
DIR = LED(20)
ENA = LED(21) 
button1 = Button(23)
button2 = Button(24)
switch1 = Button(12)
switch2 = Button(6)

def enable_button1():
    global button1
    button1.when_pressed = run_fwd #go to switch 1

def disable_button1():
    global button1
    button1.when_pressed = None

def enable_button2():
    global button2
    button2.when_pressed = run_bwd #go to switch 2

def disable_button2():
    global button2
    button2.when_pressed = None 
    
def cancel_move2():
	ENA.off()
	PUL.off()
	print("BUTTON 6 IS TRIGGERED")

def cancel_move1():
	ENA.off()
	PUL.off()
	print("BUTTON 12 IS TRIGGERED")
	
	
def run_fwd():
	ENA.on()
	PUL.blink(0.001,0.001)
	DIR.on()
	print("pass")
	
def run_bwd():
	ENA.on()
	PUL.blink(0.001,0.001)
	DIR.off()
	print("pass")
	
button1.when_pressed = run_fwd #go to switch 1 and cancel 
button2.when_pressed = run_bwd #go to switch 2
switch1.when_released= cancel_move1
switch2.when_released = cancel_move2




# -----------------------------------------------------

def initialize():
    prices = open("registered.txt", "r")

    prices_text = prices.read()
    prices_list = prices_text.split("\n")
    
    prices_dict = {}
    for price in prices_list[:-1]:
        temp = price.split()
        prices_dict[temp[0]] = int(temp[1])
    
    print(prices_dict)
    return prices_dict

prices_dict = {}
total_price = 0
total_count = 0

def get_price(rfid):
    if rfid not in prices_dict.keys():
        print("cannot find rfid")
        return 0
    print("the price is", prices_dict[rfid])
    return prices_dict[rfid]

def add_item(rfid):
    global total_price
    global total_count
    total_price += get_price(rfid)
    total_count += 1
    print("The total cost so far is", total_price)
    

def reset_total():
    global total_price
    global total_count
    
    print("Resetting total price, which was", total_price)
    print("Resetting total count, which was", total_count)

    total_price = 0
    total_count = 0
    
def main(args):
    print("Welcome to Bushido")
    print("Please return the dished on thr tray")
    global prices_dict
    prices_dict = initialize()
    while(True):
        scanned_price = input()
        add_item(scanned_price)
    pause()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
