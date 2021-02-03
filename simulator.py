import serial
import convertRaDecToCgemUnits
import time

# Another neat idea would be to have this script spawn the virtual
# serial port
# Since simulator only runs while we are simulating (duh) it could
# runs
# nullmodem.sh before attempting to establish the serial interface.

serialPort = './pty2'
ser = serial.Serial(port=serialPort,timeout=1)

class Simulator:

  def __init__ (self):
    self.raConversion  = convertRaDecToCgemUnits.ConvertRa()
    self.decConversion = convertRaDecToCgemUnits.ConvertDec()

  def parse_command(self, prefix):
    if prefix == b'e':
      # Get precise RA/Dec command
      # will hardware outputCommand
      #outputCommand = self.telecopeRaCgem + ',' + self.telescopeDecCgem + '#'
      #ser.write (outputCommand)
      ser.write(b'34AB0500,12CE0500#')
    elif prefix == b'E':
      # Get RA/Dec command
      ser.write(b'34AB,12CE#')
    elif prefix == b'h':
      # Get time command
      localtime = time.localtime(time.time())
      
      response = \
        chr(localtime.tm_hour)      + \
        chr(localtime.tm_min)       + \
        chr(localtime.tm_sec)       + \
        chr(localtime.tm_mon)       + \
        chr(localtime.tm_mday)      + \
        chr(localtime.tm_year-2000) + \
        chr(256-8)                  + \
        chr(localtime.tm_isdst)     + \
        '#'
      ser.write(response.encode('utf-8'))
    elif prefix == b'J':
      # Alignment complete command.
      # response with alignment complete response
      ser.write(b'x#')
    elif prefix == b'K':
      # Echo command
      argument = ser.read(1)
      # print ('ser.write with argument: ', argument)
      response = argument + b'#'
      # print ('argument : ', argument)
      ser.write (response)
    elif prefix == b'L':
      # Goto in progress command
      response = '0#'
      ser.write (response.encode('utf-8'))
    elif prefix == b'r':
      # Goto precise RA/Dec command
      commandText = ser.read(20)
      print ("Read command parameters: '{0}'".format(commandText))

      if False: # need to debug
        # Split up the two arguments which are separated by a ','.
      
        # args = commandText.split(',', 2)
        raHex = commandText[1:8]
        decHex = commandText[10:17]
        
        print ('simulator raHex  : ', raHex)
        print ('simulator decHex : ', decHex)
        
        # The two variables testscopeRa and telescopeDec will be used
        # to simulate the current position of the telescope
      
        self.telescopeRa = self.raConversion.fromCgem(raHex)
      
        self.telecopeRaCgem = (
          convertRaDecToCgemUnits.Ra(float(self.telescopeRa[0]),
                                     float(self.telescopeRa[1]),
                                     float(self.telescopeRa[2]))).toCgem()
                                     
        print ('self.telescopeRaCgem : ', self.telecopeRaCgem)
      
        # If the declination is outside of the range -90 to +90 then
        # it needs to be converted back. The telescopeDec variable
        # needs to be corrected before calling the toCgem method.
      
        self.telescopeDec = self.decConversion.fromCgem(decHex)
      
        self.telescopeDecGem = (convertRaDecToCgemUnits.Dec
                                (float(self.telescopeDec[0]),
                                 float(self.telescopeDec[1]),
                                 float(self.telescopeDec[2]))).toCgem()

      try:
        ser.write(b'#')
      except:
        print ('r command failed')
    elif prefix == b't':
      # Tracking mode command
      response = chr(2)+'#'
      ser.write(response.encode('utf-8'))
    elif prefix == b'w':
      # Get location command
      response = chr(34)+chr(0)+chr(0)+chr(0)+chr(119)+chr(0)+chr(0)+chr(1)+'#'
      try:
        ser.write(response.encode('utf-8'))
      except:
        print ('ser.write(response) failed, response : ', response)
    else:
      if prefix != b'':
        print ('In simulator.py unhandled case, prefix: ', prefix)

    # This else clause was resulting in too much output traffic.
    # For now I'll comment it out.
    #else:
    #    print ('Unknown command')

if __name__ == '__main__':
  
  done = False
  sim = Simulator()

  while not done:
    if ser.isOpen() == False:
      done = True
    else:
      cmd = ser.read(1)
      if cmd != '':
        sim.parse_command(cmd)
        if cmd == 'q':
          done = True

