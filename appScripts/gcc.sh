./gem5/build/X86/gem5.opt -d checkpoints/gccold2 gem5/configs/example/se.py --cpu-type=timing -I 590000000 --cmd=./apps/x86/spec/int/gcc/gcc --options="simpoint_apps/166.i" --checkpoint-dir=checkpoints/gccold2 --checkpoint-at-end 