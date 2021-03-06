#!/usr/bin/python
#Auther:Sylar Zhao 	
#Email:sylar.zhao@163.com 

import os,re

#Global Variables
tun_path='/etc/sysconfig/network-scripts/'
yesList=['y','Y','Yes','YES']
noList=['n','N','No','NO']
menuList=['1','2','3','4','5','0']
errMsg='Error IP address, please retry:'

#Global Functions,Check IP address 
def CheckIP(ip_addr):
	if	re.search("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", ip_addr):
		ip_list=re.split('\.',ip_addr)
		for ip in ip_list:
			if int(ip) >= 255 or int(ip) <0:
				return False
		return True
	return False
#Global Functions,Check string
def CheckInput(str, strList):
	if str in strList:
		return True
	return False
#Create Tunnel Function
def CreTun(iTunNum, sTunSor, sTunDes, sLocIp, sDesIp):
	tun_info=[]
	tun_info.append('DEVICE=tun'+str(iTunNum))
	tun_info.append('ONBOOT=yes')
	tun_info.append('TYPE=GRE')
	tun_info.append('MY_INNER_IPADDR='+sTunSor)
	tun_info.append('PEER_INNER_IPADDR='+sTunDes)
	tun_info.append('MY_OUTER_IPADDR='+sLocIp)
	tun_info.append('PEER_OUTER_IPADDR='+sDesIp)
	with open(tun_path+'ifcfg-tun'+str(iTunNum),"a") as dfile:
		for line in tun_info:
			dfile.write(line+'\n')
#Enable Tunnel Function
def EnableTun(iTunNum):
	cmd='ifup '+tun_path+'ifcfg-tun'+str(iTunNum)
	os.popen(cmd)
def DisableTun(iTunNum):
	cmd='ifdown '+tun_path+'ifcfg-tun'+str(iTunNum)
	os.popen(cmd)

#Delete Tunnel Function
def DelTun(iTunNum):
	if os.path.exists(tun_path+'ifcfg-tun'+str(iTunNum)):
		cmd='ifdown '+tun_path+'ifcfg-tun'+str(iTunNum)
		os.popen(cmd)
		cmd='rm -rf '+tun_path+'ifcfg-tun'+str(iTunNum)
		os.popen(cmd)
	else:	
		return False
#List Tunnel Function
def ListTun():
	tunList=os.listdir(tun_path)
	tunList.sort()
	print('Following are your current tunnels:')
	for tun in tunList:
		if tun.startswith('ifcfg-tun'):
			print(tun[6:])
	
while(1):
	os.system('clear')
	print('\n#################################################')
	print('[1] Create New tunnel            [2] Delete Tunnel\n')
	print('[3] List All Tunnel              [4] Enable Tunnel\n')
	print('[5] Disable Tunnel               [0] Quit')
	print('#################################################')
	print('Enter an option:')

	menu=input()
	while(1):
		if CheckInput(str(menu),menuList):
			break
		print('Input Error, please retry:')
		menu=input()
	#Create Tunnel	
	if menu==1:
		print('Enter the Tunnel number(1~65535):')
		while(1):
			iTunNum=raw_input()
			if str(iTunNum).isdigit():
				break
			print('Error number!enter the Tunnel number(1~65535):')

		#Check if Tunnel file exists
		while(1):
			if os.path.exists(tun_path+'ifcfg-tun'+str(iTunNum)):
				print('Tunnel number exists, please retry:')
				iTunNum=raw_input()
			break
		#Get tunnel sorce ip address
		while(1):
			print('Please enter tunnel source IP address:(for example: 10.10.10.1)')
			sTunSor=raw_input()
			if CheckIP(sTunSor):
				break
			print(errMsg)
		#Get tunnel destination ip address
		while(1):
			print('Please enter tunnel destination IP address:(for example: 10.10.10.2)')
			sTunDes=raw_input()
			if CheckIP(sTunDes):
				break
			print(errMsg)
		#Get local public ip address
		while(1):
			print('Please enter local public IP address:(for example: 202.96.186.22)')
			sLocIp=raw_input()
			if CheckIP(sLocIp):
				break
			print(errMsg)
		#Get destination public ip address
		while(1):
			print('Please enter tunnel destination IP address:(for example: 202.96.123.21)')
			sDesIp=raw_input()
			if CheckIP(sDesIp):
				break
			print(errMsg)
		#Confirm all informations
		print('Please confirm your GRE tunnel information:')
		print('Tunnel source IP address: '+sTunSor)
		print('Tunnel destination IP address: '+sTunDes)
		print('Local public IP address: '+sLocIp)
		print('Destination public IP address: '+sDesIp)
		print('Do you want create tun'+str(iTunNum)+'?(y/n) ')
		cfmMsg=raw_input()	
		while(1):
			if CheckInput(cfmMsg,yesList):
				print('Creating GRE tunnel...')
				CreTun(iTunNum, sTunSor, sTunDes, sLocIp, sDesIp)
				print('Success! Do you want enable the tunnel now(y/n)')
				cfmMsg=raw_input()
				if CheckInput(cfmMsg,yesList):
					EnableTun(iTunNum)
					print('Enabling tunnel...')
				print('Tunnel has been created, press "Enter" key to continue')
				raw_input()
				break
			print('Abort and press "Enter" key to continue...')		
			raw_input()
			break
	#Delete Tunnel
	elif menu==2:
		ListTun()
		print('Which tunnel would you want delete? for example, delete "tun20", enter "20" \n')
		print('Enter the tunnel number:')
		iTunNum=raw_input()
		if os.path.exists(tun_path+'ifcfg-tun'+str(iTunNum)):
			print('Do you want delete tun'+iTunNum+'?(y/n)')
			cfmMsg=raw_input()
			if CheckInput(cfmMsg,yesList):
				print('Disabling tun'+iTunNum+'...')
				DisableTun(iTunNum)
				print('Deleting tun'+iTunNum+' file...')
				DelTun(iTunNum)
				print('Tun'+iTunNum+' has been deleted, press "Enter" key to continue')
				raw_input()
		else:
			print('Tun'+iTunNum+' is not exists,press "Enter" key to continue')
			raw_input()
	#List Tunnels
	elif menu==3:
		ListTun()
		print('\nPress "Enter" key to continue')
		raw_input()
	elif menu==4:
		ListTun()
		print('Enter the tunnel number:')
		iTunNum=raw_input()
		if os.path.exists(tun_path+'ifcfg-tun'+str(iTunNum)):
			EnableTun(iTunNum)
			print('Tun'+iTunNum+' has been enabled, press "Enter" key to continue')
			raw_input()
		else:
			print('Tun'+iTunNum+' is not exists,press "Enter" key to continue')
			raw_input()
	elif menu==5:
		ListTun()
		print('Enter the tunnel number:')
		iTunNum=raw_input()
		if os.path.exists(tun_path+'ifcfg-tun'+str(iTunNum)):
			DisableTun(iTunNum)
			print('Tun'+iTunNum+' has been disabled, press "Enter" key to continue')
			raw_input()
		else:
			print('Tun'+iTunNum+' is not exists,press "Enter" key to continue')
			raw_input()
	elif menu==0:
		exit(0)


