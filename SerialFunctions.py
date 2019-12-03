############################
## SFWENG 3K04
## Group 33
## Nov 2019

############################
## Serial Functions

def sendparameters():
    import serial


    mode=1
    lower_rate=60
    max_sens_rate=120
    fixed_av_delay=200
    atrial_pulse_amp=3500
    vent_pulse_amp=3500
    atrial_pulse_width=50000
    vent_pulse_width=50000
    VRP=250
    ARP=250
    activity_threshold=3
    reaction_time=1
    response_factor=480
    recovery_time=600



    pacemaker=serial.Serial()
    pacemaker.port='COM5'
    pacemaker.baudrate=115200
    pacemaker.open()

    pacemaker.write(mode.to_bytes(2,'little',signed=False))
    pacemaker.write(lower_rate.to_bytes(2,'little',signed=False))
    pacemaker.write(max_sens_rate.to_bytes(2,'little',signed=False))
    pacemaker.write(fixed_av_delay.to_bytes(2,'little',signed=False))
    pacemaker.write(atrial_pulse_amp.to_bytes(2,'little',signed=False))
    pacemaker.write(vent_pulse_amp.to_bytes(2,'little',signed=False))
    pacemaker.write(atrial_pulse_width.to_bytes(2,'little',signed=False))
    pacemaker.write(vent_pulse_width.to_bytes(2,'little',signed=False))
    pacemaker.write(VRP.to_bytes(2,'little',signed=False))
    pacemaker.write(ARP.to_bytes(2,'little',signed=False))
    pacemaker.write(activity_threshold.to_bytes(2,'little',signed=False))
    pacemaker.write(reaction_time.to_bytes(2,'little',signed=False))
    pacemaker.write(response_factor.to_bytes(2,'little',signed=False))
    pacemaker.write(recovery_time.to_bytes(2,'little',signed=False))

    pacemaker.close()



def sendtest():
    import serial
    ser=serial.Serial()
    ser.port='COM5'
    ser.baudrate=115200

    send1=0
    send2=1
    send3=0
    send4=0

    arr=bytearray([send1,send2,send3,send4])
    ser.open()
    ser.write(arr)
    #ser.write(send1.to_bytes(1,'little', signed=False))
    #ser.write(send2.to_bytes(1,'little', signed=False))
    #ser.write(send3.to_bytes(1,'little', signed=False))
    #ser.write(send4.to_bytes(1,'little', signed=False))
    ser.close()
    
############################
## Receive data from pacemaker to display values in pacing mode
## called on press of button

#def PaceModesReceive():
    

############################
## Send values to pacemaker to change mode and update settings


############################
## Receive values contiuously from pacemaker
