from sense_hat import SenseHat
from time import sleep 

# Threashold level variables 
Temp_threashold = 0
Hum_threashold = 25
Pres_threashold = 480

Temp_button= "up"
Hum_button= "down"
Pres_button = "left"


s = SenseHat()                #senseHat instance

s.clear()                     #clear the LedMatrix

s.set_rotation(270)           

#Data Lists
splited = []
hum= []
temp= []
pressure= []

#RGB color code
red= (255,0,0)
green = (0,255,0)
blue=(0,255,255)
yellow = (255,255,0)
pink=(255,105,180)

#overwrite the existing text file, create one in case it does'nt exist
with open('Data.txt', 'w') as fily : 
  print('reset')


def collect() : 
# Data is read every 1s  
  with open('Data.txt', 'a') as myFile :  #append the previous data
  
    t = s.get_temperature()
    p = s.get_pressure()
    h = s.get_humidity()
    t = round(t, 3)                       #round to 3 decimal places 
    p = round(p, 3)
    h = round(h, 3)
    myFile.write(t)
    myFile.write(',')
    myFile.write(p)
    myFile.write(',')
    myFile.write(h)
    myFile.write('\n') #newline
    
    if(t <= Temp_threashold) :      #threashold level for temp
      s.set_pixel(0,0,red)   #fire a red LED
    else : 
      s.set_pixel(0,0,(0,0,0)) #clear the led 
      
    if(p <= Pres_threashold) :      #threashold level for pressure
      s.set_pixel(1,0,blue)
    else : 
      s.set_pixel(1,0,(0,0,0))
      
    if(h <= Hum_threashold) :       #threashold level for humidity
      s.set_pixel(2,0,yellow)
    else : 
      s.set_pixel(2,0,(0,0,0))
      
    #keep leds on for half a second   
    sleep(.5) 
    s.clear()
    #keep leds on for half a second
    sleep(.5)

def read() : 
  
  #clear all data lists 
  del splited[:]
  del hum[:]
  del temp[:]
  del pressure[:]
  
  with open('Data.txt', 'r') as file:
    #fill up data lists
    d = file.read()
    reading = d.split('\n')
    
    for i in reading: 
      splited.append(i.split(','))
  
    for line in splited :
      if len(line) > 2 : 
        temp.append(float(line[0]))
        pressure.append(float(line[1]))
        hum.append(float(line[2]))
    


def median(lst):
  sortedLst = sorted(lst)
  lstLen = len(lst)
  index = (lstLen - 1) // 2

  if (lstLen % 2):
      return sortedLst[index]
  else:
      return round((sortedLst[index] + sortedLst[index + 1])/2.0 , 3)

def mean(lst) : 
  n = len(lst)
  return round(sum(lst) / n , 3) 
  
def display_details(lst) : 
  read()
  s.show_message("max : " + str(max(lst)), scroll_speed = 0.05,text_colour=green)
  s.show_message("min : " + str(min(lst)), scroll_speed = 0.05,text_colour=blue)
  s.show_message("mean : " + str(mean(lst)), scroll_speed = 0.05,text_colour=yellow)
  s.show_message("median : " + str(median(lst)), scroll_speed = 0.05,text_colour=pink)


  
  
while True : 

  collect()

  for event in s.stick.get_events():
    
    print(event.action,event.direction)
    
    if event.action == "pressed":
      
      if event.direction == Temp_button:
        
        s.show_message("Temp : " + str(round(s.get_temperature(),3)),scroll_speed = 0.05)
        display_details(temp)
        
      elif event.direction == Hum_button:
        
        s.show_message("Hum : " + str(round(s.get_humidity(),3)) ,scroll_speed = 0.05)
        display_details(hum)
      
      elif event.direction == Pres_button: 
      
        s.show_message("Pressure : " + str(round(s.get_pressure(),3)) ,scroll_speed = 0.05)
        display_details(pressure)
 
      
      # Wait a while and then clear the screen
      sleep(0.2)
      s.clear()
      
      
