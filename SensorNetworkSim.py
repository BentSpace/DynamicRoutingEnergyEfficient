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
# from IPython.display import display, HTML
import pandas as pd

# each node is a sensor.  gw is the gateway where the sensors need to send their data
# sensorGraph = {
#     "a" : ["b", "c"],
#     "b" : ["a", "c", "e", "j", "i"],
#     "c" : ["a", "b", "d", "f", "g", "i"],
#     "d" : ["e", "gw", "h", "g", "c", "i"],
#     "e" : ["gw", "d", "i", "b", "j"],
#     "f" : ["c", "g"],
#     "g" : ["d", "h", "f", "c"],
#     "h" : ["gw", "g", "d"],
#     "i" : ["e", "d", "c", "b"],
#     "j" : ["e", "b"]
# }



# # the actual power remaining in each sensor node
# actualPowerRemaining = {
#     "a" : 100,
#     "b" : 100,
#     "c" : 100,
#     "gw" : 100
#     # "d" : 100,
#     # "e" : 100,
#     # "f" : 100,
#     # "g" : 100,
#     # "h" : 100,
#     # "i" : 100,
# }


# the distance vector maintained by each node, which is their estimate of the 
# cost to reach every other node. The first level is the node the table belongs
# to.  The second level is the "from" node, for each of the node's nieghboors.
# The value in the key is the estimate distance from v to the gateway.  To save
# memory and energy, only need to compute distance to gateway, since that is the
# only destination.
# # the distance vector maintained by each node, which is their estimate of the 
# # cost to reach every other node. The first level is the node the table belongs
# # to.  The second level is the "from" node.  The bottom level keys are the "to"
# # nodes.
# nodeTables = {}
#     "a" : {
#         "a" :  {
#             "a" : 0,
#             "b" : 1/100,
#             "c" : 1/100,
#             "gw" : 10000
#         },
#         "b" : {
#             "a" : 10000,
#             "b" : 10000,
#             "c" : 10000,
#             "gw" : 10000
#         },
#         "c" : {
#            "a" : 10000,
#             "b" : 10000,
#             "c" : 10000,
#             "gw" : 10000
#         }
#     },
#     "b" : {
#         "a" :  {
#            "a" : 10000,
#             "b" : 10000,
#             "c" : 10000,
#             "gw" : 10000
#         },
#         "b" : {
#             "a" : 1/100,
#             "b" : 0,
#             "c" : 10000,
#             "gw" : 1/100
#         },
#         "c" : {
#            "a" : 10000,
#             "b" : 10000,
#             "c" : 10000,
#             "gw" : 10000
#         }
#     },
#     "c" : 
#     {
#         "a" :  {
#            "a" : 10000,
#             "b" : 10000,
#             "c" : 10000,
#             "gw" : 10000
#         },
#         "b" : {
#            "a" : 10000,
#             "b" : 10000,
#             "c" : 10000,
#             "gw" : 10000
#         },
#         "c" : {
#             "a" : 1/100,
#             "b" : 10000,
#             "c" : 0,
#             "gw" : 1/100
#         }
#     },
# }


# # Cost of the link from node x to node v.
# def c(x,v):
#     if x == v:
#         return 0
#     elif v in sensorGraphSimple[x]:
#         return 1 / actualPowerRemaining[v]
#     else:
#         return 10000

# # Distance vector update algorithm. Estimated cost from node x to y.
# def D(x,y):
#     if x == y:
#         return 0
#     else:
#         mini = 10000
#         # for each neighbor v of x
#         for v in sensorGraphSimple[x]:
#             result = c(x,v) + D(v,y) 
#             if result < mini:
#                 mini = result
#         return mini

# # initializes the forwarding tables for a sensor node x
# def initialization(x):
#     # create and add x's DV to it's table
#     distanceVector = {}
#     # create empty dict to hold x's forward table
#     nodeTables[x] = {}
#     for y in N:
#         distanceVector[y] = c(x,y)
#     global NodeTables
#     nodeTables[x][x] = distanceVector

