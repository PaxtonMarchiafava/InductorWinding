import pylogix
import Common
from Common import log, GetPLCVal

from struct import unpack_from
import time

with pylogix.PLC(Common.ipAddress) as comm:

  while (True):
    # print(GetPLCVal(comm, 'bwsig'))

    ret = comm.Message(cip_service=0x01, cip_class=0x73, cip_instance=0x01)

    if ret.Status == "Success":

      data = ret.Value[44:]
      major = unpack_from("<H", data, 20)[0]
      minor = unpack_from("<H", data, 22)[0]

      print('Fault Log Major: ' + str(major) + ' Minor: ' + str(minor))
      # log('Fault Log Major: ' + str(major) + ' Minor: ' + str(minor))
    
    time.sleep(Common.RetryTime)


