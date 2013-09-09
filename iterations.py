# Assumes that the files are housed in a directory named "results"
# Also assumes that the files are contained in a folder based on the name of the directory you specify
# Makes additional assumptions on file names (due to previous scripts)
# Training set equations are equations.txt
# MICA Area/Power Data is mica.csv (equations will be designed in script)
# Arch-independent data ends with test.arc
# TODO: Knobs are static for now; make a more dynamic option later?

import os
import subprocess
import sys
import re
import time
from optparse import OptionParser, OptionGroup
from operator import itemgetter

class Knobs():
	ExecModel = [0, 1] 
	IntUnits = [1, 3, 6]
	IntMulUnits = [1, 2]
	FPUnits = [0, 1, 2]
	L1Size = [16, 32, 64]
	L1Assoc = [2, 4]
	L2Cache = [64, 256, 1024]
	ROBSize = [0, 64, 128, 200]
	IssueWidth = [1, 2, 4, 8]
	# Execution Model: 0 = Out-of-Order, 1 = In-order
	

class McPatData():
	Stock = 0
	FUStart_IO = 1
	FUStart_OoO = 4
	L1_I_Start = 7
	L1_D_Start = 10
	L2_Start = 13
	ROB_Start = 16
	Issue_Start_IO = 22
	Issue_Start_OoO = 24
	AP_Data = []
	


def main(argv):
	parser = setUp_options()
	(options, arg) = parser.parse_args()
	knobs = Knobs()
	MPData = McPatData()
	ArchData = archInd_Parse(options)
	AP_Data = mcPat_Parse(options, ArchData)
	ResultMatrix = []
	ResultMatrix = ComputeResultMatrix(MPData, knobs, ArchData, AP_Data, options)	
	
	Processors = ProcessorSelection(ResultMatrix)
	#for x in range(0,len(Processors)):	
	#	print str(Processors[x])


def ProcessorSelection(ResultMatrix):
	Processors = []
	temp = []
	for x in range(0,len(ResultMatrix)):
		for y in range(0,len(ResultMatrix[x])):
			temp = ResultMatrix[x][y][0]*ResultMatrix[x][y][4]
			ResultMatrix[x][y].append(temp)
		ResultMatrix[x] = sorted(ResultMatrix[x], key=itemgetter(14), reverse=True)
		temp = ResultMatrix[x][0]
                print temp
		for y in range(1,10):
			temp.append(ResultMatrix[x][y])
		Processors.append(temp)
		temp = []
	for y in range(0, len(ResultMatrix)):
		print "Cluster " + str(y) + '\n\n'
		for x in range(0,20):
		        print ResultMatrix[y][x]	
	return Processors

