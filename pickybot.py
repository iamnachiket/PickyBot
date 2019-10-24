import os
import time
import random
import PIL 
from PIL import Image
import face_recognition





def commandRet(command):
	'''
	Running adb shell Commands on the terminal

	Parameters:
		command: adb commands to be executed

	Returns:
		open('tmp','r').read() as a string that contains output of the adb commnand exectued

	'''
	os.system('{} > tmp'.format(command))
	return open('tmp','r').read()

	
def getDevice():
	'''
	Shows successfully connected devices

	Returns:
		lst1[devno-1]: A string that contains the identification of the device

	'''	

	Devices=commandRet('adb devices')
	dlist1=str(Devices)
	dlist=dlist1.lower()
	lst=dlist.split()
	lst1=[]

	if lst[5] == 'device':
		print('\nDevice No\t\tDevice Identity\n')

		for i in range(4,len(lst),2):
			lst1.append(lst[i])

		for i in range(len(lst1)):
				print('{}\t\t\t{}\n'.format(i+1,lst1[i]))

	else:
		print('Devices not plugged in.')
		time.sleep(5)
		getDevice()

	devno=int(input('Enter Device No:\n'))
	
	return lst1[devno-1]
	
device=getDevice()


def getres(device):
	'''
	This function finds out the resolution of the device.

	Parameters:
		device: Device identification

	Returns:
		reso: A string that contain maximum x and y coordinates

	'''
	
	size=commandRet('adb -s {} shell wm size'.format(device))
	sizel=str(size).split()
	res=sizel[len(sizel)-1]
	reso=res.split('x')
	return reso
	

xmax=float(getres(device)[0])
ymax=float(getres(device)[1])

print(xmax,ymax)



def runningapps(device):
	return commandRet('adb -s {} shell dumpsys activity'.format(device))


def startapp(device,appack):
	'''
	Start an app on the phone

	Parameters:
		device: device identification
		appack: app to be started
	'''

	print(commandRet('adb -s {} shell monkey -p {} -c android.intent.category.LAUNCHER 1'.format(device,appack)))



if 'com.tinder' not in runningapps(device):
	startapp(device,'com.tinder')
	print('Not started. Starting now.')

#if 'com.tinder' in runningapps(device):
startapp(device,'com.tinder')
reason=int(input('\nWould you like to display the reasons too?'))
print('\nRunning.......')

def screenshot(device):
	''' 
	Takes a screenshot and stores it in the directory
	
	Parameters:
		device: device identification

	'''
	os.system("adb -s {} shell screencap -p > img2.png".format(device))

def scrface(device):
	''' 
	Takes a screenshot and stores it in the directory
	
	Parameters:
		device: device identification

	'''
	os.system("adb -s {} shell screencap -p > img3.png".format(device))




def tap(device,xmax,ymax):
	''' 
	Emulates touch on the screen.

	Parameters:
		device: device identification
		xmax: Maximum x-coordinate
		ymax: Maximum y-coordinate

	'''
	x=random.uniform(xmax*0.416,xmax*0.416+10)
	y=random.uniform(ymax*0.781,ymax*0.781+4)
	os.system("adb -s {} shell input touchscreen tap {} {}".format(device,x,y))
	time.sleep(0.4) 


def swipe(device,xmax,ymax):

	''' 
	Emulates swipe on the screen 

	Parameters:
		device: device identification
		xmax: Maximum x-coordinate
		ymax: Maximum y-coordinate

	'''
	#first test
	#x1=random.uniform(400.2,410.4)
	#y1=random.uniform(1030.2,1044.2)
	#x2=random.uniform(350.2,430.4)
	#y2=random.uniform(136.2,144.2)
	#for all
	if int(ymax/xmax) is 2:#for large/bezel less screens
		eq=(1280/ymax)*0.7
	else:
		eq=1280/ymax
	

	x1=random.uniform(0.556*xmax,0.556*xmax+10.4)
	y1=random.uniform(0.804*ymax,0.804*ymax+10.2)
	x2=random.uniform(0.486*xmax,0.486*xmax+80.4)
	y2=random.uniform(0.804*ymax-((0.804-0.106)*ymax*eq),0.804*ymax-((0.804-0.106)*ymax*eq)+8.2)


	tim=random.randrange(400,800)

	os.system("adb -s {} shell input swipe {} {} {} {} {}".format(device,x1,y1,x2,y2,tim))


def crop(device,xmax,ymax):
	''' 
	Crops the image and saves it in the directory

	Parameters:
		device: device identification
		xmax: Maximum x-coordinate
		ymax: Maximum y-coordinate

	'''
	im=Image.open("img2.png")
	crops=im.crop((0.004*xmax,0.101*ymax,0.990*xmax,0.880*ymax))
	crops.save('cropimg2.png',dpi=(300, 300))

def cropf(device,xmax,ymax):
	''' 
	Crops the image and saves it in the directory

	Parameters:
		device: device identification
		xmax: Maximum x-coordinate
		ymax: Maximum y-coordinate

	'''
	im=Image.open("img3.png")
	crops=im.crop((0.005*xmax,0.083*ymax,0.990*xmax,0.741*ymax))
	crops.save('cropimg3.png',dpi=(300, 300))

