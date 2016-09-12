input="enwik8-cleaned"
size_mb=10
num_bytes=$(($size_mb * 1024 * 1024))
output=$input"-"$size_mb"mb"
echo $output
head -c $num_bytes $input >> $output
