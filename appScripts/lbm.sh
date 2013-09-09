./gem5/build/X86/gem5.opt -d checkpoints/lbm gem5/configs/example/se.py --cpu-type=atomic --mem-type=SimpleMemory --fastmem --checkpoint-dir=checkpoints/lbm --cmd=./apps/x86/spec/fp/lbm/lbm --options="3000 apps/x86/spec/fp/lbm/reference.dat 0 0 apps/x86/spec/fp/lbm/100_100_130_ldc.of" -I 700000000 --checkpoint-at-end

