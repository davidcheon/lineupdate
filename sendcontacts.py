#!/usr/bin/python
#!-*- coding:utf-8 -*-
import time
import line
from line.curve import ttypes
import threading
import os
def checkislogin(arg):
	if arg:
		def _func(func):
			def wrapper(*agr1,**agr2):
				return func(*arg1,**arg2)
	else:
		print 'login first'
class mycontactsender(object):
	def __init__(self,id,pwd,device):
		self.id=id
		self.device=device
		self.pwd=pwd
		self.groupid='c606c0578c586e81a38fa9c1a2c547f08'
		self.status=False
		self.lastsend=0
		self.mids=[]
		self.values={}
		self.authtoken=None
		self.stop=0
		self.deletecounts=None
		self.blocked={}
		self.errorcount=0
		self._login()
		self.savemids()
	def savemids(self):
		if self.status:
			filename=os.path.join('mids','mids-%s.txt'%(self.device.split(':')[1]))
			line=0
			if os.path.exists(filename):
				with open(filename,'r') as f:
					line=len(f.readlines())
				if line<len(self.contacts)-1:
					with open(filename,'wb+') as f:
						for contact in self.contacts:
							#LINE's id
							if contact.id!='u085311ecd9e3e3d74ae4c9f5437cbcb5':
								f.writelines('%s\n'%contact.id)
					print 'Mids updated  <%s> succeed.'%(filename)
			else:
					with open(filename,'wb+') as f:
						for contact in self.contacts:
							#LINE's id
							if contact.id!='u085311ecd9e3e3d74ae4c9f5437cbcb5':
								f.writelines('%s\n'%contact.id)
					print 'Mids saved in <%s> succeed.'%(filename)	
		else:
			print 'login first'		
			
	def _login(self):
		try:
			if self.authtoken is None:
				self.client=line.LineClient(self.id,self.pwd)
				self.authtoken=self.client.authToken
			else:
				self.client=line.LineClient(authToken=self.authtoken)
			self.status=True
			self.getcontacts()
		except Exception,e:
			print 'login failed'
			self.status=False
	def unblockcontacts(self):
		if self.status:
			count=1
			for id,name in self.blocked.items():
				self.client._unblockContact(id)
				print '%d:<%s> unblock succeed.'%(count,name)
				count+=1
				time.sleep(3)
	def getcontacts(self):
		if self.status:
			self.contacts=self.client.contacts
			for contact in self.contacts:
				self.values[contact.id]=contact.name
				self.mids.append(contact.id)
			self.mids.sort()
	def sendaction(self,start=None,end=None):
		if start is not None:
			self.lastsend=start-1
		else:
			start=self.lastsend+1
		if end is None:
			if self.stop!=0:
				end=self.stop+1
			else:
				self.stop=len(self.contacts)-1
				end=self.stop+1
			cou=start-1
		else:
			self.stop=end-1
			cou=start
		if start <=0 or start>end or end>len(self.contacts):
			print 'invalid start or end'
		else:
			if self.deletecounts is None:
				self.deletecounts=end-start+1
			if self.errorcount>0:self._login()
			if self.status:
				num=0
				self.errorcount=0
				for id in self.mids[self.lastsend:end+1]:				
					try:
						name=self.values[id]
						#LINE's id 1448745488229
						if id!='u085311ecd9e3e3d74ae4c9f5437cbcb5' or name!='LINE':
							msg=ttypes.Message		(contentType=13,hasContent=False,text=None,to=self.groupid,contentPreview=None,location=None,deliveredTime=int(time.time()*1000),createdTime=int(time.time()*1000),_from='ua112440ce9f59c46054b39ac892a8cc7', contentMetadata={'displayName': name, 'mid': id, 'seq': '13'}, 
toType=2)
							self.client.groups[0].sendContactMessage(msg)							
							self.lastsend=cou
							self.stop=end-1
