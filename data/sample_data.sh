input="enwik8"
size_mb=1
num_bytes=$(($size_mb * 1024 * 1024))
output=$input"-"$size_mb"mb"
echo $output
head -c $num_bytes $input >> $output