def PerfComp(KnobSettings, ArchData):
	#TODO: Automate collection of regression
	RegDataInt = []
	RegDataInt.append([0.136, 7, False, True, True, True])
	RegDataInt.append([0.1835, 7, False, False, True, True])
	RegDataInt.append([0.2329, 7, False, False, False, True])
	RegDataInt.append([0.0306, 0, False, True, True])
	RegDataInt.append([-0.0664, 0, True, True , False])
	RegDataInt.append([-0.0292, 1, False, True, True])
	RegDataInt.append([-0.0305, 1, True, False, False])
	RegDataInt.append([-0.0355, 2, True, False])
	RegDataInt.append([0.194, 3, False, True, True, True])
	RegDataInt.append([0.0622, 3, False, False, True, True])
	RegDataInt.append([-0.0992, 3, False, False, True, False])
	RegDataInt.append([-0.031, 4, False, True, True])
	RegDataInt.append([0.3068, 4, False, False, True])
	RegDataInt.append([0.0223, 5, False, True])
	RegDataInt.append([0, 6, False, True, True])
	RegDataInt.append([0, 6, False, False, True])
	RegDataInt.append([0.3645, 8, True, False])
	RegDataInt.append([-0.02, 8, False, True])
	RegDataInt.append([0.002*ArchData[8], 8, False, True])
	RegDataInt.append([0.8546, 9])
	RegDataInt.append([0, 10])
	RegDataInt.append([0, 11])
	RegDataInt.append([-0.2981, 12])
	RegDataInt.append([0.0005, 13])
	RegDataInt.append([0, 14])
	RegDataInt.append([0, 15])
	RegDataInt.append([0.0114, 16])
	RegDataInt.append([0, 17])
	RegDataInt.append([0.1634, 18])
	RegDataInt.append([0, 19])
	RegDataInt.append(-0.2912)
	performance = 0
	for x in range(0, len(RegDataInt)):
		if len(RegDataInt)-x == 1:
			perform3ance = performance + RegDataInt[x]
		else:
			if RegDataInt[x][1] > 8:
				performance = performance + (RegDataInt[x][0] * ArchData[RegDataInt[x][1]-9])
			else: 
				if RegDataInt[x][KnobSettings[RegDataInt[x][1]]+2]: 
			   		performance = performance + RegDataInt[x][0]
	RegDataFP = []
	RegDataFP.append([0.1178, 7, False, True, True, True])
	RegDataFP.append([0.2051, 7, False, False, True, True])
	RegDataFP.append([0.2887, 7, False, False, False, True])
	RegDataFP.append([0.0306, 0, False, True, True])
	RegDataFP.append([-0.0229, 0, False, True , False])
	RegDataFP.append([0.0176, 1, False, True, True])
	RegDataFP.append([-0.0229, 1, True, False, False])
	RegDataFP.append([-0.0319, 2, True, False])
	RegDataFP.append([0.0944, 3, False, True, True, True])
	RegDataFP.append([0.0519, 3, False, False, True, True])
	RegDataFP.append([-0.0207, 3, False, False, True, False])
	RegDataFP.append([0, 4, False, True, True])
	RegDataFP.append([0, 4, False, False, True])
	RegDataFP.append([0, 5, False, True])
	RegDataFP.append([0.2437, 6, False, True, True])
	RegDataFP.append([0.0385, 6, False, False, True])
	RegDataFP.append([0.3611, 8, True, False])
	RegDataFP.append([-0.02, 8, False, True])
	RegDataFP.append([0.002*ArchData[8], 8, False, True])
	RegDataFP.append([0, 9])
	RegDataFP.append([-0.6868, 10])
	RegDataFP.append([0, 11])
	RegDataFP.append([-0.741, 12])
	RegDataFP.append([0.0009, 13])
	RegDataFP.append([0, 14])
	RegDataFP.append([0, 15])
	RegDataFP.append([0.0303, 16])
	RegDataFP.append([0, 17])
	RegDataFP.append([0.6089, 18])
	RegDataFP.append([0, 19])
	RegDataFP.append(-0.3677)
	performanceFP = 0
	for x in range(0, len(RegDataFP)):
		if len(RegDataFP)-x == 1:
			performanceFP = performanceFP + RegDataFP[x]
		else:
			if RegDataFP[x][1] > 8:
				performanceFP = performanceFP + (RegDataFP[x][0] * ArchData[RegDataFP[x][1]-9])
			else: 
				if RegDataFP[x][KnobSettings[RegDataFP[x][1]]+2]: 
			   		performanceFP = performanceFP + RegDataFP[x][0]	
	
	performance = (1-ArchData[1])*performance - (max((1-ArchData[1]), 0))*(RegDataFP[14][0]) + (min((ArchData[1]*12), 1))*performanceFP
	return performance



def archInd_Parse(options):
	ArchData = []
	temp = []
	arch_file = options.pdir + '/' + options.program + '/test.arc'
	source = open( arch_file, "r" )
	for line in source:
		line_arr = re.split(',',line)
		for x in range(0, len(line_arr)):
			temp.append(float(line_arr[x]))
		ArchData.append(temp)
		temp = []
	return ArchData