#							self.client._blockContact(id)
							self.blocked[id]=name
							print '%d:<%s> sent and block succeed.'%(cou,name)
							cou+=1
							num+=1
							time.sleep(4)
					except Exception,e:
						self.errorcount+=1
						self.lastsend=cou
						self.stop=end-1
						print '%s send <%d> items failed'%(name,cou)
						print 'Total send <%d> items succeed'%num
						break
				print 'Total send <%d> items succeed'%(self.deletecounts)
				self.deleteblockedfriends(self.deletecounts)
	
	def deleteblockedfriends(self,num):
		status=os.system('adb -s %s shell "su -c \'[ ! -d /vendor/test/shieldfriends/data ] && mkdir -p /vendor/test/shieldfriends/data && chmod -R 777 /vendor\'"'%(self.device))
		if status==0:
			status=os.system('adb -s %s push %s /vendor/test/shieldfriends/'%(self.device,os.path.join('D:\\','david','test','shieldfriends','shieldanddeletefriends.sh')))
			if status==0:
				status=os.system('adb -s %s shell sh /vendor/test/shieldfriends/shieldanddeletefriends.sh %d'%(self.device,num))
				if status==0:
					print 'delete <%d> items succeed'%num
				else:
					print 'delete action failed'
			else:
				print 'push shell failed'
		else:
			print 'mkdir failed'
class mycontactreceiver(object):
	def __init__(self,id,pwd,counts=10000):
		self.id=id
		self.pwd=pwd
		self.status=False
		self.groupid='c606c0578c586e81a38fa9c1a2c547f08'
		self.counts=counts
		self.lastsend=0
		self.lastidindex=0
		self.errorcounts=0
		self.fromusertoken=None
		self.tousertoken=None
		self.totalsend=None
		self._login()
	def _login(self):
		try:
			if self.fromusertoken is None:
				self.client=line.LineClient(self.id,self.pwd)
				self.fromusertoken=self.client.authToken
			else:
				self.client=line.LineClient(authToken=self.fromusertoken)
			self.status=True
			self._getcontactids()
			self._getgroupreceived()
#			self.getgroupreceivedupdate()
		except Exception,e:
			self.status=False
			print 'login failed'	
	def _getcontactids(self):
		self.contactids=set([n.id for n in self.client.contacts])
		#LINE's id  #### acang's id ## guanhao1's id
		deletecontactids=set(['u085311ecd9e3e3d74ae4c9f5437cbcb5','u8cd5f4f7fefc80ec159f1daee05dec84','ua112440ce9f59c46054b39ac892a8cc7'])
		self.contactids=list(self.contactids-deletecontactids)
	def _getgroupreceived(self):
		self.messages=[]
		if self.status:
			group=self.client.getGroupById(self.groupid)
			tmps=group.getRecentMessages(count=self.counts)
			for temp in tmps:
				try:
					msg=temp._message
					if not msg.hasContent:
						self.messages.append(msg)
				except Exception,e:
					pass
			self.messages=list(set(self.messages))
			self.dicts={}
			for message in self.messages:
				try:
					if self.dicts.has_key(message.contentMetadata['mid']):
						continue
					self.dicts[message.contentMetadata['mid']]=message
				except Exception,e:
					pass
			self.messages=self.dicts.values()
			print 'You got %d items'%len(self.messages)
	def getgroupreceivedupdate(self):
		self.messages=[]
		if self.status:
			for poll in self.client.longPoll(count=self.count):
				receiver=poll[1]
				if receiver.id==self.groupid:
					msg=poll[2]._message
					if not msg.hasContent:
						self.messages.append(msg)
	def sendcontactstofriends(self,start=None,stop=None):
		stop= len(self.messages) if stop is None else stop
		if start is None:
			start=self.lastsend+1
		else:
			self.lastsend=start-1
		if start<=0 or start>stop or stop>len(self.messages):
			print 'invalid start or stop'
		else:
