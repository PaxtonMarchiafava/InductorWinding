# This world would be at better place if we just used cross sectional area instead of gauge

from pylogix import PLC
import Common
from Common import log, GetPLCVal

import math
import time
import os

μ = 4 * math.pi * pow(10, -7) # air: 4π × 10−7 H/m
maxCoilThickness = 40; # number of diameters thick each side of the coil is


class Inductor:
  def __init__(self, Inductance, Diameter, Current): # mH, mm, mA
    self.Inductance = (Inductance * pow(10, -3)) # mH ->Henries
    self.Turns = 0
    self.Mass = 0 # kg
    self.Diameter = (Diameter * pow(10, -3)) # mm -> m
    self.Turns_X = 1
    self.Turns_Z = 1
    self.Current = (Current * pow(10, -3)) # mA -> A
    self.wireDia = 0.001 # m

    if (self.Current > (15 * 0.5)): # these nums are wrong
      self.wireDia = 0.001628 # m
      self.gauge = 14
    elif (self.Current > (5 * 0.5)):
      self.wireDia = 0.00129 # m
      self.gauge = 16
    elif (self.Current > (1 * 0.5)):
      self.wireDia = 0.00102 # m
      self.gauge = 18
    
    self.length = 0 # m
    self.wireLength = 0
  
  def printCoil(self):
    print("Inductance: " + str(self.Inductance))
    print("Turns: " + str(self.Turns))
    print("Mass: " + str(self.Mass))
    print("Diameter: " + str(self.Diameter))
    print("Turns_X: " + str(self.Turns_X))
    print("Turns_Z: " + str(self.Turns_Z))
    print("Current: " + str(self.Current))
    print("WireDia: " + str(self.wireDia))
    print("Length: " + str(self.length))
    print("wireLength: " + str(self.wireLength))
    print("Gauge: " + str(self.gauge))

def calculateInductor(inductor):

  while (getInductance(inductor) < inductor.Inductance):

    if (inductor.Turns_X < maxCoilThickness): # get larger until max x has been reached
      inductor.Turns_X += 1
    inductor.Turns_Z += 1
    
    inductor.length = inductor.Turns_Z * inductor.wireDia
  inductor.Inductance = getInductance(inductor)

  inductor.Turns = inductor.Turns_X * inductor.Turns_Z

  inductor.wireLength = (((2 * math.pi * ((inductor.Diameter + ((inductor.wireDia * inductor.Turns_X) / 2)) / 2)) * inductor.Turns) + (inductor.length * 2)) # circumference: 2 pi r

  volume = inductor.length * areaOfCircle(inductor.wireDia / 2) # m^3
  inductor.Mass = volume * (8.96 * pow(100, 3) * 0.001)# 8.96 g/cm3, 100^3 cm^3 / m^3
  
  return inductor

def getInductance (inductor):
  return ((pow((inductor.Turns_X * inductor.Turns_Z), 2) * μ * (areaOfCircle((inductor.Diameter / 2) + ((inductor.wireDia * inductor.Turns_X) / 2)) )) / (inductor.wireDia * inductor.Turns_Z))
 
def areaOfCircle (radius):
  return math.pi * pow(radius, 2)

def SendPLCVal(plc, tag, value): # sends value to tag on PLC
  while (True):
    ret = plc.Write(tag, value)
    if ret.Status != 'Success': # "Path segment error" if tag not found
      print('Failed to send tag: ' + tag + ' ' + ret.Status)
      log('Failed to send tag:\t\t' + tag + ' ' + ret.Status)
    elif ret.Status == 'Success':
      break
    time.sleep(Common.RetryTime)

def WaitForVal(plc, tag, value): # wait for tag to equal val
  while (True):
    ret = GetPLCVal(plc, tag) # wait for PLC to be ready
    if ret == value:
      break
    time.sleep(Common.RetryTime)

def GetOrderFile(): # returns path to oldest PendingOrder file

  PendingOrders = os.listdir(Common.path + 'PendingOrders/') # list of all pending orders

  if not PendingOrders: # if no pending orders, return None
    return None

  old = os.path.getmtime(Common.path + 'PendingOrders/' + PendingOrders[0])
  oldestFile = PendingOrders[0]

  for file in PendingOrders:
    if os.path.getmtime(Common.path + 'PendingOrders/' + file) < old:
      old = os.path.getmtime(Common.path + 'PendingOrders/' + file)
      oldestFile = file


  return Common.path + 'PendingOrders/' + oldestFile

def SendInductor (plc, inductor): # waits for ready, sends inductor values to PLC, waits for done

  WaitForVal(plc, Common.ReadyTag, True)
  
  SendPLCVal(plc, Common.inductance, inductor.Inductance)
  SendPLCVal(plc, Common.turns, inductor.Turns)
  SendPLCVal(plc, Common.mass, inductor.Mass)
  SendPLCVal(plc, Common.Diameter, inductor.Diameter)
  SendPLCVal(plc, Common.Turns_X, inductor.Turns_X)
  SendPLCVal(plc, Common.Turns_Z, inductor.Turns_Z)
  SendPLCVal(plc, Common.current, inductor.Current)
  SendPLCVal(plc, Common.length, inductor.length)

  SendPLCVal(plc, Common.CommsDoneTag, True)
  CoilStartTime = CTRL.GetPLCTime(True)

  log('Sent Inductor:\t\t\t\t' + str(inductor.Inductance) + ' mH, ' + str(inductor.Diameter) + ' mm, ' + str(inductor.Current) + ' mA')
  WaitForVal(CTRL, Common.DoneTag, True)
  log('Coil wind time:\t\t\t\t' + str((CTRL.GetPLCTime(True) - CoilStartTime) * 0.001) + ' ms') # log cycle time

  SendPLCVal(plc, Common.CommsDoneTag, False) # reset value for later


with PLC() as CTRL:
  CTRL.IPAddress = Common.ipAddress
  orderPath = GetOrderFile()

  while orderPath is None: # wait for order file
    print('Waiting for order file...')
    time.sleep(2)
    orderPath = GetOrderFile()

  with open(orderPath, 'r') as OrderFile:
    log('Opened file:\t\t\t\t\t' + orderPath)
    header = next(OrderFile)  # Skip the header line
    print(header.strip())
    for line in OrderFile:
      print(line)
      Inductance, Diameter, Current = line.strip().split(',') # get values from line
      inductor = Inductor(float(Inductance), float(Diameter), float(Current))
      log('Read Inductor:\t\t\t\t' + str(inductor.Inductance) + ' mH, ' + str(inductor.Diameter) + ' mm, ' + str(inductor.Current) + ' mA')

      inductor = calculateInductor(inductor)
      inductor.printCoil()


      SendInductor(CTRL, inductor)

  OrderFile.close()
  log('Closed file:\t\t\t\t\t' + orderPath)
  os.rename(Common.path + 'PendingOrders/' + orderPath, Common.path + 'CompleteOrders/' + orderPath) # move file to CompleteOrders
  log('Moved file:\t\t\t\t\t' + orderPath)

