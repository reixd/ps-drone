#########
# multiConfig.py
# This program is part of the online PS-Drone-API-tutorial on www.playsheep.de/drone.
# It shows how to set and read out multi-configuration of a Parrot AR.Drone 2.0 using the PS-Drone-API..
# The drone will stay on the ground.
# Dependencies: a POSIX OS, PS-Drone-API 2.0 beta or higher.
# (w) J. Philipp de Graaff, www.playsheep.de, 2014
##########
# LICENCE:
#   Artistic License 2.0 as seen on http://opensource.org/licenses/artistic-license-2.0 (retrieved December 2014)
#   Visit www.playsheep.de/drone or see the PS-Drone-API-documentation for an abstract from the Artistic License 2.0.
###########

##### Suggested clean drone startup sequence #####
import time, sys
import api.ps_drone as ps_drone                                              # Import PS-Drone-API

drone = ps_drone.Drone()                                     # Start using drone					
drone.startup()                                              # Connects to drone and starts subprocesses

drone.reset()                                                # Sets the drone's status to good (LEDs turn green when red)
while (drone.getBattery()[0] == -1):  time.sleep(0.1)        # Wait until the drone has done its reset
print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])   # Gives the battery-status
drone.useDemoMode(True)                                      # Just give me 15 basic dataset per second (is default anyway)
time.sleep(0.5)                                              # Gives time to awake fully after reset

##### Mainprogram begin #####
# Take a closer look at an option...
print "default IDs:"
for i in drone.ConfigData:
    if i[0].count("custom:")==1 and i[0].count("_id")==1:    print str(i)

print "set default multiconfiguration:"
drone.setConfigAllID()
CDC = drone.ConfigDataCount
while CDC == drone.ConfigDataCount:    time.sleep(0.0001)    # Wait until configuration has been set (after resync is done)
for i in drone.ConfigData:
    if i[0].count("custom:")==1 and i[0].count("_id")==1:    print str(i) 
