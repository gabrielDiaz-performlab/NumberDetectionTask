
import viz
import vizact
import numpy as np
wii = viz.add('wiimote.dle')#Add wiimote extension


class soundBank():
	def __init__(self):
		 
		################################################################
		################################################################
		
		## Register sounds.  It makes sense to do it once per experiment.
		
		self.buzzer =  '/Resources/BUZZER.wav'
		
		viz.playSound(self.buzzer,viz.SOUND_PRELOAD)

soundBank = soundBank()

class wiiObj():
	def __init__(self):
	
		self.wiimote = wii.addWiimote()# Connect to first available wiimote
		vizact.onexit(self.wiimote.remove) # Make sure it is disconnected on quit

		self.wiimote.led = wii.LED_1 | wii.LED_4 #Turn on leds to show connection

class numberCount(viz.EventClass):
	def __init__(self):
			

		self.targetNumber = 3
		self.maxNum = 7
		
		self.buffSize  = 7
		self.updateRateSecs = 0.75
		
		self.nextBuffer  = np.array([])
		self.lastBuffer = []
		
		while(self.nextBuffer.size < self.buffSize):
			self.addInt()
		
		self.textObj = viz.addText('',parent=viz.SCREEN)
		self.textObj.setPosition(0.5,0.5)
		self.textObj.color(viz.WHITE)
		self.textObj.alignment( viz.ALIGN_CENTER_CENTER) 
		self.textObj.fontSize(1000)
		
		self.targetTimer = []
		self.updateAction  = vizact.ontimer(self.updateRateSecs,self.presentNumber)
		
		self.stopPresentingNumbers()
		
		print 'Ready. To start countdown, run <numberCount>.startPresentingNumbers()' 
		
		
		
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
		
		#print self.nextBuffer
		
		if ( self.textObj.getMessage() == str(self.targetNumber) ):
			self.startTargetTimer()

	def startPresentingNumbers(self):
		
		if(self.updateAction):
			self.updateAction.setEnabled(1)
			
	def stopPresentingNumbers(self):
		
		if(self.updateAction):
			self.updateAction.setEnabled(0)
			self.stopTargetTimer()
			self.textObj.message('')
			
	def failedToDetect(self):
		
		print 'Failed to detect'
		
		viz.clearcolor(viz.RED)
		# Temporarily stop presenting numbers
		self.stopPresentingNumbers()
		vizact.ontimer2(self.updateRateSecs,0,viz.clearcolor,viz.BLACK)
		vizact.ontimer2(self.updateRateSecs,0,self.startPresentingNumbers)
		
		import winsound
		Freq = 200 # Set Frequency To 2500 Hertz
		Dur = 150 # Set Duration To 1000 ms == 1 second

		winsound.Beep(Freq,Dur)
		
		if( networkingOn  ):
			netClient.send(message='numberTaskError')
			
	def falseAlarm(self):
		
		print 'False alarm'
	
		#vizact.ontimer2(self.updateRateSecs,0,viz.clarcolor,viz.RED)
		
		viz.clearcolor(viz.RED)
		# Temporarily stop presenting numbers
		self.stopPresentingNumbers()
		vizact.ontimer2(self.updateRateSecs,0,viz.clearcolor,viz.BLACK)
		vizact.ontimer2(self.updateRateSecs,0,self.startPresentingNumbers)
		
		import winsound
		Freq = 200 # Set Frequency To 2500 Hertz
		Dur = 150 # Set Duration To 1000 ms == 1 second

		winsound.Beep(Freq,Dur)
		
		if( networkingOn  ):
			netClient.send(message='numberTaskError')
		
	def startTargetTimer(self):
		self.targetTimer = vizact.ontimer2(self.updateRateSecs,0,self.failedToDetect)
	
	def stopTargetTimer(self):
		if ( self.targetTimer ):
			print 'Stopped timer'
			self.targetTimer.remove()
			self.targetTimer = False
		
	def targetDetected(self):
		
		# Correct detection
		if ( self.textObj.getMessage() == str(self.targetNumber) ):
			
			print 'GOT IT'
			self.stopTargetTimer()
			import winsound
			Freq = 300 # Set Frequency To 2500 Hertz
			Dur = 50 # Set Duration To 1000 ms == 1 second
			winsound.Beep(Freq,Dur)
			
		else:
			print 'BAD RESPONSE'
			self.falseAlarm()


viz.window.setFullscreenMonitor(2)
viz.go(viz.FULLSCREEN)

counter = numberCount()

import vizact

wii1 = wiiObj()
vizact.onsensordown(wii1.wiimote,wii.BUTTON_B,counter.targetDetected)		

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

networkingOn = True;

if networkingOn :
	netClient = viz.addNetwork('performLabVR2')
else:
	counter.startPresentingNumbers()

def onNetwork(packet):
	
	print 'Received network message: ' + packet.message
	
	if( packet.message == 'start'  ):
		
		counter.startPresentingNumbers()
	
	elif( packet.message == 'stop'  ): 

		counter.stopPresentingNumbers()
		
viz.callback(viz.NETWORK_EVENT, onNetwork)

