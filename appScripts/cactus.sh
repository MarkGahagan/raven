./gem5/build/X86/gem5.opt -d checkpoints/cactusADM gem5/configs/example/se.py --simpoint-profile --simpoint-interval=100000000 --cpu-type=atomic --mem-type=SimpleMemory --fastmem --checkpoint-dir=checkpoints/cactusADM --cmd=./apps/x86/spec/fp/cactusADM/cactusADM --options="apps/x86/spec/fp/cactusADM/benchADM.par" -I 30000000000 

