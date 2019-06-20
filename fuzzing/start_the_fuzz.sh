tarname="out-$(date +%m-%d-%Y.%H-%M).tar.gz"
tar -czvf old_outs/$tarname out/*
rm -rf out
# gotta remove the tmp folder INSTEAD of the files inside
# rm gets caught on files otherwise, usually ones using `
rm -rf tmp 
mkdir tmp
cd tmp
py-afl-fuzz -i ../in -o ../out -m 250 python3 ../scripts/fuzzparser.py
