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
import time
import random
import sys
sys.setrecursionlimit(20000)

# An individual sensor node in the network
class sensorNode:
    # sensorGraph = {
    # "a" : ["b", "c"],
    # "b" : ["a", "gw"],
    # "c" : ["a", "gw"],
    # "gw": ["b", "c"]
    # }
    # each node is a sensor.  gw is the gateway where the sensors need to send their data
    sensorGraph = {
        "a" : ["b", "c"],
        "b" : ["a", "c", "e", "j", "i"],
        "c" : ["a", "b", "d", "f", "g", "i"],
        "d" : ["c", "e", "g", "h", "i", "gw"],
        "e" : ["b", "d", "i",  "j", "gw"],
        "f" : ["c", "g"],
        "g" : [ "c", "d", "f", "h"],
        "h" : ["d", "g", "gw"],
        "i" : ["b", "c", "d", "e"],
        "j" : ["b", "e"],
        "gw": ["d", "e", "h"]
    }
    N = list(sensorGraph.keys()) # list of Nodes in network
    def __init__(self, name) -> None:
        self.name = name
        self.powerRemaining = 100
        self.timeTillPowerDec = 1000
        self.vStarGW = None # The next hop on the least cost path to the gateway
        # The rows in the routing table are the distance vectors of itself 
        # and it's neighbooring nodes.  
        # The columns contain the estimated cost to reach that node in the column
        # label, from the node in the row label
        dfIndex = list(self.sensorGraph[self.name])
        dfIndex.insert(0, self.name)
        self.routingTable = pd.DataFrame(index=dfIndex, columns=self.N)
        self.neighborsPowerRemaining = {}
        for v in self.sensorGraph[self.name]:
            self.neighborsPowerRemaining[v] = 100
        self.routingTable = self.routingTable.fillna(10000)

        # construct own DV, to start need assume nodes fully charged
        for v in self.sensorGraph[self.name]:
            self.routingTable.at[self.name, v] = 1/100
        self.routingTable = self.routingTable.fillna(10000)

        # set cells with matching index and label to 0
        for x in dfIndex:
            for y in self.N:
                if x == y:
                    self.routingTable.at[x,y] = 0
     
    # Cost of the link from node x to node v.
    def c(self,x,v):
        if x == v:
            return 0
        elif v in self.neighborsPowerRemaining.keys():
            if self.neighborsPowerRemaining[v] == 0:
                self.nodeDead()
            else:
                return 1.0 / self.neighborsPowerRemaining[v] * 1000.0
        else:
            return 10000

    def sendDVtoNeigboors(self):
        for v in self.sensorGraph[self.name]:
            self.sendDV(v)

    # Sends own DV to v
    def sendDV(self, v):
        ownDV = self.routingTable.iloc[0]
        # print("sendDV", self.name, "->", v)
        self.decrementPower()
        sensorNetworkSim.dictOfSensorObjects[v].receiveDV(self.name, ownDV, self.powerRemaining)

    # For receiveing a DV from node x
    def receiveDV(self, x, DV, powerLevel):
        # if the incoming DV is diferrent
        oldDV = self.routingTable.loc[x]
        self.neighborsPowerRemaining[x] = powerLevel
        if not oldDV.equals(DV):
            self.routingTable.loc[x] = DV
            self.updateOwnDV()
        
    def updateOwnDV(self):
        newDV = []
        for y in self.N:
            result = self.D(self.name, y)
            newDV.append(result)
        oldDV = self.routingTable.loc[self.name]
        if not oldDV.equals(newDV):
            self.routingTable.loc[self.name] = newDV
            # print(self.routingTable.to_string)
            self.sendDVtoNeigboors()

    # Distance vector update algorithm. Estimated cost from node x to y.
    def D(self,x,y):
        if x == y:
            return 0
        else:
            mini = 10000
            vStar = None
            # for each neighbor v of x
            for v in self.sensorGraph[x]:
                result = self.c(x,v) + self.routingTable.at[v,y] 
                if result < mini:
                    mini = result
                    vStar = v
            # if calculating path to gw, update vStarGW
            if y == "gw":
                if x == 'a':
                    pass
                self.vStarGW = vStar
            return mini

    def nodeDead(self):
        sensorNetworkSim.nodeDead = True

    def sendPacket(self):
        packetNum = random.randrange(1, 1000)
        data = random.randrange(1, 100)
        print("sendPacket#: ", packetNum, "data: ", data,  self.name, "->", self.vStarGW)
        self.decrementPower()
        sensorNetworkSim.dictOfSensorObjects[self.vStarGW].receivePacket(packetNum, data)
        
    def receivePacket(self, packetNum, data):
        if self.name != "gw":
            self.relayPacket(packetNum, data)

    def relayPacket(self, packetNum, data):
        print("relayPacket#: ", packetNum, "data: ", data,  self.name, "->", self.vStarGW)
        self.decrementPower()
        sensorNetworkSim.dictOfSensorObjects[self.vStarGW].receivePacket(packetNum, data)
        
    def decrementPower(self):
        if self.name != "gw":
            self.timeTillPowerDec = self.timeTillPowerDec - 1
            if self.timeTillPowerDec == 0:
                self.powerRemaining -= 1
                print("node", self.name, "powerRemaining",self.powerRemaining)
                self.timeTillPowerDec = 100
                if self.powerRemaining == 0:
                    self.nodeDead()
                self.updateOwnDV()
 

