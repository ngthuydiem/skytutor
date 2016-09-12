input=enwik8 # enwik8 enwik9 (frwiki,enwiki)viwiki-latest-pages-articles.xml 
output=enwik8-cleaned # enwik8-cleaned enwik9-cleaned (frwiki,enwiki)viwiki-cleaned
perl wikifil.pl $input > $output
echo $input; head -c 500 $input; echo; ls -lh $input; echo;
echo $output; head -c 100 $output; echo; ls -lh $output 
