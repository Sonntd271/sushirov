from time import sleep
from gpiozero import Button, LED


class Motor:
    def __init__(self) -> None: 
        try:
            self.pulse_dur = 0.0002
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

    def move_cont(self, duration=2):
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
        # print("BUTTON 6 IS TRIGGERED")

    def cancel_move1(self):
        self.ena.off()
        self.pul.off()
        # print("BUTTON 12 IS TRIGGERED")
        
    def run_fwd(self):
        self.ena.on()
        self.pul.blink(self.pulse_dur, self.pulse_dur)
        self.dir.on()
        # print("pass")
        
    def run_bwd(self):
        self.ena.on()
        self.pul.blink(self.pulse_dur, self.pulse_dur)
        self.dir.off()
        # print("pass")

if __name__ == "__main__":
    motor = Motor()
    for _ in range(10):
        motor.move_cont()
