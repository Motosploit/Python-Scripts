#run an sslscan then analyze the output and create registry keys based on the output
#future ideas can we do this for linux? It would just be a config file too.
#Cipher suite reference file https://testssl.sh/openssl-rfc.mapping.html

#add support to use argument for host instead of a prompt
#do we need to identify the windows server version to make the right keys? 
#would have different generate_reg_keys functions for each type of windows server, have a selection of server type after running

import subprocess
import sys
import re

end = '\033[1;m'
green = '\033[1;32m'

print """%s
		Thanks for using the sslscan registry key generator. This script runs sslscan
		then generates registry keys to disable weak protocols in windows machines.
		Version 1: Generates keys to disable the SSLv2, SSLv3, TLSv1.0 and TLSv1.1, feel free to adjust the script to suit your needs\n
		Author: Written by Ben Sondgeroth <motosploit@gmail.com> Twitter: @MotoSploit

		sslscan Authors:
				originally written by Ian Ventura-Whiting <fizz@titania.co.uk>.
			   extended by Jacob Appelbaum <jacob@appelbaum.net>.
			   extended by rbsec <robin@rbsec.net>.
		%s""" % (green, end)
print "Usage: ./SSLScan_with_File_Creation.py [host:port]"

def main():
	#global host
	#no fancy command line parsing here
	#check for argument values and there are at least 2 arguments
	if len(sys.argv[1:]) != 1:
		# print out examples of usage
		print "Usage: ./SSLScan_with_File_Creation.py [host:port]"
		sys.exit(0)
	else:
		#setup parameters
		host = sys.argv[1]
		#port = int(sys.argv[2])
		sslscanner(host)
		scrub_output(output)
		generate_protocol_reg_keys(scrubbed_output)
		generate_weak_cipher_reg_keys_for_strong_protocols(scrubbed_output)
		print "Registry key file created under /tmp/ciphers.reg"
	

#set host to be input of user and check it is valid
def set_host():
#set host as global variable
	global host
#keep asking for input until values are entered
#todo: check for valid IP or hostname instead of just null
	while True:
		host = raw_input("What host would you like to scan? ")
		if host == '': 
			print "Please enter a IP address or hostname."
		elif host != '':
			return host

#run sslscan using set value from above
def sslscanner(system_address):
	global output
#set sslscan sgandard output to proc variable 
	proc = subprocess.Popen(["sslscan", "--no-fallback", "--no-renegotiation", "--no-compression", "--no-heartbleed", "--no-check-certificate", system_address], stdout=subprocess.PIPE)
#read the standard output and set it to output variable
	output = proc.stdout.read()
	return output

#scrub out color coding ascii characters from sslscan output
def scrub_output(sslscan_output):
	global scrubbed_output
	#delete the characters
	scrubbed_output = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]','',sslscan_output)
	#return new global variable with scrubbed data
	return scrubbed_output

#scan output for SSLv3, SSLv2, TLSv1.0, TLSv1.1 protocols
def generate_protocol_reg_keys(sslscan_output):

#create registry file in the temporary directory with first line, overwriting any previous versions.
#todo: add ip or hostname to file name
	f = open("/tmp/ciphers.reg", 'w')
	f.write("Windows Registry Editor Version 5.00\n")
	f.close
#set match variable to False
	match = False
	
	if "SSLv2" in sslscan_output:
	#create registry key to disable SSLv2
		print "SSLv2 Found"
		match = True
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
	
	if "SSLv3" in sslscan_output:
	#create registry key to disable SSLv3
		print "SSLv3 Found"
		match = True
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
	
	if "TLSv1.0" in sslscan_output:
	#create registry key to disable TLSv1.0
		print "TLSv1.0 Found"
		match = True
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
		
	if "TLSv1.1" in sslscan_output:
	#create registry key to disable TLSv1.1
		print "TLSv1.1 Found"
		match = True
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
	
	if match == False:
		print "No Weak Protocols Found"

#Identify specific ciphers to disable under TLSv1.2		
def generate_weak_cipher_reg_keys_for_strong_protocols(sslscan_output):

#set match to False
	match = False

#identify ciphers running 1024bits or less DHE
	if re.search(r"TLSv1\.2([a-zA-Z0-9\[\^\s\-]+)DHE (([0-9][0-9]|[0-9][0-9][0-9]|10[0-2][0-4])\s+)bits", sslscan_output):
		#create registry key to disable key lengths of 1024 and less
		print "TLSv1.2 with DHE key length of 1024 or less found"
		match = True
		f = open("/tmp/ciphers.reg", 'a')
		f.write('''[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\KeyExchangeAlgorithms]\n
		[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\KeyExchangeAlgorithms\Diffie-Hellman]
		"ServerMinKeyBitLength"=dword:00000800\n''')
		f.close

		#identify ciphers running DES
	if re.search(r"TLSv1\.2([a-zA-Z0-9\[\^\s\-]+)DES", sslscan_output):
		#create registry key to disable DES
		print "TLSv1.2 with DES found"
		match = True
		f = open("/tmp/ciphers.reg", 'a')
		f.write('''[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers]\n
		[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\DES 56/56]
		"Enabled"=dword:00000000\n''')
		f.close
		
		#identify ciphers running Triple DES
	if re.search(r"TLSv1\.2([a-zA-Z0-9\[\^\s\-]+)DES-CBC3", sslscan_output):
		#create registry key to disable Triple DES
		print "TLSv1.2 with Triple DES found"
		match = True
		f = open("/tmp/ciphers.reg", 'a')
		f.write('''[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers]\n
		[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\Triple DES 168]
		"Enabled"=dword:00000000\n''')
		f.close
	
		#identify ciphers running RC4
	if re.search(r"TLSv1\.2([a-zA-Z0-9\[\^\s\-]+)RC4", sslscan_output):
		#create registry key to RC4
		print "TLSv1.2 with RC4 found"
		match = True
		f = open("/tmp/ciphers.reg", 'a')
		f.write('''[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers]\n
		[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\RC4 128/128]
		"Enabled"=dword:00000000\n
		[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\RC4 40/128]
		"Enabled"=dword:00000000\n
		[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\RC4 56/128]
		"Enabled"=dword:00000000\n''')
		f.close
	
		#identify ciphers running MD5
	if re.search(r"TLSv1\.2([a-zA-Z0-9\[\^\s\-]+)MD5", sslscan_output):
		#create registry key to MD5
		print "TLSv1.2 with MD5 found"
		match = True
		f = open("/tmp/ciphers.reg", 'a')
		f.write('''[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes]\n
		[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\MD5]
		"Enabled"=dword:00000000\n''')
		f.close
		
		#add sha1 (might need a non match so it doesnt include sha256 etc)

	if match == False:
		print "No Weak Ciphers Found"

main()