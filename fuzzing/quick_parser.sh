!/bin/sh
for file in out/crashes/*
do
  scripts/fuzzparser.py < "$file"
  read -p "Press enter to continue"
done
