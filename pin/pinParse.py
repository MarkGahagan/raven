import os
import subprocess
import sys
import re
import time
import glob
from optparse import OptionParser, OptionGroup
from operator import itemgetter


def main(argv):
	register_file = glob.glob(argv[1]+"/reg*.out")
	reuse_file = glob.glob(argv[1]+"/memr*.out")
	footprint_file = glob.glob(argv[1]+"/memf*.out")
	itypes_file = glob.glob(argv[1]+"/itypes_phases*.out")
        output_filename =  sys.argv[1] + '_' + sys.argv[2] + '.pinout'
	arch = [0,0,0,0,0,0,0,0,0,0,0,0]


	

	source = open( itypes_file[0], "r" )
	x = 0
	for line in source:
		if x == int(argv[2]):
			line2 = re.split(' +', line)	
			arch[0] = round((float(line2[4])+float(line2[7]))/float(line2[0]),4)
			arch[1] = round((float(line2[5])+float(line2[9]))/float(line2[0]),4)
			arch[2] = round(float(line2[3])/float(line2[0]),4)
			arch[3] = round((float(line2[1])+float(line2[2]))/float(line2[0]),4)
		x = x + 1
	source.close()

	source = open(footprint_file[0], "r" )
	x = 0
	for line in source:
		if x == int(argv[2]):
			line2 = re.split(' +', line)
			arch[4]=round((float(line2[0])*64.0)/1048576.0,4)	
			arch[5]=round((float(line2[2])*64.0)/1048576.0,4)	
		x = x + 1
	source.close()


	source = open( register_file[0], "r" )
	x = 0
	for line in source:
		if x == int(argv[2]):
			line2 = re.split(' +', line)	
			arch[6] = round(float(line2[3])/float(line2[2]),4)
			arch[7] = round((float(line2[5])*1.0+(float(line2[6])-float(line2[5]))*2.0+(float(line2[7])-float(line2[6]))*4.0+(float(line2[8])-float(line2[7]))*8.0+(float(line2[9])-float(line2[8]))*16.0+(float(line2[10])-float(line2[9]))*32.0+(float(line2[11])-float(line2[10]))*64.0+(float(line2[4])-float(line2[11]))*128.0)/1000000000.0, 4)
		x = x + 1

	source.close()
	source = open( reuse_file[0], "r" )
	x = 0
	for line in source:
		if x == int(argv[2]):
			line2 = re.split(' +', line)
			print line2
			arch[8] = round(((float(line2[2])*2.0)+(float(line2[3])*4.0)+(float(line2[4])*8.0)+(float(line2[5])*16.0)+(float(line2[6])*32.0)+(float(line2[7])*64.0)+(float(line2[8])*128.0)+(float(line2[9])*256.0)+(float(line2[10])*512.0)+(float(line2[11])*1024.0)+(float(line2[12])*2048.0)+(float(line2[13])*4096.0)+(float(line2[14])*8192.0)+(float(line2[15])*16384.0)+(float(line2[16])*32768.0)+(float(line2[17])*65536.0)+(float(line2[18])*131072.0)+(float(line2[19])*262144.0)+(float(line2[20])*524288.0))/(float(line2[0])*1000.0), 4)	
			arch[9] = round((float(line2[2])+float(line2[3])+float(line2[4])+float(line2[5])+float(line2[6]))/float(line2[0]),4)
			arch[10] = round((float(line2[17])+float(line2[18])+float(line2[19])+float(line2[20]))/float(line2[0]),4)
		x = x + 1


	source.close()


        writeFile = open(output_filename, "w")
	   
	writeFile.write( str(arch[0]) + ',' + str(arch[1])  + ','  + str(arch[2])  + ','  + str(arch[3])  + ','  + str(arch[4])  + ','  + str(arch[5])  + ','  + str(arch[6]) + ',' + str(arch[7]) + ',' + str(arch[8]) + ',' + str(arch[9]) + ',' + str(arch[10]))
        writeFile.close()
        cmd = ['mv', output_filename, '/home/mark/hydra/data/mibench/']
        subprocess.call(cmd)
        
main(sys.argv)
