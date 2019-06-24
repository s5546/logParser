rm -rf tmp
mkdir tmp
cd tmp
for file in ../out/*/crashes/*
do
  ../scripts/fuzzparser.py < "$file" 2> errors.txt
  read -p "<Press enter to continue>"
done