#			try:
#				if self.tousertoken is None:
#					touser=line.LineClient(touserid,touserpwd)
#					self.tousertoken=touser.authToken
#				else:
#					touser=line.LineClient(authToken=self.tousertoken)
#			except Exception,e:
#				print 'login failed'
#			else:
#				tousercontacts=touser.contacts
#				touserids=[t.id for t in tousercontacts]			
				to=self.contactids
				if self.errorcounts>0:
					if self.fromusertoken is None:
						self.client=line.LineClient(self.id,self.pwd)
						self.fromusertoken=self.client.authToken
					else:
						self.client=line.LineClient(authToken=self.fromusertoken)
				self.lastsend=start-1 if self.lastsend==0 else self.lastsend
				if self.status and self.messages[self.lastsend:stop]!=[]:
					for i,id in enumerate(to[self.lastidindex:]):
						iii=2 if self.lastidindex==0 else 0
						#LINE's id
						if id!='u085311ecd9e3e3d74ae4c9f5437cbcb5' and i==iii:
							name=self.client.getContactById(id).name
							self.errorcounts=0
							co=self.lastsend+1
							print '='*10,stop
							for msg in self.messages[self.lastsend:stop]:
								try:
									msgid=msg.contentMetadata['mid']
									print '-'*10
									msg.to=id
									#chuangjianqunzu's id
									msg._from='u0a51561594a2a774c0c64b8501f308b7'
									msg.toType=0
						
									self.client.groups[0].sendContactMessage(msg)
									print name,co
									co+=1
									time.sleep(5)
								except Exception,e:
									print '%s error occured:%s'%(name,str(e))
									self.errorcounts+=1
									self.lastsend=co-1
									self.lastidindex=i
									break
						
							print '%s send <%d> items succeed.'%(name,(co-start))
							if self.errorcounts>0:break
	def sendcontactstofriendsupdate(self,touserid,touserpwd,start=None,stop=None):
		stop= len(self.messages)-1 if stop is None else stop
		if start is None:
			start=self.lastsend+1
		else:
			self.lastsend=start-1
		if start<=0 or start>stop or stop>len(self.messages):
			print 'invalid start or stop'
		else:
			try:
				if self.tousertoken is None:
					touser=line.LineClient(touserid,touserpwd)
					self.tousertoken=touser.authToken
				else:
					touser=line.LineClient(authToken=self.tousertoken)
			except Exception,e:
				print 'touser login failed'
			else:
				tousercontacts=touser.contacts
				touserids=[t.id for t in tousercontacts]			
				to=self.contactids
				if self.fromusertoken is None:
					self.client=line.LineClient(self.id,self.pwd)
					self.fromusertoken=self.client.authToken
				else:
					self.client=line.LineClient(authToken=self.fromusertoken)
#				self.lastsend=start-1 if self.lastsend==0 else self.lastsend
				if self.status and self.messages[self.lastsend:stop+1]!=[]:
#					self.getgroupreceived()
					for i,id in enumerate(to[self.lastidindex:]):
						iii=2 if self.lastidindex==0 else 0
						#LINE's id
						if id!='u085311ecd9e3e3d74ae4c9f5437cbcb5' and i==iii:
							name=self.client.getContactById(id).name
							self.errorcounts=0
#							co=self.lastsend+1
							co=start
							num=0
							for msg in self.messages[self.lastsend:stop+1]:
								try:
									msgid=msg.contentMetadata['mid']
									if msgid not in touserids:
										msg.to=id
										#chuangjianqunzu's id
										msg._from='u0a51561594a2a774c0c64b8501f308b7'
										msg.toType=0
						
										self.client.groups[0].sendContactMessage(msg)
										print '%d:<%s> send succeed.'%(co,name)
										co+=1
										num+=1
										self.lastidindex=i
										time.sleep(5)
									self.lastidindex=i
									self.lastsend+=1
								except Exception,e:
									print '%s error occured:%s'%(name,str(e))
									self.errorcounts+=1
#									self.lastsend=co-1
									break
						
							print '%s send <%d> items succeed.'%(name,num)
							if self.errorcounts>0:break
	def sendcontactstofriendsupdate2(self,start=None,stop=None):
		stop= len(self.messages) if stop is None else stop
		if start is None:
			start=self.lastsend+1
		else:
			self.lastsend=start-1
		if start<=0 or start>stop or stop>len(self.messages):
			print 'invalid start or stop'
		else:

			if self.status and self.messages[self.lastsend:stop]!=[]:
				if self.totalsend is None:
					self.totalsend=stop-start+1
				co=start
				name='<'
				for cont in self.contactids:
					id=cont.id
					cont=self.client.getContactById(id)
					name+=cont.name+','
				name+='>'
				for msg in self.messages[self.lastsend:stop]:
					try:
						msgid=msg.contentMetadata['mid']
						#chuangjianqunzu's id
						msg._from='u0a51561594a2a774c0c64b8501f308b7'
						msg.toType=0
						for id in self.contactids:
							msg.to=id
							contact=self.client.getContactById(id)
							contact.sendContactMessage(msg)
						print '%d:<%s> send succeed.'%(co,name)
						co+=1
						time.sleep(5)
						self.lastsend+=1
					except Exception,e:
						print 'error occured:%s'%(str(e))
						break
						
				print 'Total send <%d> items succeed.'%(self.totalsend)
