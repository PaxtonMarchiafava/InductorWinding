
 # jus a file to test stuff

import os 


path = 'C:/Users/paxto/OneDrive/Desktop/LocalProjects/InductorWinding/ENGINEERING/CODE/' # path that contains PendingOrders and CompleteOrders folders



def GetOrderFile(): # returns path to oldest PendingOrder file

  PendingOrders = os.listdir(path + 'PendingOrders/') # list of all pending orders

  old = os.path.getmtime(path + 'PendingOrders/' + PendingOrders[0])
  oldestFile = PendingOrders[0]

  for file in PendingOrders:
    if os.path.getmtime(path + 'PendingOrders/' + file) < old:
      old = os.path.getmtime(path + 'PendingOrders/' + file)
      oldestFile = file


  return path + 'PendingOrders/' + oldestFile


print(GetOrderFile()) # test the function