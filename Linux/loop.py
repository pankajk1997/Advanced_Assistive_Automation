from time import sleep
from subprocess import call
import RPi.GPIO as GPIO
import pigpio

#Note the BOARD Mode
GPIO.setmode(GPIO.BOARD)

#Alarm Sensors
GPIO.setup(8,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)   #Fire Sensor
GPIO.setup(10,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)  #Motion Sensor
GPIO.setup(12,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)  #Gas Sensor

#Relay
GPIO.setup(37,GPIO.OUT) #Red Alarm Bulb
GPIO.setup(35,GPIO.OUT) #White Normal Bulb
GPIO.setup(33,GPIO.OUT) #First Switch
GPIO.setup(31,GPIO.OUT) #Second Switch

#Servo
GPIO.setup(40,GPIO.OUT)
GPIO.setup(38,GPIO.OUT)

#Keypad Columns
GPIO.setup(36,GPIO.OUT)         #36 - 22
GPIO.setup(32,GPIO.OUT)         #32 - 18
GPIO.setup(26,GPIO.OUT)         #26 - 16

#Keypad Rows
GPIO.setup(24,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)       #24 - 36
GPIO.setup(22,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)       #22 - 32
GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)       #18 - 26
GPIO.setup(16,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)       #16 - 24

#Initializing Keypad Columns
GPIO.output(36,GPIO.LOW)        #36 - 22
GPIO.output(32,GPIO.LOW)        #32 - 18
GPIO.output(26,GPIO.LOW)        #26 - 16

#Initializing Relay
GPIO.output(37,GPIO.LOW)
GPIO.output(35,GPIO.LOW)

#Initializing Servo PWM
servo1=21
servo2=20

pi = pigpio.pi()

pi.set_servo_pulsewidth(servo1, 1500)
pi.set_servo_pulsewidth(servo2, 1500)

i=0                 #Just an incrementer
chkalrm='0'         #No 'alarm' in beggining
unlock='0'          #Doors locked in beggining
passorig=[2,0,1,8]  #Original Password
passcode=[0,0,0,0]  #To store input password from keypad

#Writing '0' to 'unlock' and 'alarm' file
with open('/home/pi/Documents/HAP/unlock.txt','w') as f1:
    f1.write(unlock)
with open('/home/pi/Documents/HAP/alarm.txt','w') as f2:
    f2.write(chkalrm)

#Infinite Loop
while(True):

    #Read 'unlock' file which can be changed by other programs
    with open('/home/pi/Documents/HAP/unlock.txt','r') as f3:
        unlock=f3.read()

    #Choosing different type of alarm(chkalrm) to be written in 'alarm' file
    if chkalrm=='0':

        GPIO.output(37,GPIO.LOW)    #Switch OFF red bulb when no alarm

        if(GPIO.input(8)):
            chkalrm='1'             #Choose '1' in case of fire sensed
        elif unlock=='0':
            if(GPIO.input(10)):
                chkalrm='2'         #Choose '2' in case of motion sensed of thief
        elif(GPIO.input(12)):
            chkalrm='3'             #Choose '3' in case of gas sensed

        with open('/home/pi/Documents/HAP/alarm.txt','w') as f5:
            f5.write(chkalrm)       #Writing triggered alarm type to file
    
    elif chkalrm != '0':

        GPIO.output(37,GPIO.HIGH)   #Switch ON red bulb when alarm
        call("/home/pi/Documents/HAP/alarm.sh") #Playing Choosen Alarm

        GPIO.output(36,GPIO.HIGH)
        if(GPIO.input(16)):
            chkalrm='0'             #Stop alarm when keypress
            call("/home/pi/Documents/HAP/pkill.sh")    #Stop voice alarm when keypress
        GPIO.output(36,GPIO.LOW)

        with open('/home/pi/Documents/HAP/alarm.txt','w') as f5:
            f5.write(chkalrm)       #Writing changes in alarm to file

    if unlock=='1':

        GPIO.output(35,GPIO.HIGH)   #Switch ON White bulb when unlocked

        GPIO.output(26,GPIO.HIGH)
        if(GPIO.input(16)):
            unlock='0'              #Lock doors when keypress
        GPIO.output(26,GPIO.LOW)

        if unlock=='0':
            with open('/home/pi/Documents/HAP/unlock.txt','w') as f4:
                f4.write(unlock)        #Writing change in lock condition to file

        pi.set_servo_pulsewidth(servo1, 500)
        pi.set_servo_pulsewidth(servo2, 500)
        print("SERVO OPEN")

    elif unlock=='0':

        GPIO.output(35,GPIO.LOW)    #Switch OFF White bulb when locked

        #Taking input from 4x3 keypad
        GPIO.output(36,GPIO.HIGH)
        if(GPIO.input(24)):
            sleep(0.1)
            if(GPIO.input(24)):
                passcode[i]=1
                i+=1
        elif(GPIO.input(22)):
            sleep(0.1)
            if(GPIO.input(22)):
                passcode[i]=4
                i+=1
        elif(GPIO.input(18)):
            sleep(0.1)
            if(GPIO.input(18)):
                passcode[i]=7
                i+=1
        GPIO.output(36,GPIO.LOW)

        GPIO.output(32,GPIO.HIGH)
        if(GPIO.input(24)):
            sleep(0.1)
            if(GPIO.input(24)):
                passcode[i]=2
                i+=1
        elif(GPIO.input(22)):
            sleep(0.1)
            if(GPIO.input(22)):
                passcode[i]=5
                i+=1
        elif(GPIO.input(18)):
            sleep(0.1)
            if(GPIO.input(18)):
                passcode[i]=8
                i+=1
        elif(GPIO.input(16)):
            sleep(0.1)
            if(GPIO.input(16)):
                passcode[i]=0
                i+=1
        GPIO.output(32,GPIO.LOW)

        GPIO.output(26,GPIO.HIGH)
        if(GPIO.input(24)):
            sleep(0.1)
            if(GPIO.input(24)):
                passcode[i]=3
                i+=1
        elif(GPIO.input(22)):
            sleep(0.1)
            if(GPIO.input(22)):
                passcode[i]=6
                i+=1
        elif(GPIO.input(18)):
            sleep(0.1)
            if(GPIO.input(18)):
                passcode[i]=9
                i+=1
        GPIO.output(26,GPIO.LOW)

        if((i>3)):                  #Proceed (after entering 4 digit password)
            i=0                     #Restart password input
            if passcode==passorig:
                unlock='1'          #Unlock when password matched
                with open('/home/pi/Documents/HAP/unlock.txt','w') as f4:
                    f4.write(unlock)
            call("/home/pi/Documents/HAP/unlock.sh") #Voice feedback of authentication status
            sleep(2)

        pi.set_servo_pulsewidth(servo1, 1500)
        pi.set_servo_pulsewidth(servo2, 1500)
        print("SERVO CLOSE")

        #For Debugging
        print(passcode)
        print(chkalrm)
        print(unlock)
        print(i)

    with open('/home/pi/Documents/HAP/switch1.txt','r') as f6:
        switch1=f6.read()
    with open('/home/pi/Documents/HAP/switch2.txt','r') as f7:
        switch2=f7.read()

    if switch1=='0':
        GPIO.output(33,GPIO.LOW)
    elif switch1=='1':
        GPIO.output(33,GPIO.HIGH)

    if switch2=='0':
        GPIO.output(31,GPIO.LOW)
    elif switch2=='1':
        GPIO.output(31,GPIO.HIGH)
