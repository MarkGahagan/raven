./gem5/build/X86/gem5.opt -d checkpoints/libquantum gem5/configs/example/se.py --cpu-type=atomic --mem-type=SimpleMemory --checkpoint-dir=checkpoints/libquantum --cmd=./apps/x86/spec/int/libquantum/libquantum --options="1397 8" --caches -I $1 --checkpoint-at-end 