# Outputs McPat Data to a file then gets power/area tuple
def mcPat_Parse(options, ArchData):
	AP_Data = []	
	temp = 0;
	mcPat_file = options.pdir + '/' + options.program + '/mica.csv'
	source = open( mcPat_file, "r" )
	for line in source:
		line_arr = re.split(',',line)
		if len(line_arr) == 2:
			AP_Data.append([float(line_arr[0]), float(line_arr[1])])
		else:
			AP_Data.append([float(line_arr[0]), float(line_arr[1]), float(line_arr[2]), float(line_arr[3])])
	source.close()
	return AP_Data	








def APComp (AP_Data, Knobs, ArchData, MPData):
	power = AP_Data[MPData.Stock][1]
	area = AP_Data[MPData.Stock][0]

	# Adding Functional Units
	if Knobs[0] == 1:
		for x in range(0, 3):
			if x == 2:
			   y = ArchData[1]
                        else:
                           y = ArchData[0]+ArchData[2]
	    		power = power + Knobs[x+1]*((AP_Data[MPData.FUStart_IO+x][1])+AP_Data[MPData.FUStart_IO+x][2]+AP_Data[MPData.FUStart_IO+x][3])
			area = area + Knobs[x+1]*(AP_Data[MPData.FUStart_IO+x][0])
	else:
		for x in range(0, 3):
			if x == 2:
			   y = ArchData[1]
                        else:
                           y = ArchData[0]+ArchData[2]
			power = power + Knobs[x+1]*((AP_Data[MPData.FUStart_OoO+x][1])+AP_Data[MPData.FUStart_OoO+x][2]+AP_Data[MPData.FUStart_OoO+x][3])
			area = area + Knobs[x+1]*(AP_Data[MPData.FUStart_OoO+x][0])
	
	# Adding L1 Cache
	power = power + AP_Data[MPData.L1_I_Start+Knobs[4]][1] + AP_Data[MPData.L1_I_Start+Knobs[4]][2] + AP_Data[MPData.L1_I_Start+Knobs[4]][3]
	area = area + AP_Data[MPData.L1_I_Start+Knobs[4]][0]
	power = power + AP_Data[MPData.L1_D_Start+Knobs[4]][1] + AP_Data[MPData.L1_D_Start+Knobs[4]][2] + AP_Data[MPData.L1_D_Start+Knobs[4]][3]
	area = area + AP_Data[MPData.L1_D_Start+Knobs[4]][0]

	# Adding L2 Cache
	power = power + AP_Data[MPData.L2_Start+Knobs[5]][1] + AP_Data[MPData.L2_Start+Knobs[5]][2] + AP_Data[MPData.L2_Start+Knobs[5]][3]
	area = area + AP_Data[MPData.L2_Start+Knobs[5]][0]
	# Adding RoB
	if Knobs[0] == 0:
		if Knobs[7] == 3:
			setup = MPData.ROB_Start + 2
		else:
			setup = MPData.ROB_Start -1
		power = power + AP_Data[setup+Knobs[6]][1] + AP_Data[setup+Knobs[6]][2] + AP_Data[setup+Knobs[6]][3]
		area = area + AP_Data[setup+Knobs[6]][0] 
	# Adding issue width

	if Knobs[0] == 0:
		Issues = MPData.Issue_Start_OoO
	elif Knobs[0] == 1:
		Issues = MPData.Issue_Start_IO
 	if Knobs[7] > 0: 
		for x in range(0, Knobs[7]):
			power = power + AP_Data[Issues+x][1] + AP_Data[Issues+x][2] + AP_Data[Issues+x][3]
			area = area + AP_Data[Issues+x][0] 
	return (power, area)





