import os
import subprocess
import sys
import re
import time
import glob
from optparse import OptionParser, OptionGroup
from operator import itemgetter


def main(argv):
	list_of_files = glob.glob(sys.argv[1] + "/*.txt")
	final_list = []

	source = open( sys.argv[1] + "/stock.txt", "r" )
        for line in source:
                if "cpu.numCycles" in line:
                        line2 = re.split(' +', line)
                        stockTime = int(line2[1])


	source.close()
	output_filename = sys.argv[1] + sys.argv[2] + '.out'
	out_file = open( output_filename, "w")
	for x in range(0, len(list_of_files)):
		temp_list = ['stock']
		power = 1
		source = open(list_of_files[x], "r")
		if "big" in list_of_files[x]:
			temp_list[0] = 'big'
			power = float(argv[3])/9.9824
		if "little" in list_of_files[x]:
			temp_list[0] = 'little'
			power = float(argv[3])/3.85
		if "ravan" in list_of_files[x]:
			temp_list[0] = 'Raven'
			power = float(argv[3])/float(argv[4])
		if "max" in list_of_files[x]:
			temp_list[0] = '8-OoO'
			power = float(argv[3])/16.57
		if "min" in list_of_files[x]:
			temp_list[0] = '1-IO'
			power = float(argv[3])/1.74
		for line in source:
              	  if "numCycles" in line:
                        line2 = re.split(' +', line)
                        newTime = int(line2[1])
			if "-w" in sys.argv[2]: 
				newTime = int(newTime)
			elif "-is" in sys.argv[2]:
				newTime = float(newTime)/float(stockTime)
				newTime = round(newTime, 4)
			elif "-s" in sys.argv[2]:
				newTime = float(stockTime)/float(newTime)
				newTime = round(newTime, 4)
			elif "-e" in sys.argv[2]:
				newTime = float(stockTime)/float(newTime)
				newTime = round(newTime*power, 4)
			temp_list.append(newTime)
	
		
		source.close()
		final_list.append(temp_list)
		temp_list = []



	outString=""
	for x in range(0, len(final_list[0])):
		if x == 0:
		    outString = outString + 'App\t'
		if x == 1:
		    outString = outString + argv[1] + '\t'
		for y in range(0, len(final_list)):
			outString = outString + str(final_list[y][x]) + '\t'
		outString = outString + ' \n'

		
	out_file.write(outString)
	out_file.close()
		
	
		
main(sys.argv)
