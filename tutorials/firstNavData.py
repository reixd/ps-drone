#########
# firstNavData.py
# This program is part of the online PS-Drone-API-tutorial on www.playsheep.de/drone.
# It shows the general use of NavData from a Parrot AR.Drone 2.0 using the PS-Drone-API. The drone will stay on the ground.
# Dependencies: a POSIX OS, PS-Drone-API 2.0 beta or higher.
# (w)+(c) J. Philipp de Graaff, www.playsheep.de, 2014
##########
# LICENCE:
#   Artistic License 2.0 as seen on http://opensource.org/licenses/artistic-license-2.0 (retrieved December 2014)
#   Visit www.playsheep.de/drone or see the PS-Drone-API-documentation for an abstract from the Artistic License 2.0.
###########

##### Suggested clean drone startup sequence #####
import time, sys
import api.ps_drone as ps_drone                                            # Import PS-Drone-API

drone = ps_drone.Drone()                                   # Start using drone					
drone.startup()                                            # Connects to drone and starts subprocesses

drone.reset()                                              # Sets drone's status to good (LEDs turn green when red)
while (drone.getBattery()[0] == -1):   time.sleep(0.1)     # Waits until drone has done its reset
print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])	# Gives a battery-status
drone.useDemoMode(True)                                    # Just give me 15 basic dataset per second (is default anyway)
drone.getNDpackage(["demo"])                               # Packets, which shall be decoded
time.sleep(0.5)                                            # Give it some time to awake fully after reset

##### Mainprogram begin #####
NDC =   drone.NavDataCount
state = 0
end =   False
while not end:
    while drone.NavDataCount == NDC:   time.sleep(0.001)   # Wait for the next NavData
    if drone.getKey():
        state+=1
        if state == 1:	drone.addNDpackage(["demo"])       # Add "demo" to the list of packages
        if state == 2:	drone.getNDpackage(["all"])        # Get exact following packages
        if state == 3:	drone.delNDpackage(["all"])        # Delete "all" from list of packages
        if state == 3:	drone.useDemoMode(False)           # switch to full-mode, NOTE: swtich may delay
        if state == 4:	drone.addNDpackage(["demo"])
        if state == 5:	drone.getNDpackage(["all"])
        if state > 5:	sys.exit()

    print "------------------"
    if state == 0: print "##### Demo Mode: On   , NavData-Packages: None"
    if state == 1: print "##### Demo Mode: On   , NavData-Packages: Demo"
    if state == 2: print "##### Demo Mode: On   , NavData-Packages: All"
    if state == 3: print "##### Demo Mode: Off  , NavData-Packages: None"
    if state == 4: print "##### Demo Mode: Off  , NavData-Packages: Demo"
    if state == 5: print "##### Demo Mode: Off  , NavData-Packages: All"

    if drone.NavDataCount-NDC>1:    print "Lost "+str(drone.NavDataCount-NDC-1)+" NavData"
    print "Number of package : "+str(drone.NavDataCount)
    print "Receifetime :       "+str(drone.NavDataTimeStamp)+" , \t"+str(time.time()-drone.NavDataTimeStamp)+" sec ago"
    print "Time to decode :    "+str(drone.NavDataDecodingTime)
    print "Included packages : "+str(drone.NavData.keys())
    print "State-data :        "+str(drone.State)
    try:       print "Demo-data :         "+str(drone.NavData["demo"])
    except:    pass
    NDC = drone.NavDataCount