class myaddfriendsbymid(object):
	def __init__(self,id,pwd):
		self.id=id
		self.pwd=pwd
		self.status=False
		self._login()
	def _login(self):
		try:
			if not self.status:
				self.client=line.LineClient(self.id,self.pwd)
				self.status=True
				self._getreceivedmids()
		except Exception,e:
			self.status=False
	def _getreceivedmids(self):
		if self.status:
			#id=guanhao's id
			fromuser=self.client.getContactById('ua112440ce9f59c46054b39ac892a8cc7')
			if fromuser is not None:
				linemessages=fromuser.getRecentMessages(count=100000)
				self.mids=[]
				for linemessage in linemessages:
					try:
						if isinstance(linemessage,line.LineMessage):
							mid=linemessage._message.contentMetadata['mid']							
							self.mids.append(mid)	
					except Exception,e:
						pass
			else:
				self.mids=None
	def _getreceivedmidsupdate(self):
		if self.status:
			#id=guanhao's id
			self.mids=[]
			for pol in self.client.longPoll(count=100000):
				sender=pol[0]
				msg=pol[2]
				if sender.id=='ua112440ce9f59c46054b39ac892a8cc7':
					try:
						mid=msg._message.contentMetadata['mid']
						self.mids.append(mid)
					except Exception,e:
						pass
			else:
				self.mids=None
			
	def addfriendsbymids(self):
		if self.status and self.mids is not None and self.mids!=[]:
			flag=True
			for mid in self.mids:
				try:
					self.client._findAndAddContactsByMid(mid)
					print 'add <%s> succeed'%mid
#					time.sleep(5)
				except Exception,e:
					flag=False
					break
			print 'succeed' if flag else 'failed'
		else:
			print 'login first or no mids'
					

class myaddfriendsbymidupdate(object):
	def __init__(self,id,pwd):
		self.id=id
		self.pwd=pwd
		self.status=False
		self.sender='u0a51561594a2a774c0c64b8501f308b7'
		self.authtoken=None
		self._login()
	def _login(self):
		try:
#			if not self.status:
			if self.authtoken is None:
				self.client=line.LineClient(self.id,self.pwd)
				self.authtoken=self.client.authToken
			else:
				self.client=line.LineClient(authToken=self.authtoken)
			self.contactids=[contact.id for contact in self.client.contacts]
			self.status=True
			self._getreceivedmids()
		except Exception,e:
			print 'login failed:%s'%str(e)
	def getaddingcontactscounts(self):
		return len(self.mids)
	def _getreceivedmids(self):
		self.mids={}
		sender=self.client.getContactById(self.sender)
		if sender is not None:
			msgs=sender.getRecentMessages(count=10000)
			if msgs!=[]:
				for msg in msgs:
					mid=msg.contentMetadata['mid']
					if mid not in self.contactids:
						name=msg.contentMetadata['displayName']
						self.mids[mid]=name
		else:
			print 'can not find sender'
					
	def addfriendsbymids(self):
		if self.status and self.mids!={}:
			count=1
			for mid,name in self.mids.items():
				try:
					self.client._findAndAddContactsByMid(mid)
					print '%d: add <%s> succeed'%(count,name)
					count+=1
#					time.sleep(5)
				except Exception,e:
					print 'error occured:%s'%str(e)
					break
		else:
			print 'login first or no mids'

if __name__=='__main__':
#	ms=mycontactsender('1960772215@qq.com','521125dane')
#	ms.sendaction()
	mr=myaddfriendsbymid('1960772215@qq.com','521125dane')
	mr.addfriendsbymids()
