#!/usr/bin/python
#!-*- coding:utf-8 -*-
import time
import line
from line.curve import ttypes

class mycontactsender(object):
	def __init__(self,id,pwd):
		self.id=id
		self.pwd=pwd
		self.groupid='c606c0578c586e81a38fa9c1a2c547f08'
		self.status=False
		self._login()
	def _login(self):
		try:
			self.client=line.LineClient(self.id,self.pwd)
			self.status=True
			self.getcontacts()
		except Exception,e:
			pass
	def getcontacts(self):
		if self.status:
			self.contacts=self.client.contacts
	def sendaction(self):
		if self.status:
			for contact in self.contacts:
				id=contact.id
				name=contact.name
				if id!='u085311ecd9e3e3d74ae4c9f5437cbcb5' or name!='LINE':
					msg=ttypes.Message		(contentType=13,hasContent=False,text=None,to=self.groupid,contentPreview=None,location=None,deliveredTime=1448745488229,createdTime=1448745488229,_from='ua112440ce9f59c46054b39ac892a8cc7', contentMetadata={'displayName': name, 'mid': id, 'seq': '13'}, 
toType=2)
					self.client.groups[0].sendContactMessage(msg)
					time.sleep(1)
class mycontactreceiver(object):
	def __init__(self,id,pwd,counts=10):
		self.id=id
		self.pwd=pwd
		self.status=False
		self.groupid='c606c0578c586e81a38fa9c1a2c547f08'
		self.counts=counts
		self._login()
	def _login(self):
		try:
			self.client=line.LineClient(self.id,self.pwd)
			self.status=True
			self._getcontactids()
			self.getgroupreceived()
		except Exception,e:
			self.status=False	
	def _getcontactids(self):
		self.contactids=[n.id for n in self.client.contacts]
	def getgroupreceived(self):
		if self.status:
			group=self.client.getGroupById(self.groupid)
			tmps=group.getRecentMessages(count=self.counts)
			self.messages=[tmp._message for tmp in tmps]
	def sendcontactstofriends(self,to=[]):
		to=self.contactids if to ==[] else to
		if self.status:
			for i,id in enumerate(to):
				if id!='u085311ecd9e3e3d74ae4c9f5437cbcb5':
					for msg in self.messages:
						msg.to=id
						self.client.contacts[0].sendContactMessage(msg)
						time.sleep(1)

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
	def addfriendsbymids(self):
		if self.status and self.mids is not None:
			flag=True
			for mid in self.mids:
				try:
					self.client._findAndAddContactsByMid(mid)
					time.sleep(1)
				except Exception,e:
					flag=False
					break
			print 'succeed' if flag else 'failed'
		else:
			print 'login first or no mids'
					
		
if __name__=='__main__':
#	ms=mycontactsender('1960772215@qq.com','521125dane')
#	ms.sendaction()
	mr=myaddfriendsbymid('1960772215@qq.com','521125dane')
	mr.addfriendsbymids()
