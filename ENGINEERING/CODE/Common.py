
# file with functions and variables that are used in the other files

import time

# ipAddress = '192.168.1.146' # test plc ip
ipAddress = '192.168.1.200' # plc ip
RetryTime = 1 # time to wait before retrying PLC read/write in seconds. Not the communication timeout

# path that contains PendingOrders and CompleteOrders folders
# path = 'C:/Users/paxto/OneDrive/Desktop/LocalProjects/InductorWinding/ENGINEERING/CODE/'
path = 'C:/Users/Inductor Winding/Desktop/'

 # Tag names in PLC
localBase = 'Program:MainProgram.' # tag to specify tag local to MainProgram
ReadyTag = localBase + 'Ready'
DoneTag = localBase + 'Done'

inductance = 'Coil.Inductance'
maxDia = 'Coil.MaxDia'
current = 'Coil.Current'

CommsDoneTag = 'InductorSent' # this code sets this true when it is done sending data


def log (Message): # Write to log file

  with open(path + 'log.txt', "a") as f:
    f.write(Message + "\n")
  f.close()


def GetPLCVal(plc, tag): # read until value
  while (True):
    ret = plc.Read(tag)
    if ret.Status != 'Success':
      print('Failed to read tag: ' + tag + ' ' + ret.Status)
      log('Failed to read tag:\t\t' + tag + ' ' + ret.Status)
    elif ret.Status == 'Success':
      return ret.Value
    time.sleep(RetryTime)