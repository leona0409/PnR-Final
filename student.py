import pigo
import time  # import just in case students need
import datetime
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
        self.start_time = datetime.datetime.utcnow()
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
                "d": ("Dance", self.smooth_turn),
                "o": ("Obstacle Count", self.full_obstacle_count),
                "c": ("Calibrate", self.calibrate),
                "t": ("Test restore heading", self.test_restore_heading),
                "s": ("Check status", self.status),
                "q": ("Quit", quit_now),
                "2": ("Nav method attempt", self.nav_two)
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

    def restore_heading(self):
        """
        Uses self.turn_track to reorient to original heading
        """
        print("Restoring heading!")
        if self.turn_track > 0:
            self.encL(abs(self.turn_track))
        elif self.turn_track < 0:
            self.encR(abs(self.turn_track))

    def test_restore_heading(self):
        self.set_speed(100, 100)
        self.encR(5)
        self.encL(15)
        self.encR(10)
        self.encR(10)
        self.encL(7)
        time.sleep(2)
        self.restore_heading()

    def nav(self):
        """auto pilots and attempts to maintain original heading"""
        logging.debug("Starting the nav method")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        #right_now = datetime.datetime.utcnow()
        #difference = (right_now - self.start_time).seconds
        #print ("It took you %d seconds to run this" % difference)
        self.servo(self.MIDPOINT)
        while True:
            #if path is clear, robot will cruise
            self.restore_heading()
            if self.is_clear():
                print("Path is clear, moving forward.")
                self.nav_cruise()
            else:
                print("Path is not clear, turning left.")
                self.check_left()
                if self.is_clear():
                    #if path after turning left is clear, robot will cruise
                    self.nav_cruise()
                else:
                    #if path after turning left is not clear, robot will turn left one more time to check
                    self.check_left()
                    if self.is_clear():
                        self.nav_cruise()
                    else:
                        # if path after turning left is not clear, robot will turn left one more time to check
                        self.check_left()
                        if self.is_clear():
                            self.nav_cruise()
                        else:
                            #if path after checking left twice is not clear, robot will return to midpoint
                            print("Path to the left is not clear, turning to midpoint.")
                            self.restore_heading()
                            time.sleep(2)
                            if self.is_clear():
                                print("Path is clear, moving forward.")
                                self.nav_cruise()
                            else:
                                #if midpoint is not clear, robot will turn right and check
                                print("Path is not clear, turning right.")
                                self.check_right()
                                if self.is_clear():
                                    self.nav_cruise()
                                else:
                                    #if path after turning right is not clear, robot will turn right one more time to check
                                    self.check_right()
                                    if self.is_clear():
                                        self.nav_cruise()
                                    else:
                                        self.check_right()
                                        if self.is_clear():
                                            self.nav_cruise()
                                        else:
                                            #if path after turning left twice is not clear, robot will back up
                                            print("Paths are not clear, backing up.")
                                            self.restore_heading()
                                            self.encB(5)

    def nav_two(self):
        right_now = datetime.datetime.utcnow()
        difference = (right_now - self.start_time).seconds
        print("It took you %d seconds to run this" % difference)
        while self.encR(30):
            if self.scan[x] > 50:
                time.sleep(2)
                self.servo(x)
                self.encR(x%8)
                print("I have found an open area.")

    def check_right(self):
        self.servo(self.MIDPOINT)
        self.encR(4)
        time.sleep(1)

    def check_left(self):
        self.servo(self.MIDPOINT)
        self.encL(4)
        time.sleep(1)

    def nav_cruise(self):
        self.servo(self.MIDPOINT)
        self.cruise()

    def smooth_turn(self):
        self.encR()
        start = datetime.datetime.utcnow()
        while True:
            if self.dist() > 50:
                self.stop()
                print("I think I've found a good path.")
            elif datetime.datetime.utcnow() - start > datetime.timedelta(seconds=1):
                self.stop()
                print("I give up.")
            time.sleep(.2)

    def cruise(self):
        """drive straight while path is clear"""
        print("about to drive forward")
        self.fwd()
        while self.dist() > self.SAFE_STOP_DIST:
            time.sleep(.05)
        self.stop()

    def full_obstacle_count(self):
        counter = 0
        for x in range(4):
            counter += self.obstacle_count()
            self.encR(8)
        print("\n-------I see %d object(s) total------\n" % counter)

    def obstacle_count(self):
        """scans and estimates the number of obstacles within sight"""
        for x in range(65, 115):
            self.wide_scan(count=5)
            found_something = False
            counter = 0
            threshold = 60
            for self.scan[x] in self.scan:
                if self.scan[x] and self.scan[x] < threshold and not found_something:
                    found_something = True
                    counter += 1
                    print("Object #%d found, I think" % counter)
                if self.scan[x] and self.scan[x] > threshold and found_something:
                    found_something = False
            print("\n-------I see %d object(s)------\n" % counter)
            return counter

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
