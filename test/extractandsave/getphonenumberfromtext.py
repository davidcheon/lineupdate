#!/usr/bin/python
#!-*- coding:utf-8 -*-
import re
import os
import xlwt
import time
import sys
class mymodel(object):
	def __init__(self,filename):
		self.pat=re.compile('008869\d+')
		self.origfilename=filename
		self.filename=os.path.join('D:\\david\\test\\extractandsave\\data','%s.txt'%filename)
		self.phonenumber={}
		self.flag=False
		self.extractnumber()
	def extractnumber(self):
		with open(self.filename,'r') as f:
			content=f.read()
			results=self.pat.findall(content)
		if results!=[]:
			self.flag=True
			for result in results:
				if not self.phonenumber.has_key(result):
					self.phonenumber[result]=1
				else:
					self.phonenumber[result]+=1
		
	def savetoxls(self):
		if self.flag:
			headers=(u'姓名',u'手机',u'宅话',u'Email',u'地址',u'单位',u'职务')
#			filecounts=len(self.phonenumber)/30 if len(self.phonenumber%30==0)else (len(self.phonenumber)/30+1)
			tmp=False
#			for fileindex in xrange(1,filecounts+1):
			w=xlwt.Workbook()
			ws=w.add_sheet('phonenumbers')
			for i,c in enumerate(headers):
				ws.write(0,i,c)
				ws.col(i).width=6000 if c==u'姓名' else 3000
				ws.col(i).width=6000 if c==u'手机' else 3000
				
			for i,key in enumerate(self.phonenumber.keys()):
				if (i+1)%500==0:
					ws.write(500,0,key)
					ws.write(500,1,key)
					w.save(os.path.join('D:\\david\\test\\extractandsave\\result','phone-%s.xls'%(str(time.time()).replace('.',''))))
					time.sleep(.1)
					if i!=(len(self.phonenumber)-1):
						w=xlwt.Workbook()
						ws=w.add_sheet('phonenumbers')
						for i,c in enumerate(headers):
							ws.write(0,i,c)
							ws.col(i).width=6000 if c==u'姓名' else 3000
							ws.col(i).width=6000 if c==u'手机' else 3000
						
					else:
						tmp=True
				else:
					xline=i%500+1
					ws.write(xline,0,key)
					ws.write(xline,1,key)
				
			if not tmp:
				w.save(os.path.join('D:\\david\\test\\extractandsave\\result','phone-%s.xls'%(str(time.time()).replace('.',''))))
	def savetotxt(self):
		if self.flag:
			with open(os.path.join('D:\\david\\test\\extractandsave\\result','%s.txt'%(self.origfilename)),'w+') as f:
				for key in  self.phonenumber.keys():
					f.writelines('%s\n'%key)
	def printphonenumbers(self):
		if self.flag:
			for k,v in self.phonenumber.items():
				print k,v
		else:
			print 'no phonenumber'
if __name__=='__main__':
	mm=mymodel(sys.argv[1])
#	mm.printphonenumbers()
	mm.savetoxls()
	mm.savetotxt()
