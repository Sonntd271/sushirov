from time import sleep
from gpiozero import Button, LED

FILE_PATH = "../static/assets/registered.txt"

# -----------------------------------------------------
class Scanner:
    def __init__(self, fp=FILE_PATH, testing=False) -> None:
        if not testing:
            try:
                self.pulse_dur = 0.0001

                # Declare LEDs
                self.red = LED(17)
                self.green = LED(27)
                self.blue = LED(22)
                self.pul = LED(16)
                self.dir = LED(20)
                self.ena = LED(21) 

                # Declare buttons
                self.button1 = Button(23)
                self.button2 = Button(24)
                self.switch1 = Button(12)
                self.switch2 = Button(6)
            
                # Declare default button functions
                # self.button1.when_pressed = self.run_fwd # go to switch 1 and cancel 
                # self.button2.when_pressed = self.run_bwd # go to switch 2
                self.switch1.when_released = self.cancel_move1
                self.switch2.when_released = self.cancel_move2
            except:
                print("GPIO already initialized")

        # Declare default values
        self.prices_dict = {}
        self.summary_dict = {
            "count": {
                "red": 0,
                "silver": 0,
                "gold": 0,
                "black": 0,
                "others": 0
            },
            "total_price": 0
        }

        # Initializing sequence
        print("Welcome to Sushirov")
        print("Please return the dishes to the tray")
        with open(fp, "r") as prices:
            prices_list = prices.read().split("\n")
            # print(prices_list)
            
            self.prices_dict = {}
            for price in prices_list[:-1]:
                id, price = price.split()
                self.prices_dict[id] = int(price)
            # print(self.prices_dict)

    def move_cont(self, duration=1):
        print("Running forward")
        self.run_fwd()
        sleep(duration)
        print("Running backward")
        self.run_bwd()
        sleep(0.1)
        self.run_bwd()
        sleep(duration)
        print("Release switch")
        self.run_fwd()
        sleep(0.1)
        
    def cancel_move2(self):
        self.ena.off()
        self.pul.off()
        print("BUTTON 6 IS TRIGGERED")

    def cancel_move1(self):
        self.ena.off()
        self.pul.off()
        print("BUTTON 12 IS TRIGGERED")
        
    def run_fwd(self):
        self.ena.on()
        self.pul.blink(self.pulse_dur,self.pulse_dur)
        self.dir.on()
        print("pass")
        
    def run_bwd(self):
        self.ena.on()
        self.pul.blink(self.pulse_dur,self.pulse_dur)
        self.dir.off()
        print("pass")

    def get_price(self, rfid):
        if rfid not in self.prices_dict.keys():
            print("cannot find rfid")
            return 0
        price = self.prices_dict[rfid]
        print("the price is", price)
        return price

    def add_item(self, rfid):
        price = self.get_price(rfid)
        if price == -1:
            return False
        self.summary_dict["total_price"] += price    
        if price == 0:
            print("Please enter a valid rfid")
        elif price == 40:
            print("Red detected!")
            self.summary_dict["count"]["red"] += 1
        elif price == 60:
            print("Silver detected!")
            self.summary_dict["count"]["silver"] += 1
        elif price == 80:
            print("Gold detected!")
            self.summary_dict["count"]["gold"] += 1
        elif price == 120:
            print("Black detected!")
            self.summary_dict["count"]["black"] += 1
        else:
            print(f"Another price detected: {price}")
            self.summary_dict["count"]["others"] += 1

        print(f"Current total is {self.summary_dict['total_price']}")
        print(f"Plate count (red, silver, gold, black, others): {self.summary_dict['count']['red']}, {self.summary_dict['count']['silver']}, {self.summary_dict['count']['gold']}, {self.summary_dict['count']['black']}, {self.summary_dict['count']['others']}")
        print(f"Total plates: {sum(self.summary_dict['count'].values())}")
        
        return True

    def reset_total(self):
        print("Resetting...")
        print(f"Total price: {self.summary_dict['total_price']}")

        self.summary_dict = {
            "count": {
                "red": 0,
                "silver": 0,
                "gold": 0,
                "black": 0,
                "others": 0
            },
            "total_price": 0
        }


if __name__ == "__main__":
    scanner = Scanner()
    for _ in range(10):
        scanner.move_cont()
    # while True:
    #     scanned_price = input()
    #     if scanned_price == "q":
    #         break
    #     scanner.add_item(scanned_price)