def ocr(device):
	'''
	Using tesseract, strings are extacted from the cropped screenshots
	
	Parameters:
		device: device identification
	Returns:
		A dictionary that contains biosplit and biosplitsml
		biosplit contains a broader list than biosplitsml
	'''
	bios=commandRet('tesseract cropimg2.png stdout')
	biosplit3=str(bios).lower() 
	biosplit2=biosplit3.strip('!')  
	biosplit1=biosplit2.strip('@')	
	biosplitt=biosplit1				


	biosplitt2=biosplitt.replace('\n','')
	biosplit=biosplitt2.split(' ')#split by space
	biosplitsml=biosplit
	biosplit.extend(biosplit1.split('\n'))#lines
	unw=['', ' ', '\x0c','   ','!',' ! ',' !','|','{','1', '}', '\\', 'k','see what a friend thinks', 'miles', 'away\x0c', 'what', 'a', 'friend', 'thinks\x0c','  ','share','miles away','km','away','km away','kms away']
	

	for i in range(len(unw)):
		biosplitr(biosplit,unw[i])


	return {'biosplit':biosplit,'biosplitsml':biosplitsml}


def biosplitr(bis,ele):
	'''
	Removes elements that are unwanted

	Parameters:
		bis: the bio list
		ele: element to be removed

	'''
	while bis.count(ele)>0:
		bis.remove(ele)
	


def checker(device,filevar,biosplit,xmax,ymax,biosplitsml,reason):

	'''
	This function contains conditions that determine the swipe. It has face recognition and comparisons between various lists.

	Parameters:
		device: String that contains device identification
		filevar: String that contains the file read from words.txt
		biosplit: List that contains the bio
		xmax: The value from the function getres
		ymax: The value from the function getres
		reason: Integer if the reason is to be displayed, 0 for No, 1 for Yes


	Returns:

	'''

	imag=face_recognition.load_image_file('cropimg3.png')
	face_locations=face_recognition.face_locations(imag)

	for j in range(len(biosplit)):
		if (len(biosplitsml)<=15):

			x1=random.uniform(0.436*xmax,0.436*xmax+35)
			y1=random.uniform(0.479*ymax,0.479*ymax+15)
			x2=random.uniform(0.027*xmax,0.027*xmax+40)
			y2=random.uniform(0.543*ymax,0.543*ymax+50)

			tim=random.randrange(400,800)
			
			
			os.system("adb -s {} shell input keyevent 4".format(device))
			os.system("adb -s {} shell input swipe {} {} {} {} {}".format(device,x1,y1,x2,y2,tim))
			if reason==1:
				print('Swiped Left. Reason: Ridiculously short bio/No bio')
			break

		if biosplit[j] in filevar:


			x1=random.uniform(0.436*xmax,0.436*xmax+35)
			y1=random.uniform(0.479*ymax,0.479*ymax+15)
			x2=random.uniform(0.027*xmax,0.027*xmax+40)
			y2=random.uniform(0.543*ymax,0.543*ymax+50)

			tim=random.randrange(400,800)
			

			os.system("adb -s {} shell input keyevent 4".format(device))
			os.system("adb -s {} shell input swipe {} {} {} {} {}".format(device,x1,y1,x2,y2,tim))
			if reason==1:

				print('Swiped Left. Reason: Bio contains a pet peeve')

			break

		if j==(len(biosplit)-1):


			x2=random.uniform(0.436*xmax,0.436*xmax+35)
			y2=random.uniform(0.479*ymax,0.479*ymax+15)
			x1=random.uniform(0.027*xmax,0.027*xmax+40)
			y1=random.uniform(0.543*ymax,0.543*ymax+50)
			tim=random.randrange(400,800)
			
			os.system("adb -s {} shell input keyevent 4".format(device))
			if len(face_locations) is 0:
				os.system("adb -s {} shell input swipe {} {} {} {} {}".format(device,x2,y2,x1,y1,tim))
				if reason==1:
					print('Reason:Swiped Left. No/Unrecognizale Face.')				
				break

			else:
				os.system("adb -s {} shell input swipe {} {} {} {} {}".format(device,x1,y1,x2,y2,tim))
				if reason==1:
					print('Swiped Right.')
				break



os.system('touch words.txt')
with open("words.txt",) as file:
	pepev=file.read()
	pepv=pepev.strip()
	pepx=pepv. lower()
	pepl=pepv.split('\n')

def main():
	tap(device,xmax,ymax)
	scrface(device)
	cropf(device,xmax,ymax)
	swipe(device,xmax,ymax)
	screenshot(device)
	crop(device,xmax,ymax)

	bsp=ocr(device)['biosplit']
	biosplitsml=ocr(device)['biosplitsml']

	#print(bsp)

	checker(device,pepl,bsp,xmax,ymax,biosplitsml,reason)
		


if __name__=='__main__':
	while(1):
		main()