def ComputeResultMatrix(MPData, knobs, ArchData, AP_Data, options):	
   ResultMatrix = []
   AppMatrix = []
   for x in range(0, len(ArchData)):
      (normalizedPower, normalizedArea) = APComp(AP_Data,[0,3,1,1,1,1,2,2] , ArchData[x], MPData) 
      for a in range(0, len(knobs.L2Cache)):
         for b in range (0, len(knobs.L1Size)):
	    for i in range(0, len(knobs.ExecModel)):
	       (issueMin, issueMax, ROBSizeMin, ROBSizeMax) = issueSetup(knobs, i)
               for g in range(issueMin, issueMax+1):
                  (xInt, yInt, xMul, yMul, xFP, yFP) = FUSetup(knobs, knobs.IssueWidth[g])
                  for d in range (xInt, yInt):
                     for e in range (xMul, yMul):
                        for f in range (xFP, yFP):			
			   for c in range (ROBSizeMin, ROBSizeMax): 
			       if b == 2:
				 h = 1
			       else:
                                 h = 0
                               KnobSettings = [knobs.L2Cache[a], knobs.L1Size[b], knobs.L1Assoc[h], knobs.ROBSize[c], knobs.IntUnits[d], knobs.IntMulUnits[e], knobs.FPUnits[f], knobs.IssueWidth[g], knobs.ExecModel[i]]
			       TupleSettings = [KnobSettings[8], KnobSettings[4], KnobSettings[5], KnobSettings[6], b, a, c, g]
	                       (powerTuple, areaTuple) = APComp(AP_Data, TupleSettings, ArchData[x], MPData)
                               performanceTuple = PerfComp([a,b,h,c,d,e,f,g,i], ArchData[x])

			       AppMatrix.append([performanceTuple, areaTuple, powerTuple, areaTuple/normalizedArea, normalizedPower/powerTuple, KnobSettings[0], KnobSettings[1], KnobSettings[2], KnobSettings[3], KnobSettings[4], KnobSettings[5],KnobSettings[6],KnobSettings[7],KnobSettings[8]])
                               
      ResultMatrix.append(AppMatrix)
      AppMatrix = []
   return ResultMatrix



def issueSetup (knobs, execmodel):
	iMin = 0
        iMax = 2
        ROBSizeMax = 1
	ROBSizeMin = 0
	if execmodel == 0:
		iMin = 2
		iMax = 3
		ROBSizeMin = 1
		ROBSizeMax = len(knobs.ROBSize)
	return (iMin, iMax, ROBSizeMin, ROBSizeMax)


def FUSetup (knobs, issueWidth):
	xint = 0
	yint = 0
	xmul = 0
	ymul = 0
	xfp = 0
	yfp = 0
	if issueWidth == 1:
	   xint = 0
           yint = 1
        elif issueWidth == 2:
	   xint = 0
           yint = 2
        elif issueWidth == 4:
           xint = 1
           yint = 2
        elif issueWidth == 8:
           xint = 2
           yint = 3
	#for a in range(0, len(knobs.IntUnits)):
	#	if(knobs.IntUnits[a]):
	#		xint = xint + 1
	#	if(knobs.IntUnits[a] <= issuewidth+1):
	#		yint = yint + 1
	for a in range(0, len(knobs.IntMulUnits)):
		#if(knobs.IntMulUnits[a] < issuewidth/8):
		#	xmul++
		if(knobs.IntMulUnits[a] <= issueWidth):
			ymul = ymul + 1
	for a in range(0, len(knobs.FPUnits)):
		#if(knobs.FPUnits[a] < issuewidth/8):
		#	xfp++
		if(knobs.FPUnits[a] <= issueWidth):
			yfp = yfp + 1
	return (xint, yint, xmul, ymul, xfp, yfp)

def setUp_options():
	parser = OptionParser()
	parser.add_option("-p", "--program", type="string", default="test", help="Folder you wish to analyze data from")
	parser.add_option("--pdir", type="string", default="results", help="Location of Program")
	group = OptionGroup(parser, "Gem5 Options")
	group.add_option("--wekadir", type="string", default="weka/", help="Base Directory of weka application (end with a '/')")
	parser.add_option_group(group)

	return parser

main(sys.argv)
	