#     # set distance vectors of x's neighbors (w) to infinity and add to x's table
#     for w in sensorGraphSimple[x]:
#         distanceVector = {}
#         for y in N:
#             distanceVector[y] = 10000
#         nodeTables[x][w] = distanceVector


# for x in N:
#     initialization(x)
# time = 0
# # print(c("a","gw"))
# D("a","gw")

# An individual sensor node in the network
class sensorNode:
    sensorGraphSimple = {
    "a" : ["b", "c"],
    "b" : ["a", "gw"],
    "c" : ["a", "gw"],
    "gw": ["b", "c"]
    }
    N = list(sensorGraphSimple.keys()) # list of Nodes in network
    def __init__(self, name) -> None:
        self.name = name
        self.powerRemaining = 100
        # The rows in the forwarding table are the distance vectors of itself 
        # and it's neighbooring nodes.  
        # The columns contain the estimated cost to reach that node in the column
        # label, from the node in the row label
        dfIndex = list(self.sensorGraphSimple[self.name])
        dfIndex.insert(0, self.name)
        self.forwardingTable = pd.DataFrame(index=dfIndex, columns=self.N)
        # self.forwardingTable.columns = self.N
        self.neighborsPowerRemaining = {}
        for v in self.sensorGraphSimple[self.name]:
            self.neighborsPowerRemaining[v] = 100
        print(self.neighborsPowerRemaining)
        self.forwardingTable = self.forwardingTable.fillna(10000)
        # construct own DV, to start need assume nodes fully charged
        for v in self.sensorGraphSimple[self.name]:
            self.forwardingTable.at[self.name, v] = 1/100
        self.forwardingTable = self.forwardingTable.fillna(10000)
        print(self.forwardingTable)



     
    # Cost of the link from node x to node v.
    def c(self,x,v):
        if x == v:
            return 0
        elif v in self.neighborsPowerRemaining[v]:
            return 1 / self.neighborsPowerRemaining[v]
        else:
            return 10000

    # Sends own DV to v
    # def sendDV(self, v)

class sensorNetworkSim:
    def __init__(self) -> None:
        self.initSensorNodes()
  

    def initSensorNodes(self):
        sensorNames = ["a","b","c","gw"]
        for sensor in sensorNames:
            sensor = sensorNode(sensor)
            # print(sensor.name)
    
if __name__ == '__main__':
    sensorNetworkSim()
   

# # the distance vector maintained by each node, which is their estimate of the 
# # cost to reach every other node. The first level is the node the table belongs
# # to.  The second level is the "from" node.  The bottom level keys are the "to"
# # nodes.
# nodeTables = {
#     "a" : {
#         "a" :  {
#             "a" : 0,
#             "b" : 1/100,
#             "c" : 1/100,
#             "gw" : 10000
#         },
#         "b" : {
#             "a" : 10000,
#             "b" : 10000,
#             "c" : 10000,
#             "gw" : 10000
#         },
#         "c" : {
#            "a" : 10000,
#             "b" : 10000,
#             "c" : 10000,
#             "gw" : 10000
#         }
#     },
#     "b" : {
#         "a" :  {
#            "a" : 10000,
#             "b" : 10000,
#             "c" : 10000,
#             "gw" : 10000
#         },
#         "b" : {
#             "a" : 1/100,
#             "b" : 0,
#             "c" : 10000,
#             "gw" : 1/100
#         },
#         "c" : {
#            "a" : 10000,
#             "b" : 10000,
#             "c" : 10000,
#             "gw" : 10000
#         }
#     },
#     "c" : 
#     {
#         "a" :  {
#            "a" : 10000,
#             "b" : 10000,
#             "c" : 10000,
#             "gw" : 10000
#         },
#         "b" : {
#            "a" : 10000,
#             "b" : 10000,
#             "c" : 10000,
#             "gw" : 10000
#         },
#         "c" : {
#             "a" : 1/100,
#             "b" : 10000,
#             "c" : 0,
#             "gw" : 1/100
#         }
#     },
# }
