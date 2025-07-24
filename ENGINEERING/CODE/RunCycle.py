from pylogix import PLC
import Common
from Common import log, GetPLCVal

import time
import os


class Inductor:
  def __init__(self, Inductance, MaxDia, Current): # mH, mm, mA
    self.Inductance = Inductance
    self.MaxDia = MaxDia
    self.Current = Current

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

  old = os.path.getmtime(Common.path + 'PendingOrders/' + PendingOrders[0])
  oldestFile = PendingOrders[0]

  for file in PendingOrders:
    if os.path.getmtime(Common.path + 'PendingOrders/' + file) < old:
      old = os.path.getmtime(Common.path + 'PendingOrders/' + file)
      oldestFile = file


  return Common.path + 'PendingOrders/' + oldestFile

def SendInductor (plc, inductor): # waits for ready, sends inductor values to PLC, waits for done

  WaitForVal(plc, Common.ReadyTag, True)
  
  SendPLCVal(plc, 'Coil.Inductance', inductor.Inductance)
  SendPLCVal(plc, 'MaxDia', inductor.MaxDia)
  SendPLCVal(plc, 'Current', inductor.Current)

  SendPLCVal(plc, Common.CommsDoneTag, True)
  CoilStartTime = CTRL.GetPLCTime(True)

  log('Sent Inductor:\t\t\t\t' + str(inductor.Inductance) + ' mH, ' + str(inductor.MaxDia) + ' mm, ' + str(inductor.Current) + ' mA')
  WaitForVal(CTRL, Common.DoneTag, True)
  log('Coil wind time:\t\t\t\t' + str((CTRL.GetPLCTime(True) - CoilStartTime) * 0.001) + ' ms') # log cycle time

  SendPLCVal(plc, Common.CommsDoneTag, False) # reset value for later



with PLC() as CTRL:
  CTRL.IPAddress = Common.ipAddress
  orderPath = GetOrderFile()
  with open(orderPath, 'r') as OrderFile:
    log('Opened file:\t\t\t\t\t' + orderPath)
    header = next(OrderFile)  # Skip the header line
    print(header.strip())
    for line in OrderFile:
      print(line)
      Inductance, MaxDia, Current = line.strip().split(',') # get values from line
      inductor = Inductor(int(Inductance), int(MaxDia), int(Current))
      log('Read Inductor:\t\t\t\t' + str(inductor.Inductance) + ' mH, ' + str(inductor.MaxDia) + ' mm, ' + str(inductor.Current) + ' mA')

      SendInductor(CTRL, inductor)

  OrderFile.close()
  log('Closed file:\t\t\t\t\t' + orderPath)
  os.rename(Common.path + 'PendingOrders/' + orderPath, Common.path + 'CompleteOrders/' + orderPath) # move file to CompleteOrders
  log('Moved file:\t\t\t\t\t' + orderPath)

