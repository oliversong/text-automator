import sys
import os
import re
import ast
from datetime import datetime
from datetime import timedelta
import dateutil.parser as dparser

def fixremind(x):
  if x[:11].lower()=='reminder me':
    return 'remind me'+x[11:]
  else:
    return x
def timeparser(time,target,tog):
  if tog: #in
    typematch=re.search('([0-9]+) ([a-z]+)[.]?',target)
    if typematch.group(2)=='hours' or typematch.group(2)=='hrs' or typematch.group(2)=='hr' or typematch.group(2)=="hour":
      dtime=dparser.parse(time)+timedelta(hours=int(typematch.group(1)))
      return dtime.strftime('%H:%M')
    elif typematch.group(2)=='minutes' or typematch.group(2)=='mins' or typematch.group(2)=='min' or typematch.group(2)=='minute':
      dtime=dparser.parse(time)+timedelta(minutes=int(typematch.group(1)))
      return dtime.strftime('%H:%M')
    else:
      print "IN Time format not recognized, the item was: ",target
  else: #at
    if target[-2:].lower()=='pm' or target[-2].lower()=='am':
      dtime=dparser.parse(target)
      #print dtime.strftime('%H:%M')
      return dtime.strftime('%H:%M')
    elif ":" in target or len(target)==1 or len(target)==2:
      if len(target)==1 or len(target)==2:
        new=target+"00"
      else:
        ind=target.find(":")
        new=target[:ind]+target[ind+1:]
      #figure out whether am or pm
      timematch=re.search('([0-9]+):([0-9]+) (am|pm)',time, flags=re.I)
      x=timematch.group(1)+timematch.group(2)
      ap=timematch.group(3)
      #print x,ap
      if ap.lower()=='am':
        if int(x)>int(new):
          if int(timematch.group(1))==12:  # BUG. IF IT'S 12 AND THE TARGTIME IS ALSO 12, SHOULD BE SAME UNLESS ALREADY PAST
            dtime=dparser.parse(target+"AM")
            return dtime.strftime('%H:%M')
          else:
            dtime=dparser.parse(target+"PM")
            #print dtime
            return dtime.strftime('%H:%M')
        else:
          if int(timematch.group(1))==12:
            dtime=dparser.parse(target+"PM")
            return dtime.strftime('%H:%M')
          else:
            dtime=dparser.parse(target+"AM")
            return dtime.strftime('%H:%M')
      elif ap.lower()=='pm':
        if int(x)<int(new):
          if int(timematch.group(1))==12:
            dtime=dparser.parse(target+"AM")
            return dtime.strftime('%H:%M')
          else:
            dtime=dparser.parse(target+"PM")
            return dtime.strftime('%H:%M')
        else:
          if int(timematch.group(1))==12:
            dtime=dparser.parse(target+"PM")
            return dtime.strftime('%H:%M')
          else:
            dtime=dparser.parse(target+"AM")
            return dtime.strftime('%H:%M')
    else:
      print "AT Time format not recognized!, the item is: ", target
output=[]
filename=sys.argv[1]
f= open(filename,'r')
data=[]
x=f.readline()
while x!='':
  data.append(ast.literal_eval(x))
  x=f.readline()
for text in data:
  content=text[u'text']
  number=text[u'from']
  time=text[u'time']
  toggle=False
  content=fixremind(content)
  if content[:9].lower()=='remind me':
    inind=content.rfind(' in ')
    atind=content.rfind(' at ')
    if inind>atind:
      index=inind
      toggle=True # if it's in, treat it one way
    else:
      index=atind # if it's at, treat it another
    content=content[:index]+' blork '+content[index+4:] #swap it out for blork
    match=re.search('remind me (.+) blork (.+)',content,flags=re.I)
    reminder=match.group(1) #the actual reminder
    tartime=match.group(2)  #the target time
    #print tartime
    fintime=timeparser(time,tartime,toggle)
    output.append([fintime,reminder[3:], number])
  else:
    pass

#for later, add in checking what type of message it is
#for now just doing reminders

# remove repeats
# sort by time
# return ones on current tim
from googlevoice import Voice
from googlevoice.util import input

currenttime=datetime.time(datetime.now())
actualtime=str(currenttime)[:5]

def sortqueue(x):
  temp=[]
  for i in x:
    temp.append(tuple(i))
  temp.sort()
  return temp

def checktime(item):
  try:
    timeelement=str(item).split(',')[0]
    match=re.search('([0-9]+:[0-9]+)',timeelement)
    detecttime=match.group(1)
    if len(detecttime)==4:
      detecttime='0'+detecttime
    if detecttime==actualtime:
      return True
    else:
      return False
  except:
    print "something went wrong!"

#print "output", output
sortd=sortqueue(output)
print "sortd", sortd
currents=[]
for item in sortd:
  if checktime(item):
    print "\n  Time match!\n"
    currents.append(item)
  else:
    print "\n  Question is in the queue. Listening...\n"
print "currents",currents
for current in currents:
  voice=Voice()
  voice.login()
  text=current[1]
  phone=current[2]
  print 'textpacket',text,phone
  voice.send_sms(phone, text)
