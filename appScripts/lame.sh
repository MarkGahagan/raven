./gem5/build/X86/gem5.opt -d results/lamex86 gem5/configs/example/se.py --simpoint-profile --simpoint-interval=100000000 --cpu-type=atomic --mem-type=SimpleMemory --fastmem -I 30000000000 --cmd=./apps/x86/mibench/lame3.70/lame --options="apps/x86/mibench/large.wav apps/x86/mibench/output_large.mp3"