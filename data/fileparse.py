import os
import subprocess
import sys
import re
import time
import glob
from optparse import OptionParser, OptionGroup
from operator import itemgetter


def main(argv):
	list_of_files = glob.glob(sys.argv[2] + "_data/*.txt")

 	arch_list = []
	source = open( sys.argv[1], "r")
        for line in source:
		line2 = re.split(',', line)
                for x in range(0,len(line2)):
                     arch_list.append(line2[x])

	source.close()

	source = open( sys.argv[2] + "_data/stock.txt", "r" )
        for line in source:
                if "cpu.numCycles" in line:
                        line2 = re.split(' +', line)
                        stockTime = int(line2[1])


	source.close()
	output_filename = sys.argv[2] + '.out'
	out_file = open( output_filename, "w")
	for x in range(0, len(list_of_files)):
		temp_list = [4, 256, 32, 2, 128, 3, 1, 1, 0];
		source = open(list_of_files[x], "r")
		if "l1L" in list_of_files[x]:
			temp_list[2] = 64
			temp_list[3] = 4
		if "l1S" in list_of_files[x]:
			temp_list[2] = 16
		if "l2S" in list_of_files[x]:
			temp_list[1] = 64
		if "l2L" in list_of_files[x]:
			temp_list[1] = 1024
		if "oo8" in list_of_files[x]:
			temp_list[0] = 8
		if "io4" in list_of_files[x]:
			temp_list[8] = 1
			temp_list[4] = 0
		if "io2" in list_of_files[x]:
			temp_list[0] = 2
			temp_list[8] = 1
			temp_list[4] = 0
		if "io1" in list_of_files[x]:
			temp_list[0] = 1
			temp_list[8] = 1
			temp_list[4] = 0
		if "robS" in list_of_files[x]:
			temp_list[4] = 64
		if "robL" in list_of_files[x]:
			temp_list[4] = 200
		if "intL" in list_of_files[x]:
			temp_list[5] = 6
		if "intS" in list_of_files[x]:
			temp_list[5] = 1
		if "intMulL" in list_of_files[x]:
			temp_list[6] = 2
		if "fpL" in list_of_files[x]:
			temp_list[7] = 2
		if "fpS" in list_of_files[x]:
			temp_list[7] = 0
		print list_of_files[x]
		for line in source:
              	  if "numCycles" in line:
                        line2 = re.split(' +', line)
                        newTime = int(line2[1])
			newTime = float(stockTime)/float(newTime)
			newTime = round(newTime, 4)
			temp_list.append(newTime)
	
		
		source.close()
		outString=""
		for x in range(0, len(temp_list)):
			outString = outString + str(temp_list[x]) + ','

		for x in range(0, len(arch_list)):
			if x == len(arch_list)-1:
				outString = outString + arch_list[x] + '\n'
			else:
				outString = outString + arch_list[x] + ','
		out_file.write(outString)
	out_file.close()
		
	
		
main(sys.argv)
