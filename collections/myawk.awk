#!/usr/bin/awk -f
BEGIN {
  num_task=0
  open=0
  num_commas_removed = 0
  num_commas = 0
}
#END {
#  print "num_tasks=" num_task
#  print "num_commas_removed=" num_commas_removed
#  print "num_commas=" num_commas
#}
# usalo con:
# for f in lp_interactive/*/*.yaml ; do ./myawk.awk $f > tmp ; mv tmp $f ; done;
{
    if($0 ~ /^- {/) {
	open=1
	++num_task
	print "- "num_task":"
    }
    else if($0 ~ /^  }/) {
	open=0
	print ""
    }
    else if($0 ~ /,$/) {
      ++num_commas
      if(open==1){
        ++num_commas_removed
        print substr($0, 1, length($0)-1)
      }
      else print
    }
    else print
}
