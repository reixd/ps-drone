#########
# firstConfig.py
# This program is part of the online PS-Drone-API-tutorial on www.playsheep.de/drone.
# It shows how to set and read out configurations of a Parrot AR.Drone 2.0 using the PS-Drone-API. The drone will stay on the ground.
# Dependencies: a POSIX OS, PS-Drone-API 2.0 beta or higher.
# (w) J. Philipp de Graaff, www.playsheep.de, 2014
##########
# LICENCE:
#   Artistic License 2.0 as seen on http://opensource.org/licenses/artistic-license-2.0 (retrieved December 2014)
#   Visit www.playsheep.de/drone or see the PS-Drone-API-documentation for an abstract from the Artistic License 2.0.
###########

##### Suggested clean drone startup sequence #####
import time, sys
import api.ps_drone as ps_drone                                                     # Import PS-Drone-API

drone = ps_drone.Drone()                                            # Start using drone	
drone.startup()                                                     # Connects to drone and starts subprocesses

drone.reset()                                                       # Sets the drone's status to good (LEDs turn green when red)
while (drone.getBattery()[0] == -1):    time.sleep(0.1)             # Wait until the drone has done its reset
print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])   # Gives a battery-status
drone.useDemoMode(True)                                             # Just give me 15 basic dataset per second (is default anyway)
time.sleep(0.5)                                                     # Gives time to awake fully

##### Mainprogram begin #####
# Just list the configuration, it is already synchronized
for i in drone.ConfigData:              print i

# Take a closer look at an option...
print "\nSample: ",
for i in drone.ConfigData:
    if i[0] == "control:altitude_max":  print str(i)+"   Count: "+str(drone.ConfigDataCount)+"   Timestamp: "+str(drone.ConfigDataTimeStamp)

# ... and change it
print "-----"
print "Setting \"control:altitude_max\" to \"2999\"..."
CDC =     drone.ConfigDataCount
NDC =     drone.NavDataCount
refTime = time.time()	
drone.setConfig("control:altitude_max","2999")                      # Request change of an option
while CDC == drone.ConfigDataCount:     time.sleep(0.001)           # Wait until configuration has been set (after resync is done)
print "   Finished after "+str(time.time()-refTime)+" seconds, "+str(drone.NavDataCount-NDC)+" NavData where received meanwhile."
for i in drone.ConfigData:
    if i[0] == "control:altitude_max":	print "   "+str(i)+"   Count: "+str(drone.ConfigDataCount)+"   Timestamp: "+str(drone.ConfigDataTimeStamp)

# Change an option a couple of times
print "\n-----"
print "Setting \"control:altitude_max\" to \"2996\", then to \"2997\", \"2998\", \"2999\" and \"3000\"..."
CDC =     drone.ConfigDataCount
NDC =     drone.NavDataCount
refTime = time.time()
drone.setConfig("control:altitude_max","2996")                      # Request change of an option...
drone.setConfig("control:altitude_max","2997")                      # ...request change of the option again...
drone.setConfig("control:altitude_max","2998")                      # ...and again
drone.setConfig("control:altitude_max","2999")                      # PS-Drone detects and deletes double...
drone.setConfig("control:altitude_max","3000")                      # ...requests and sets the last one only
while CDC == drone.ConfigDataCount:    time.sleep(0.001)            # Wait until configuration has been set (after resync is done)
print "   Finished after "+str(time.time()-refTime)+" seconds, "+str(drone.NavDataCount-NDC)+" NavData where received meanwhile."
for i in drone.ConfigData:
    if i[0] == "control:altitude_max":	print "   "+str(i)+"   Count: "+str(drone.ConfigDataCount)+"   Timestamp: "+str(drone.ConfigDataTimeStamp)

print "\n-----"
print "Setting \"control:altitude_max\" to \"2980\", \"control:altitude_min\" to \"499\" and \"video:video_on_usb\" to \"false\"..."
CDC =     drone.ConfigDataCount
NDC =     drone.NavDataCount
refTime = time.time()
drone.setConfig("control:altitude_max","2980")                      # Request change of an option
drone.setConfig("control:altitude_min","499")                       # Request change of an other option
drone.setConfig("video:video_on_usb","false")                       # Request change of an other option
while CDC == drone.ConfigDataCount:     time.sleep(0.001)           # Wait until configuration has been set (after resync is done)
print "   Finished after "+str(time.time()-refTime)+" seconds, "+str(drone.NavDataCount-NDC)+" NavData where received meanwhile."
for i in drone.ConfigData:
    if i[0]=="control:altitude_max" or i[0]=="control:altitude_min" or i[0]=="video:video_on_usb" :
        print "   "+str(i)+"   Count: "+str(drone.ConfigDataCount)+"   Timestamp: "+str(drone.ConfigDataTimeStamp)

print "\n-----"
print "Just resyncing the drones configuration..."
CDC =     drone.ConfigDataCount
NDC =     drone.NavDataCount
refTime = time.time()
drone.getConfig()                                                   # Request resyncing
while CDC == drone.ConfigDataCount:     time.sleep(0.001)           # Wait until configuration has been set (after resync is done)
print "   Finished after "+str(time.time()-refTime)+" seconds, "+str(drone.NavDataCount-NDC)+" NavData where received meanwhile."
