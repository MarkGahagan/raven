./gem5/build/X86/gem5.opt -d checkpoints/freqmine gem5/configs/example/se.py --cpu-type=atomic --mem-type=SimpleMemory --cmd=./apps/x86/parsec/freqmine/freqmine --options="apps/x86/parsec/freqmine/kosarak_500k.dat 410" --checkpoint-dir=checkpoints/freqmine -r 1 --caches -I 100000000
./gem5/build/X86/gem5.opt -d checkpoints/freqmine --stats-file=ooo.txt gem5/configs/example/se.py --cpu-type=detailed --mem-type=SimpleMemory --cmd=./apps/x86/parsec/freqmine/freqmine --options="apps/x86/parsec/freqmine/kosarak_500k.dat 410" --checkpoint-dir=checkpoints/freqmine -r 1 --caches -I 100000000