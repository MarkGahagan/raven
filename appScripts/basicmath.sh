./gem5/build/X86/gem5.opt -d checkpoints/basicmath gem5/configs/example/se.py --cpu-type=atomic --mem-type=SimpleMemory --cmd=./apps/x86/mibench/basicmath/basicmath_large --checkpoint-dir=checkpoints/basicmath -r 1 --caches -I 100000000
./gem5/build/X86/gem5.opt -d checkpoints/basicmath --stats-file=ooo.txt gem5/configs/example/se.py --cpu-type=detailed --mem-type=SimpleMemory --cmd=./apps/x86/mibench/basicmath/basicmath_large --checkpoint-dir=checkpoints/basicmath -r 1 --caches -I 100000000