tarname="out-$(date +%m-%d-%Y.%H-%M).tar.gz"
tar -czvf old_outs/$tarname out/*
rm -rf out
# gotta remove the tmp folder INSTEAD of the files inside
# rm gets caught on files otherwise, usually ones using ` or -
rm -rf tmp
mkdir tmp
cd tmp
gnome-terminal -x py-afl-fuzz -i ../in -o ../out -m 250 -M fuzzer1 python3 ../scripts/fuzzparser.py
cores=$(grep -c ^processor /proc/cpuinfo)
for (( c=1; c<=$cores; c++ ))
do
	echo -e "Waiting 10 seconds to launch next fuzzer...\n$c/$cores\n" #timeout COULD be lower but it fails if it's too low, and an extra 5 sec per core is nbd for how long AFL takes
	sleep 10
	gnome-terminal -x py-afl-fuzz -i ../in -o ../out -m 250 -S fuzzer$c python3 ../scripts/fuzzparser.py #-x is apparently depricated
done

echo "Waiting 10 seconds for all fuzzers to start..."
sleep 10 #unneeded, but afl-whatsup misses the last fuzzer otherwise
while true
do
	clear
	echo -e "Press [CTRL+C] to exit...\n(fuzzers will remain active)"
	pwd
	afl-whatsup ../out
	for i in {30..0..-1}
	do
		echo -en "\r$i seconds until update..."
		sleep 1
	done
done
