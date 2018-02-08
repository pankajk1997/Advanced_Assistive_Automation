from time import sleep
from subprocess import call
import RPi.GPIO as GPIO

#Note the BOARD Mode
GPIO.setmode(GPIO.BOARD)

#Alarm Sensors
GPIO.setup(8,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)   #Fire Sensor
GPIO.setup(10,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)  #Motion Sensor
GPIO.setup(12,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)  #Gas Sensor

#Relay
GPIO.setup(37,GPIO.OUT) #Red Alarm Bulb
GPIO.setup(35,GPIO.OUT) #White Normal Bulb

#Servo
GPIO.setup(40,GPIO.OUT)
GPIO.setup(38,GPIO.OUT)

#Keypad Columns
GPIO.setup(22,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)

#Keypad Rows
GPIO.setup(36,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(32,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(26,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(24,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

#Initializing Keypad Columns
GPIO.output(22,GPIO.LOW)
GPIO.output(18,GPIO.LOW)
GPIO.output(16,GPIO.LOW)

#Initializing Relay
GPIO.output(37,GPIO.LOW)
GPIO.output(35,GPIO.LOW)

#Initializing Servo PWM
pwm1=GPIO.PWM(40,50)
pwm2=GPIO.PWM(38,50)
pwm1.start(7.5)
pwm2.start(7.5)

i=0         ##Just an incrementer
chkalrm='0'     ##No 'alarm' in beggining
unlock='0'      ##Locked in beggining
passorig=[2,0,1,8]  #Original Password
passcode=[0,0,0,0]  ##To store input password from keypad
prevpass=passcode   ##To prevent duplicate fast input when keypad pressed
prevlok=0   ##To check unlock change

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
    if(GPIO.input(8)):
        chkalrm='1' #Choose '1' in case of fire sensed
    elif unlock=='0':
        if(GPIO.input(10)):
            chkalrm='2' #Choose '2' in case of motion sensed when locked
    elif(GPIO.input(12)):
        chkalrm='3' #Choose '3' in case of gas sensed
    else:       #Take password input from keypad when no alarm triggered
        #Taking input from 4x3 keypad
        GPIO.output(22,GPIO.HIGH)
        if(GPIO.input(36)):
            passcode[i]=1
            i+=1
        elif(GPIO.input(32)):
            passcode[i]=4
            i+=1
        elif(GPIO.input(26)):
            passcode[i]=7
            i+=1
        GPIO.output(22,GPIO.LOW)

        GPIO.output(18,GPIO.HIGH)
        if(GPIO.input(36)):
            passcode[i]=2
            i+=1
        elif(GPIO.input(32)):
            passcode[i]=5
            i+=1
        elif(GPIO.input(26)):
            passcode[i]=8
            i+=1
        elif(GPIO.input(24)):
            passcode[i]=0
            i+=1
        GPIO.output(18,GPIO.LOW)

        GPIO.output(16,GPIO.HIGH)
        if(GPIO.input(36)):
            passcode[i]=3
            i+=1
        elif(GPIO.input(32)):
            passcode[i]=6
            i+=1
        elif(GPIO.input(26)):
            passcode[i]=9
            i+=1
        GPIO.output(16,GPIO.LOW)

        if prevpass!=passcode:  #Prevent duplicate fast input by delay for 1 sec
            time.sleep(1)

        prevpass=passcode   #Getting ready for next input

    #Out of if-elif-else condition but inside while loop

    GPIO.output(16,GPIO.HIGH)
    if(GPIO.input(24)):     #Proceed (after entering password)
        i=0
        passcode=[0,0,0,0]
        if passcode==passorig:
            unlock='1'      #Unlock when password matched
            with open('/home/pi/Documents/HAP/unlock.txt','w') as f4:
                f4.write(unlock)
            call("/home/pi/Documents/HAP/unlock.sh")    #Voice feedback of authentication status
    GPIO.output(16,GPIO.LOW)

    GPIO.output(22,GPIO.HIGH)
    if(GPIO.input(24)):     #Stop Alarm
        chkalrm='0'
    GPIO.output(22,GPIO.LOW)

    with open('/home/pi/Documents/HAP/alarm.txt','w') as f5:
        f5.write(chkalrm)

    if prevlok != unlock:   #Locking and Unlocking Doors with Servo Motors
        if unlock == '1':
            pwm1.ChangeDutyCycle(2.5)
            pwm2.ChangeDutyCycle(2.5)
            sleep(2)
            GPIO.output(40,GPIO.LOW)
            GPIO.output(38,GPIO.LOW)
        else:
            pwm1.ChangeDutyCycle(7.5)
            pwm2.ChangeDutyCycle(7.5)
            sleep(2)
            GPIO.output(40,GPIO.LOW)
            GPIO.output(38,GPIO.LOW)

    prevlok=unlock

    if chkalrm != '0':
        GPIO.output(35,GPIO.HIGH)   #Switch ON red bulb when alarm
    else:
        GPIO.output(35,GPIO.LOW)

    if unlock == '1':
        GPIO.output(37,GPIO.HIGH)   #Switch ON White bulb when unlocked
    else:
        GPIO.output(37,GPIO.LOW)

    #Executing alarm based on content of 'alarm' file
    call("/home/pi/Documents/HAP/alarm.sh")
