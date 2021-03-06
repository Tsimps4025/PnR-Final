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
        self.MIDPOINT = 110
        # YOU DECIDE: How close can an object get (cm) before we have to stop?
        self.SAFE_STOP_DIST = 30
        self.HARD_STOP_DIST = 15
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.LEFT_SPEED = 160
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.RIGHT_SPEED = 165
        # This one isn't capitalized because it changes during runtime, the others don't
        self.turn_track = 0
        # Our scan list! The index will be the degree and it will store distance
        self.scan = [None] * 180
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        if __name__ == "__main__":
            while True:
                self.stop()
                self.menu()

    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like to add an experimental method
        menu = {"n": ("Navigate forward", self.nav),
                "d": ("Dance", self.dance),
                "o": ("Obstacle count", self.obstacle_count),
                "c": ("Calibrate", self.calibrate),
                "s": ("Check status", self.status),
                "h": ("Open House", self.open_house),
                "t": ("Test", self.skill_test),
                "q": ("Quit", quit_now)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = raw_input("Your selection: ")
        # activate the item selected
        menu.get(ans, [None, error])[1]()

    def skill_test(self):
        """demonstrates two nav skills"""
        choice = raw_input("Left/Right or Turn Until Clear")

        if "l" in choice:
            self.wide_scan(count=3) #scan the area
            # picks left or right

            # create two variables, left_total and right_total
            left_total = 0
            right_total = 0
            # loop from self.MIDPOINT - 60 to self.MIDPOINT
            for angle in range(self.MIDPOINT - 60, self.MIDPOINT):
                if self.scan[angle]:
                    # add up the numbers to right_total
                    right_total += self.scan[angle]
            # loop from self.MIDPOINT to self.MIDPOINT + 60
            for angle in range(self.MIDPOINT, self.MIDPOINT + 60):
                if self.scan[angle]:
                    # add up the numbers to left_total
                    left_total += self.scan[angle]
            # if right is bigger:
            if right_total > left_total:
                # turn right
                self.encR(10)
            # if left is bigger:
            if left_total > right_total:
                # turn left
                self.encL(10)

        else:
            # turns until it's clear
            while not self.is_clear():
                self.encR(3)





    def open_house(self):
        """reacts to dist measurement in a cute way"""
        while True:
            if self.dist() < 20:
                self.encB(5)
                self.encR(43)
                self.encF(5)
                self.encB(5)
                self.encF(5)
                self.encB(5)
                self.encF(5)
                self.encB(5)
                self.encF(5)

            time.sleep(.1)


    # YOU DECIDE: How does your GoPiggy dance?
    def dance(self):
        """executes a series of methods that add up to a compound dance"""
        if not self.safe_to_dance():
            print("\n---- NOT SAFE TO DANCE----\n")
            return
        print("\n---- LET'S DANCE ----\n")
        ##### WRITE YOUR FIRST PROJECT HERE
        self.gucci_shuffle()
        self.whip_my_hair()
        self.back_it_up()
        self.surprise()

    def safe_to_dance(self):
        """circles around and checks for any obstacles"""
        # check for problems
        for x in range(4):
            if not self.is_clear():
                return False
            self.encR(10)
        # if we find no problems
        return True

    def gucci_shuffle(self):
        """moves right,left,forward, and then rotates while moving head"""
        for x in range(4):
            self.encR(18)
            self.encL(18)
            self.encF(18)
            # starts moving and shaking head at same time
            self.left_rot()
            self.servo(80)
            time.sleep(1)
            self.servo(140)
            time.sleep(1)
            self.stop()

    def whip_my_hair(self):
        """whips hair back and forth"""
        for x in range(10):
            self.servo(80)
            self.servo(140)

    def back_it_up(self):
        """backs up while moving left and right"""
        for x in range(2):
            self.encR(9)
            self.encB(9)
            self.encL(9)
            self.encB(9)
            self.encR(20)

    # from Garret
    def surprise(self):
        """creates the coolest move you have ever seen"""
        for x in range(2):
            self.encF(30)
            self.encL(5)
            self.encB(5)
            self.encR(10)
            self.encB(5)
            self.encL(5)
            self.encB(5)
            self.encR(10)
            self.encB(5)
            self.encL(5)
            self.encB(5)
            self.encR(10)
            self.encB(5)
            self.encL(5)
            self.encB(5)
            self.encR(10)
            self.encB(5)


    def obstacle_count(self):
        """scans and estimates the number of obstacles within sight"""
        self.wide_scan()
        found_something = False
        counter = 0
        for ang, distance in enumerate(self.scan):
            if distance and distance < 200 and not found_something:
                found_something = True
                counter += 1
                print("Object # %d found, I think" % counter)
            if distance and distance > 200 and found_something:
                found_something = False
        print("\n----I SEE %d OBJECTS----\n" % counter)

    def safety_check(self):
        """subroutine of the dance method"""
        self.servo(self.MIDPOINT)  # look straight ahead
        for loop in range(4):
            if not self.is_clear():
                print("NOT GOING TO DANCE")
                return False
            print("Check #%d" % (loop + 1))
            self.encR(8)  # figure out 90 deg
        print("Safe to dance!")
        return True

    def nav(self):
        """auto pilots and attempts to maintain original heading"""
        logging.debug("Starting the nav method")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        count = 0

        error_count = 0
        while True:
            if self.is_clear():
                self.cruise()
                error_count = 0
            else:
                self.choose_direction()
                error_count += 1
                if error_count == 10:
                    raw_input("Wus poppin logang")

    def is_clear_infront(self):
        """check the scan array to see if there's a path dead ahead"""

        # checks for obstacles
        for ang in range(self.MIDPOINT - 10, self.MIDPOINT + 10):
            if self.scan[ang] and self.scan[ang] < self.SAFE_STOP_DIST:
                return False
        return True

    def cruise(self):
        """ drive straight while path is clear """
        self.fwd()
        while self.dist() > self.SAFE_STOP_DIST:
            time.sleep(.3)
        self.stop()

    def is_clear_ahead(self):
        for ang in range(self.MIDPOINT - 14, self.MIDPOINT +14):
            if self.scan[ang] and self.scan[ang] < self.SAFE_STOP_DIST:
                return False
    def is_clear(self):
        """does a 3-point scan around the midpoint, returns false if a test fails"""
        print("Running the is_clear method.")
        for x in range((self.MIDPOINT - 35), (self.MIDPOINT + 35), 5):
            self.servo(x)
            scan1 = self.dist()
            # double check the distance
            scan2 = self.dist()
            # if I found a different distance the second time....
            if abs(scan1 - scan2) > 2:
                scan3 = self.dist()
                # take another scan and average the three together
                scan1 = (scan1 + scan2 + scan3) / 3
            self.scan[x] = scan1
            print("Degree: " + str(x) + ", distance: " + str(scan1))
            if scan1 < self.SAFE_STOP_DIST:
                print("Doesn't look clear to me")
                return False
        self.servo(self.MIDPOINT)
        return True

    def choose_direction(self):
        """has the robot decide whether turning right or left is a better option"""
        self.wide_scan(count=5)  # scan the area
        left_total = 0
        right_total = 0
            # loop from self.MIDPOINT - 60 to self.MIDPOINT
        for angle in range(self.MIDPOINT - 60, self.MIDPOINT):
            if self.scan[angle]:
                    # add up the numbers to right_total
                right_total += self.scan[angle]
            # loop from self.MIDPOINT to self.MIDPOINT + 60
        for angle in range(self.MIDPOINT, self.MIDPOINT + 60):
            if self.scan[angle]:
                    # add up the numbers to left_total
                left_total += self.scan[angle]
        if self.is_clear_ahead():
            print("It's Clear")
            return
            # if right is bigger:
        if right_total > left_total:
                # turn right
            self.encR(12)
            # if left is bigger:
        if left_total > right_total:
                # turn left
            self.encL(12)
        return True

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
