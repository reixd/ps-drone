#########
# BatPrepare.py
# Lithium-ion-batteries will loose their capacity, if they were stored full powered.
# This program will rotate the propellers of the drone (but not make it flight), till battery reached 50% capacity.
# Dependencies: a POSIX OS, PS-Drone-API 2.0 beta or higher.
# (w) J. Philipp de Graaff, www.playsheep.de, 2015
##########
# LICENCE:
#   Artistic License 2.0 as seen on http://opensource.org/licenses/artistic-license-2.0 (retrieved December 2014)
#   Visit www.playsheep.de/drone or see the PS-Drone-API-documentation for an abstract from the Artistic License 2.0.
###########

##### Suggested clean drone startup sequence #####
import time
import api.ps_drone as ps_drone                                                     # Import PS-Drone-API

drone = ps_drone.Drone()                                            # Start using drone	
drone.startup()                                                     # Connects to drone and starts subprocesses

while (drone.getBattery()[0] == -1):    time.sleep(0.1)             # Wait until the drone has done its reset
print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])   # Gives a battery-status
drone.useDemoMode(True)                                             # Just give me 15 basic dataset per second (is default anyway)
time.sleep(0.5)                                                     # Gives time to awake fully

pwm		= 100
status	= 100
stop	= False
odrive	= False
while status>50 and not stop:
	status=drone.getBattery()[0]
	drone.printLineUp()
	print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])+"   PWM: "+str(pwm)+"  Overdrive:"+str(odrive)+"         "
	time.sleep(0.1)
	key=drone.getKey()
	if key!="":
		if   key=="+": 	pwm	 += 1
		elif key=="-": 	pwm	 -= 1
		elif key=="o" and odrive:		odrive	= False
		elif key=="o" and not odrive:	odrive	= True
		else:					stop = True
	if pwm>115 and not odrive:		pwm	 	=  115
	if pwm>255 and 		odrive:		pwm	 	=  255
	if pwm<50:						pwm	 =  50
	drone.thrust(pwm,pwm,pwm,pwm)
drone.thrust(0,0,0,0)
if stop:	print "Aborted !"
else:		print "Done"
