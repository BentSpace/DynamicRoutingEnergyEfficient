# Dynamic routing mechanism design wih focus on energy conservation
# By: Nathan Bertam

# Main Idea: Want to keep sensors alive as long as possible.  Since each message
# sent decreases the amount of power left in a node by 1 unit, it should send as few unnessary
# messages as possible.  Will be using the distance vector alogrithm since
# the amount of power left in each sensor is constantly changing with every message
# sent and the link costs will be based on the inverse amount of power left in 
# each node.  So each message sent from a sensor to the gateway will attempt to 
# take the least cost path, based on the sensors distance vector estimate of the
# least cost path.  The total cost of a path is equal to: 
# (1 / powerRemainingNode + 1 / powerRemainingNode + ...(for each node in path))

# each node is a sensor.  gw is the gateway where the sensors need to send their data
sensorGraph = {
    "a" : ["b", "c"],
    "b" : ["a", "c", "e", "j", "i"],
    "c" : ["a", "b", "d", "f", "g", "i"],
    "d" : ["e", "gw", "h", "g", "c", "i"],
    "e" : ["gw", "d", "i", "b", "j"],
    "f" : ["c", "g"],
    "g" : ["d", "h", "f", "c"],
    "h" : ["gw", "g", "d"],
    "i" : ["e", "d", "c", "b"],
    "j" : ["e", "b"]
}

sensorGraphSimple = {
    "a" : ["b", "c"],
    "b" : ["a", "gw"],
    "c" : ["a", "gw"]
}

# the actual power remaining in each sensor node
actualPowerRemaining = {
    "a" : 100,
    "b" : 100,
    "c" : 100
    # "d" : 100,
    # "e" : 100,
    # "f" : 100,
    # "g" : 100,
    # "h" : 100,
    # "i" : 100,
}

# the distance vector maintained by each node, which is their estimate of the 
# cost to reach every other node. The first level is the node the table belongs
# to.  The second level is the "from" node.  The bottom level keys are the "to"
# nodes.
nodeTables = {
    "a" : {
        "a" :  {
            "a" : 0,
            "b" : 1/100,
            "c" : 1/100,
            "gw" : 10000
        },
        "b" : {
            "a" : 10000,
            "b" : 10000,
            "c" : 10000,
            "gw" : 10000
        },
        "c" : {
           "a" : 10000,
            "b" : 10000,
            "c" : 10000,
            "gw" : 10000
        }
    },
    "b" : {
        "a" :  {
           "a" : 10000,
            "b" : 10000,
            "c" : 10000,
            "gw" : 10000
        },
        "b" : {
            "a" : 1/100,
            "b" : 0,
            "c" : 10000,
            "gw" : 1/100
        },
        "c" : {
           "a" : 10000,
            "b" : 10000,
            "c" : 10000,
            "gw" : 10000
        }
    },
    "c" : 
    {
        "a" :  {
           "a" : 10000,
            "b" : 10000,
            "c" : 10000,
            "gw" : 10000
        },
        "b" : {
           "a" : 10000,
            "b" : 10000,
            "c" : 10000,
            "gw" : 10000
        },
        "c" : {
            "a" : 1/100,
            "b" : 10000,
            "c" : 0,
            "gw" : 1/100
        }
    },
}

# cost of the link from node x to node y.
def c(x,y):
    if y in sensorGraphSimple[x]:
        return 1 / actualPowerRemaining[y]
    else:
        return 10000

time = 0
print(c("a","gw"))





# No time for OOP...
# class sensorNode:
#     def __init__(self, name) -> None:
#         self.name = name
#         self.powerRemaining = 100

# class sensorNetworkSim:
#     def __init__(self) -> None:
#         self.initSensorNodes()
#         print(1)
#         print(a)

#     def initSensorNodes(self):
#         sensorNames = ["a","b","c","d","e","f","g","h","i","j","gw"]
#         for sensor in sensorNames:
#             sensor = sensorNode(sensor)
#             print(sensor.name)
#     print(2)
# if __name__ == '__main__':
#     sensorNetworkSim()
   