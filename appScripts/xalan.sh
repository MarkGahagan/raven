./gem5/build/X86/gem5.opt -d checkpoints/xalan gem5/configs/example/se.py --cpu-type=atomic --mem-type=SimpleMemory --caches -I $1 --cmd=./apps/x86/spec/int/xalan/Xalan --options="-v apps/x86/spec/int/xalan/t5.xml apps/x86/spec/int/xalan/xalanc.xsl" --checkpoint-dir=checkpoints/xalan --checkpoint-at-end
