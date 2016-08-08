input=viwiki-latest-pages-articles.xml 
output=viwiki-cleaned
perl wikifil-vietnamese.pl $input > $output
echo $input; head -c 500 $input; echo; ls -lh $input; echo;
echo $output; head -c 100 $output; echo; ls -lh $output 
