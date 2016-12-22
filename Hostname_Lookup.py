#for loop through IP list
#	run ns lookup
#	append to file
#	end when list is empty

#import socket module
import socket
import re
# create get_hostname function
def get_hostname(file):
# open file and read it, set to f
	with open(file, 'r') as f:
#loop through reading each line of f and set to line
		for line in f.readlines():
# lookup hostname of the ip from the read line
# set the line to the variable hostname
			hostname = socket.getfqdn(line)
# remove .com from hostname output. 
			name_only = re.sub('(.com)','',hostname)
#append hostnames to file
			e = open('output.xls','a')
			e.write(name_only)
			e.write("\n")
			e.close()
	#		print name_only
# return the hostname and print it out
	#return name_only

# set ips.txt document to files variable. ips.txt is the file
# housing the IPs i want to reslove the hostnames for
files = 'ips.txt'

#call get_hostname function with files variable
hosts = get_hostname(files)
#print hosts

