# Read the line of a file for an ip
# Run snmpwalk on that ip with public community string
# must have snmpwalk installed on host system
# Output data to new file
# Repeat till end of file
# ToDo: make my own snmpwalk python script removing dependency on snmpwalk
import subprocess
import sys
import os.path
import argparse

#set parser
parser = argparse.ArgumentParser()
#add file arguments to parser
parser.add_argument('ip_file', help='The file containing your ips')
parser.add_argument('-c', '--community', help='Provide the community string you want to use, otherwise it is set to public by default.', dest='community_string')
parser.add_argument('-v', '--version', help='Provide the version number of snmp, if none supplied default is 1', dest='version_num')
#set args variable
args = parser.parse_args()
#set host variable to the value in the host_address arg
ip_list = args.ip_file
community = args.community_string
version = args.version_num

#check if arguments have values, if not then provide help message and quit
if args.ip_file is None:
    parser.print_help()
    quit()

#if community string is empty set it to public
if args.community_string is None:
	community = 'public'

#if version string is empty set it to 1
if args.version_num is None:
	version = '1'

# create snmp_walk function
def snmp_walk(ip_list):
# open file and read it, set to f
	with open(ip_list, 'r') as f:
#loop through reading each line of f and set to line
		for line in f:
# run snmpwalk and set snmpwalk standard output to proc variable 
			line = line.strip()
# Next four ommented lines are for debugging.
			#print line
			#print "snmpwalk", "-c", "public", "-v", "1", line
			#Use next line to do debugging with a much faster and smaller data set.
			#proc = subprocess.Popen(["snmpwalk", "-CE", "iso.3.6.1.2.1.1.8.0", "-c", "public", "-v", "1", line], stdout=subprocess.PIPE)
			proc = subprocess.Popen(["snmpwalk", "-c", community, "-v", version, line], stdout=subprocess.PIPE)
#read the standard output and set it to output variable
			#print proc
			output = proc.stdout.read()
			#print output
			#add data to file
			e = open('snmp_%s' % line, 'w')
			e.write(output)
			e.close()


try:	
	snmp_walk(ip_list)
except IOError:
	print """Please create a file named ips for this script to reference. Each line should be a unique ip that has the public community string for snmp. You can edit this script to use different community strings or arguments."""
