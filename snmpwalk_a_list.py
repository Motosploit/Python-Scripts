# Read the line of a file for an ip
# Run snmpwalk on that ip with public community string
# Output data to new file
# Repeat till end of file
import subprocess
import sys
import os.path

# create snmp_data function
def snmp_walk(file):
# open file and read it, set to f
	with open(file, 'r') as f:
#loop through reading each line of f and set to line
		for line in f:
# run snmpwalk and set snmpwalk standard output to proc variable 
			line = line.strip()
# Next four ommented lines are for debugging.
			#print line
			#print "snmpwalk", "-c", "public", "-v", "1", line
			#Use next line to do debugging with a much faster and smaller data set.
			#proc = subprocess.Popen(["snmpwalk", "-CE", "iso.3.6.1.2.1.1.8.0", "-c", "public", "-v", "1", line], stdout=subprocess.PIPE)
			proc = subprocess.Popen(["snmpwalk", "-c", "public", "-v", "1", line], stdout=subprocess.PIPE)
#read the standard output and set it to output variable
			#print proc
			output = proc.stdout.read()
			#print output
			#add data to file
			e = open('snmp_%s' % line, 'w')
			e.write(output)
			e.close()


try:
	file = 'ips'	
	snmp_walk(file)
except IOError:
	print """Please create a file named ips for this script to reference. Each line should be a unique ip that has the public community string for snmp. You can edit this script to use different community strings or arguments."""
