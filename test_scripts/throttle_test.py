from typing import Optional
import time

def map_range(x: float, X_min: float, X_max: float, Y_min: float, Y_max: float) -> float:
    '''
    Linear mapping between two ranges of values
    '''
    X_range = X_max - X_min
    Y_range = Y_max - Y_min
    XY_ratio = X_range/Y_range

    return ((x-X_min) / XY_ratio + Y_min)

        
class PCA9685:
    ''' 
    PWM motor controler using PCA9685 boards. 
    This is used for most RC Cars
    '''
    def __init__(self, channel:int, address:int, frequency:int=60, busnum:Optional[int]=None, init_delay:float=0.1):

        self.default_freq = 60
        self.pwm_scale = frequency / self.default_freq

        import Adafruit_PCA9685
        # Initialise the PCA9685 using the default address (0x40).
        if busnum is not None:
            from Adafruit_GPIO import I2C
            #replace the get_bus function with our own
            def get_bus():
                return busnum
            I2C.get_default_bus = get_bus
        self.pwm = Adafruit_PCA9685.PCA9685(address=address)
        self.pwm.set_pwm_freq(frequency)
        self.channel = channel
        time.sleep(init_delay) # "Tamiya TBLE-02" makes a little leap otherwise

    def set_pulse(self, pulse:int ):
        self.pwm.set_pwm(self.channel, 0, int(pulse * self.pwm_scale))

    def run(self, pulse: int):
        self.set_pulse(pulse)

class PWMThrottle:
    """
    Wrapper over a PWM motor cotnroller to convert -1 to 1 throttle
    values to PWM pulses.
    """
    MIN_THROTTLE = -1
    MAX_THROTTLE =  1

    def __init__(self, 
        controller:PCA9685,
        max_pulse:int=4095,
        min_pulse:int=-4095,
        zero_pulse:int=0):

        self.controller = controller
        self.max_pulse = max_pulse
        self.min_pulse = min_pulse
        self.zero_pulse = zero_pulse
        
        #send zero pulse to calibrate ESC
        print("Init ESC")
        self.controller.set_pulse(self.zero_pulse)
        time.sleep(1)


    def run(self, throttle: float):
        if throttle > 0:
            pulse = map_range(throttle,
                                    0, self.MAX_THROTTLE, 
                                    self.zero_pulse, self.max_pulse)
            self.controller.pwm.set_pwm(self.controller.channel,0,pulse)
            self.controller.pwm.set_pwm(self.controller.channel+1,0,4095)
            self.controller.pwm.set_pwm(self.controller.channel+2,0,0)
            self.controller.pwm.set_pwm(self.controller.channel+3,0,0)
            self.controller.pwm.set_pwm(self.controller.channel+4,0,pulse)
            self.controller.pwm.set_pwm(self.controller.channel+7,0,pulse)
            self.controller.pwm.set_pwm(self.controller.channel+6,0,4095)
            self.controller.pwm.set_pwm(self.controller.channel+5,0,0)      
        else:
            pulse = map_range(throttle,
                                    self.MIN_THROTTLE, 0, 
                                    self.min_pulse, self.zero_pulse)
            self.controller.pwm.set_pwm(self.controller.channel,0,- pulse)
            self.controller.pwm.set_pwm(self.controller.channel+2,0,4095)
            self.controller.pwm.set_pwm(self.controller.channel+1,0,0)
            self.controller.pwm.set_pwm(self.controller.channel+3,0,- pulse)
            self.controller.pwm.set_pwm(self.controller.channel+4,0,0)
            self.controller.pwm.set_pwm(self.controller.channel+7,0,- pulse)
            self.controller.pwm.set_pwm(self.controller.channel+5,0,4095)
            self.controller.pwm.set_pwm(self.controller.channel+6,0,0)
        
    def shutdown(self):
        self.run(0) #stop vehicle

#THROTTLE
THROTTLE_CHANNEL = 0            #channel on the 9685 pwm board 0-15
THROTTLE_FORWARD_PWM = 4095      #pwm value for max forward throttle
THROTTLE_STOPPED_PWM = 0      #pwm value for no movement
THROTTLE_REVERSE_PWM = -4095      #pwm value for max reverse throttle
THROTTLE_PCA9685_I2C_ADDR1 = 0x60 #I2C address for the first set of 9685s
THROTTLE_PCA9685_BUSNUM = 1      #I2C bus number for the first set of 9685s 
throttle_controller = PCA9685(THROTTLE_CHANNEL, THROTTLE_PCA9685_I2C_ADDR1, frequency=1600, busnum=THROTTLE_PCA9685_BUSNUM)

throttle = PWMThrottle(controller=throttle_controller,
                            max_pulse=THROTTLE_FORWARD_PWM,
                            zero_pulse=THROTTLE_STOPPED_PWM, 
                            min_pulse=THROTTLE_REVERSE_PWM)

throttle.run(0.5)