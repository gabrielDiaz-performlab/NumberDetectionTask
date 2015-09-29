
import viz
import vizact
import numpy as np
wii = viz.add('wiimote.dle')#Add wiimote extension

sendNetCommands = True

receiver  = False

if( sendNetCommands ):
	receiver = viz.addNetwork('performLabVR2'.upper())
	receiver.port(5000) # Send data over port 5000

# dummy
def appendTrialToEndOfBlock():
	return

class wiiObj():
	def __init__(self):
	
		self.wiimote = wii.addWiimote()# Connect to first available wiimote
		vizact.onexit(self.wiimote.remove) # Make sure it is disconnected on quit

		self.wiimote.led = wii.LED_1 | wii.LED_4 #Turn on leds to show connection

class numberCount(viz.EventClass):
	def __init__(self):
			

		self.targetNumber = 0
		self.maxNum = 3
		
		self.buffSize  = 10
		self.updateRateSecs = 1
		
		self.nextBuffer  = np.array([])
		self.lastBuffer = []
		
		while(self.nextBuffer.size < self.buffSize):
			self.addInt()
		
		self.textObj = viz.addText('',parent=viz.SCREEN)
		self.textObj.setPosition(0.5,0.5)
		self.textObj.color(viz.WHITE)
		self.textObj.alignment( viz.ALIGN_CENTER_CENTER) 
		self.textObj.fontSize(1000)
		
		self.updateAction  = vizact.ontimer(self.updateRateSecs,self.presentNumber)
		self.updateAction.setEnabled(viz.disable)
		
		self.targetTimer = []
		
	def addInt(self):
		''' Add a number to the right of the self.numberbuffer '''
		
		if( self.nextBuffer.size == 0):
			self.nextBuffer = np.array([np.random.randint(low=0,high=self.maxNum)])
		else:
			randInt = np.random.randint(low=0,high=self.maxNum)

			# Ensure it is a unique int
			while( randInt  == self.nextBuffer[0]):
				randInt = np.random.randint(low=0,high=self.maxNum)

			self.nextBuffer = np.insert(self.nextBuffer,0,randInt)
			
	def presentNumber(self):
		
		# Show the number on the right of nextBuffer
		self.textObj.message( str(self.nextBuffer[-1]))
		
		# Append number to the right of last buffer
		self.lastBuffer = np.append(self.lastBuffer,self.nextBuffer[-1])
		# Delete the left on the last buffer
		self.lastBuffer = np.delete(self.lastBuffer,0)		
		
		# Delete the number on the right of nextBuffer
		self.nextBuffer = np.delete(self.nextBuffer,-1)
		
		# Add a rand int to the left of nextBuffer
		self.addInt()
		
		print self.nextBuffer
		
		if ( self.textObj.getMessage() == str(self.targetNumber) ):
			self.startTargetTimer()
		
	def startCountDown(self):
		
		if(self.updateAction):
			self.updateAction.setEnabled(viz.enable)
			
	def stopCountDown(self):
		
		if(self.updateAction):
			self.updateAction.setEnabled(viz.disable)

	def mistakeMade(self):
		
		print 'MISSED IT'
		import winsound
		Freq = 500 # Set Frequency To 2500 Hertz
		Dur = 100 # Set Duration To 1000 ms == 1 second
		winsound.Beep(Freq,Dur)
		
		if(sendNetCommands):
			receiver.send(action = appendTrialToEndOfBlock) # Passed through the e object as e.message
		
	def startTargetTimer(self):
		self.targetTimer = vizact.ontimer2(self.updateRateSecs+0.2,0,self.mistakeMade)
	
	def stopTargetTimer(self):
		print 'Stopped timer'
		self.targetTimer.remove()
		self.targetTimer = False
		
	def targetDetected(self):
		
		# Correct detection
		if ( self.textObj.getMessage() == str(self.targetNumber) ):
			
			print 'GOT IT'
			self.stopTargetTimer()
			import winsound
			Freq = 200 # Set Frequency To 2500 Hertz
			Dur = 50 # Set Duration To 1000 ms == 1 second
			winsound.Beep(Freq,Dur)
			
		else:
			print 'BAD RESPONSE'
			self.mistakeMade()
			
viz.go(viz.FULLSCREEN)

counter = numberCount()
#counter.startCountDown()

import vizact

wii1 = wiiObj()
vizact.onsensordown(wii1.wiimote,wii.BUTTON_B,counter.targetDetected)		

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

####################################
## Setup receiver
#
#def onNetwork(e):
#	
#	print 'Got it.'
#	sender = 'performVR'.upper()
#	
#	print sender
#	if e.sender.upper() == sender:
#		e.action(e)
#		
#
#def printMessage(e):
#	print 'Message is: ' + e.message
#
## Receive data over port 5000
#viz.net.addPort(5000)
#	
#viz.callback(viz.NETWORK_EVENT, onNetwork)
#


