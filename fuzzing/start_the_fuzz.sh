cd tmp
rm -rf *
py-afl-fuzz -i ../in -o ../out -m 250 python3 ../scripts/fuzzparser.py