class gatewayNode(sensorNode):
    pass

class sensorNetworkSim:
    # sensorGraph = {
    # "a" : ["b", "c"],
    # "b" : ["a", "gw"],
    # "c" : ["a", "gw"],
    # "gw": ["b", "c"]
    # }
    sensorGraph = {
        "a" : ["b", "c"],
        "b" : ["a", "c", "e", "j", "i"],
        "c" : ["a", "b", "d", "f", "g", "i"],
        "d" : ["c", "e", "g", "h", "i", "gw"],
        "e" : ["b", "d", "i",  "j", "gw"],
        "f" : ["c", "g"],
        "g" : ["c", "d", "f", "h"],
        "h" : ["d", "g", "gw"],
        "i" : ["b", "c", "d", "e"],
        "j" : ["b", "e"],
        "gw": ["d", "e", "h"]
    }
    N = list(sensorGraph.keys())
    dictOfSensorObjects = {}
    nodeDead = False

    def __init__(self) -> None:
        self.initSensorNodes()
  
    def initSensorNodes(self):
        
        # initialize sensors
        for sensor in self.N:
            sensorObject = sensorNode(sensor)
            self.dictOfSensorObjects[sensor] = sensorObject
        # send intial DV to neighbors
        for x in self.N:
            for v in self.sensorGraph[x]:
                self.dictOfSensorObjects[x].sendDV(v)
        # update all node's own DV
        for x in self.N:
            self.dictOfSensorObjects[x].updateOwnDV()
        self.runSimulation()

    def runSimulation(self):
        start = time.time()
        packetsSentPerNode = 0
        sendDVsEveryNumPackets = 5
        while not self.nodeDead:
            # sensors send out packets every 1 second
            for sensor in self.dictOfSensorObjects.values():
                if sensor.name != "gw":
                    sensor.sendPacket()
            # packetsSentPerNode += 1
            # if packetsSentPerNode % sendDVsEveryNumPackets == 0:
            #     self.sendDVsOutAllNodes()
            # time.sleep(.1)
        end = time.time()   
        print("Network stayed alive for: ", end - start, "seconds")
    
    def sendDVsOutAllNodes(self):
        for sensor in self.dictOfSensorObjects.values():
            if sensor.name != "gw":
                sensor.sendDVtoNeigboors()

if __name__ == '__main__':
    sensorNetworkSim()