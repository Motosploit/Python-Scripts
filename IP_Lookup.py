#for loop through IP list
#	run ns lookup
#	append to file
#	end when list is empty

#import socket module
import socket
import re
# create get_ip function
def get_ip(file):
# open file and read it, set to f
	with open(file, 'r') as f:
#loop through reading each line of f and set to line
		for line in f:
# lookup ip of the hostname from the read line
# set the line to the variable ip
			ip = socket.gethostbyname(line.strip())
#			print ip
#append hostnames to file
			e = open('output.xls','a')
			e.write(ip)
			e.write("\n")
			e.close()

# return the hostname and print it out
	#return name_only

# set hosts.txt document to files variable
files = 'hosts.txt'
#can i append it into the existing file?
#call get_hostname function with files variable
hosts = get_ip(files)
#print hosts

