N=500
head -n $N viwiki-latest-pages-articles.xml > viwiki-$N-lines.xml
input=viwiki-$N-lines.xml 
output=viwiki-$N-lines-cleaned 
perl wikifil-unicode.pl $input > $output
#echo $input; echo; head -c 500 $input; echo; echo; ls -lh $input; echo;
echo $output; echo; head -c 10000 $output; echo; echo; ls -lh $output; echo;
