from gpiozero import Button, LED

FILE_PATH = "./registered.txt"

# -----------------------------------------------------
class Scanner:
    def __init__(self) -> None:
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
        self.button1.when_pressed = self.run_fwd # go to switch 1 and cancel 
        self.button2.when_pressed = self.run_bwd # go to switch 2
        self.switch1.when_released = self.cancel_move1
        self.switch2.when_released = self.cancel_move2

        # Declare default values
        self.prices_dict = {}
        self.total_price = 0
        self.total_count = 0
        self.red_count = 0
        self.silver_count = 0
        self.gold_count = 0
        self.black_count = 0

    def enable_button1(self):
        self.button1.when_pressed = self.run_fwd #go to switch 1

    def disable_button1(self):
        self.button1.when_pressed = None

    def enable_button2(self):
        self.button2.when_pressed = self.run_bwd #go to switch 2

    def disable_button2(self):
        self.button2.when_pressed = None 
        
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
        self.pul.blink(0.001,0.001)
        self.dir.on()
        print("pass")
        
    def run_bwd(self):
        self.ena.on()
        self.pul.blink(0.001,0.001)
        self.dir.off()
        print("pass")

    def initialize(self):
        with open(FILE_PATH, "r") as prices:
            prices_list = prices.read().split("\n")
            # print(prices_list)
            
            self.prices_dict = {}
            for price in prices_list[:-1]:
                id, price = price.split()
                self.prices_dict[id] = int(price)
            print(self.prices_dict)

    def get_price(self, rfid):
        if rfid not in self.prices_dict.keys():
            print("cannot find rfid")
            return 0
        print("the price is", self.prices_dict[rfid])
        return self.prices_dict[rfid]

    def add_item(self, rfid):
        price = self.get_price(rfid)
        self.total_price += price
        self.total_count += 1
        if price == 40:
            self.red_count += 1
        elif price == 60:
            self.silver_count += 1
        elif price == 80:
            self.gold_count += 1
        elif price == 120:
            self.black_count += 1
        else:
            print(f"Another price detected: {price}")

        print(f"The total cost so far is {self.total_price}")
        print(f"Plate count (red, silver, gold, black): {self.red_count}, {self.silver_count}, {self.gold_count}, {self.black_count}")
        print(f"Total plates: {self.total_count}")

    def reset_total(self):
        print("Resetting total price, which was", self.total_price)
        print("Resetting total count, which was", self.total_count)

        self.total_price = 0
        self.total_count = 0


if __name__ == "__main__":
    scanner = Scanner()
    print("Welcome to Sushirov")
    print("Please return the dishes tp the tray")
    scanner.initialize()
    while True:
        scanned_price = input()
        if scanned_price == "q":
            break
        scanner.add_item(scanned_price)
