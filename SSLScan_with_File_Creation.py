#run an sslscan then analyze the output and create registry keys based on the output
#future ideas can we do this for linux? It would just be a config file too.

import subprocess
import sys

print """Thanks for using the sslscan registry key generator. This script runs sslscan
then generates registry keys to disable weak protocols in windows machines.
Version 1: Generates keys to disable the SSLv2, SSLv3, TLSv1.0 and TLSv1.1, feel free to adjust the script to suit your needs\n
Author:
	Written by Ben Sondgeroth <motosploit@gmail.com> Twitter: @MotoSploit

sslscan Authors:
       originally written by Ian Ventura-Whiting <fizz@titania.co.uk>.
       extended by Jacob Appelbaum <jacob@appelbaum.net>.
       extended by rbsec <robin@rbsec.net>.
 """
#set host to be input of user and check it is valid
def set_host():
#set host as global variable
	global host
#keep asking for input until values are entered
#need to edit this to check for valid IP or hostname instead of just null
	while True:
		host = raw_input("What host would you like to scan? ")
		if host == '': 
			print "Please enter a IP address or hostname."
		elif host != '':
			return host

#run sslscan using set value from above
def sslscanner(a):
	global output
#set sslscan sgandard output to proc variable 
	proc = subprocess.Popen(["sslscan", "--no-fallback", "--no-renegotiation", "--no-compression", "--no-heartbleed", "--no-check-certificate", a], stdout=subprocess.PIPE)
#read the standard output and set it to output variable
	output = proc.stdout.read()
	return output

#do we need to identify the windows server version to make the right keys? 
#would have different generate_reg_keys functions for each type of windows server

def generate_reg_keys(b):
#scan file for SSLv3, SSLv2, TLSv1.0, TLSv1.1
#TLSv1.2 is allowed so would have to identify weak ciphers specifically
#use specific strings like "TLSv1.2  128 bits  AES128-GCM-SHA256", this isnt acually weak just an example
#each key generation could be its own function?

#create registry file in the temporary directory with first line, overwriting any previous versions.
	f = open("/tmp/ciphers.reg", 'w')
	f.write("Windows Registry Editor Version 5.00\n")
	f.close
	
	if "SSLv2" in b:
	#create registry key to disable SSLv2
		print "SSLv2 Found"
		f = open("/tmp/ciphers.reg", 'a')
		f.write('''[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols]\n
		[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0]\n
		[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Client]
		"Enabled"=dword:00000000
		"DisabledByDefault"=dword:00000001\n
		[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Server]
		"Enabled"=dword:00000000
		"DisabledByDefault"=dword:00000001\n''')
		f.close
	
	if "SSLv3" in b:
	#create registry key to disable SSLv3
		print "SSLv3 Found"
		f = open("/tmp/ciphers.reg", 'a')
		f.write('''[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols]\n
		[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0]\n
		[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Client]
		"Enabled"=dword:00000000
		"DisabledByDefault"=dword:00000001\n
		[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Server]
		"Enabled"=dword:00000000
		"DisabledByDefault"=dword:00000001\n''')
		f.close
	
	if "TLSv1.0" in b:
	#create registry key to disable TLSv1.0
		print "TLSv1.0 Found"
		f = open("/tmp/ciphers.reg", 'a')
		f.write('''[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols]\n
		[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0]\n
		[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Client]
		"Enabled"=dword:00000000
		"DisabledByDefault"=dword:00000001\n
		[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Server]
		"Enabled"=dword:00000000
		"DisabledByDefault"=dword:00000001\n''')
		f.close
		
	if "TLSv1.1" in b:
	#create registry key to disable TLSv1.1
		print "TLSv1.1 Found"
		f = open("/tmp/ciphers.reg", 'a')
		f.write('''[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols]\n
		[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1]\n
		[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Client]
		"Enabled"=dword:00000000
		"DisabledByDefault"=dword:00000001\n
		[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Server]
		"Enabled"=dword:00000000
		"DisabledByDefault"=dword:00000001\n''')
		f.close
	
	if "TLSv1.2" in b:
	#create registry key to disable specific TLSv1.2 weak ciphers
		print "TLSv1.2 Found"
	
	else:
		print "No Weak Ciphers Found"
		
def main():
	set_host()
	sslscanner(host)
	generate_reg_keys(output)

main()