 #########
# glideNstop.py
# This program is part of the online PS-Drone-API-tutorial on www.playsheep.de/drone.
# It shows the difference between active stopping and holding position of a Parrot AR.Drone 2.0 and "stopping"
#  by reducing the thrust to 0.0 of the moving drone, using the PS-Drone-API. The drone will be flying.
# Dependencies: a POSIX OS, PS-Drone-API 2.0 beta or higher.
# (w)+(c) J. Philipp de Graaff, www.playsheep.de, 2014
##########
# LICENCE:
#   Artistic License 2.0 as seen on http://opensource.org/licenses/artistic-license-2.0 (retrieved December 2014)
#   Visit www.playsheep.de/drone or see the PS-Drone-API-documentation for an abstract from the Artistic License 2.0.
###########

##### Suggested clean drone startup sequence #####
import time, sys
import api.ps_drone as ps_drone                                          # Import PS-Drone-API

drone = ps_drone.Drone()                                 # Start using drone					
drone.startup()                                          # Connects to drone and starts subprocesses

drone.reset()                                            # Sets drone's status to good (LEDs turn green when red)
while (drone.getBattery()[0] == -1):   time.sleep(0.1)   # Wait until drone has done its reset
print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])	# Gives a battery-status
if drone.getBattery()[1] == "empty":   sys.exit()        # Give it up if battery is empty

drone.useDemoMode(True)                                  # Just give me 15 basic dataset per second (is default anyway)
drone.getNDpackage(["demo"])                             # Packets, which shall be decoded
time.sleep(0.5)                                          # Give it some time to awake fully after reset

drone.takeoff()                                          # Fly, drone, fly !
while drone.NavData["demo"][0][2]:     time.sleep(0.1)   # Wait until the drone is really flying (not in landed-mode anymore)

##### Mainprogram begin
print "The Drone is flying now, land it with any key but <space>"

gliding = False
print "The Drone is holding its position, toggle \"hold position\" and \"glide\" with <space>-key."

end = False
while not end:
    key = drone.getKey()                                 # Get a pressed key
    if key == " ":
        if gliding:
            gliding = False
            drone.stop()                                 # Stop and hold position
            print "Drone is now holding its position"
        else:
            gliding = True
            drone.moveForward(0)                         # Just do not fly actively in any direction
            print "Drone is now gliding"
    elif key:        end = True                          # End this loop, you can also use sys.exit()
    else:            time.sleep(0.1)                     # Wait until next looping
