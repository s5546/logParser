!/bin/sh
rm -rf tmp
mkdir tmp
cd tmp
for file in ../out/crashes/*
do
  ../scripts/fuzzparser06-19.py < "$file"
  read -p "<Press enter to continue>"
done
