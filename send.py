from googlevoice import Voice
from googlevoice.util import input
import sys

f=open(sys.argv[1],'r')
data=[]
x=f.readline()
while x!='':
  data.append(x)
  x=f.readline()
print data
data=str(data).split(',')
print data
voice=Voice()
voice.login()

text=data[1]
phone=data[2]
print text,phone
voice.send_sms(phone, text)
