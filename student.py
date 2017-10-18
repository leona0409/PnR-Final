import pigo
import time  # import just in case students need
import random

# setup logs
import logging
LOG_LEVEL = logging.INFO
LOG_FILE = "/home/pi/PnR-Final/log_robot.log"  # don't forget to make this file!
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)


class Piggy(pigo.Pigo):
    """Student project, inherits teacher Pigo class which wraps all RPi specific functions"""

    def __init__(self):
        """The robot's constructor: sets variables and runs menu loop"""
        print("I have been instantiated!")
        # Our servo turns the sensor. What angle of the servo( ) method sets it straight?
        self.MIDPOINT = 77
        # YOU DECIDE: How close can an object get (cm) before we have to stop?
        self.SAFE_STOP_DIST = 30
        self.HARD_STOP_DIST = 15
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.LEFT_SPEED = 140
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.RIGHT_SPEED = 140
        # This one isn't capitalized because it changes during runtime, the others don't
        self.turn_track = 0
        # Our scan list! The index will be the degree and it will store distance
        self.scan = [None] * 180
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        while True:
            self.stop()
            self.menu()

    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like to add an experimental method
        menu = {"n": ("Navigate forward", self.nav),
                "d": ("Dance", self.cotton_eye_joe),
                "o": ("Obstacle count", self.obstacle_count),
                "c": ("Calibrate", self.calibrate),
                "s": ("Check status", self.status),
                "q": ("Quit", quit_now)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = raw_input("Your selection: ")
        # activate the item selected
        menu.get(ans, [None, error])[1]()

    # YOU DECIDE: How does your GoPiggy dance?
    def cotton_eye_joe(self):
        """executes a series of methods that add up to a compound dance"""
        print("\n---- LET'S DANCE ----\n")
        ##### WRITE YOUR FIRST PROJECT HERE
        if self.safety_check():
            print("About to dance")
            self.shake_left()
            self.heel()
            self.shake_right()
            self.toe()
            self.pause()
            self.look_forward()
            self.walk_to_right()
            self.turn_to_left()
            self.shake_left()
            self.shake_right()
            self.look_forward()
            self.swing()
            self.ending_flourish()

    def safety_check(self):
        self.servo(self.MIDPOINT)  # look straight ahead
        for loop in range(9):
            if not self.is_clear():
                print("NOT GOING TO DANCE")
                return False
            self.encR(4)
            print ("Check #%d" % (loop + 1))  # figure out 90 deg
        print("Safe to dance!")
        return True

    def shake_right(self):
        """subroutine of dance method"""
        for x in range(3):
            self.servo(20)
            self.servo(50)
            self.servo(20)

    def shake_left(self):
        """subroutine of dance method"""
        for x in range(3):
            self.servo(130)
            self.servo(100)
            self.servo(130)

    def heel(self):
        """subroutine of dance method"""
        # makes the robot go forward
        for x in range (3):
            self.encF(2)

    def toe(self):
        """subroutine of dance method"""
        # makes the robot go backwards
        for x in range(3):
            self.encB(2)

    def walk_to_right(self):
        """subroutine of dance method"""
        #turn to right and go forward
        for x in range(1):
            self.encR(8)
            self.encF(30)

    def turn_to_left(self):
        """subroutine of dance method"""
        #turns 180, goes forward
        for x in range(4):
            self.encL(27)
            self.encF(20)

    def pause(self):
        """subroutine of dance method"""
        time.sleep(2)

    def look_forward(self):
        """subroutine of dance method"""
        self.servo(77)

    def ending_flourish(self):
        """subroutine of dance method"""
        #spin around multiple times
        for x in range(3):
            self.encR(27)
        print("Thank you for watching")

    def swing(self):
        """subroutine of dance method"""
        #turns slightly to the left as head turns right, then turns to right as head turns left
        for x in range(3):
            self.encR(6)
            self.servo(20)
            self.encL(6)
            self.servo(100)

    def nav(self):
        """auto pilots and attempts to maintain original heading"""
        logging.debug("Starting the nav method")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        for x in range(20):
            if self.is_clear():
                self.servo(self.MIDPOINT)
                self.cruise()
            else:
                self.encR(2)

    def cruise(self):
        """drive straight while path is clear"""
        self.fwd()
        print("about to drive forward")
        while self.dist() > self.SAFE_STOP_DIST:
            time.sleep(.1)


    def obstacle_count(self):
        """scans and estimates the number of obstacles within sight"""
        for x in range(4):
            self.wide_scan(count=5)
            found_something = False
            counter = 1
            threshold = 300
            for distance in self.scan:
                if distance and distance < threshold and not found_something:
                    found_something = True
                    print("Object #%d found, I think" % counter)
                if distance and distance > threshold and found_something:
                    found_something = False
                    counter += 1
            print("\n-------I see %d object(s)------\n" % counter)
            self.encR(7)

        #Add in a 360 rotation
        #find the area that has the widest gap and turn robot to that gap



####################################################
############### STATIC FUNCTIONS

def error():
    """records general, less specific error"""
    logging.error("ERROR")
    print('ERROR')


def quit_now():
    """shuts down app"""
    raise SystemExit

##################################################################
######## The app starts right here when we instantiate our GoPiggy


try:
    g = Piggy()
except (KeyboardInterrupt, SystemExit):
    pigo.stop_now()
except Exception as ee:
    logging.error(ee.__str__())
