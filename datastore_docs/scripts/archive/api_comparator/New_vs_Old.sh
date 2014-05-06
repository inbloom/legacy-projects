#!/bin/bash

FILE1=endpoint_list.txt
FILE2=endpoint_list_old.txt
FILE3=api_changes.txt

echo Searching for new or changed endpoints in the current version of the API...
while read line; do
  if grep $line $FILE2 >> temp.txt; then
    continue
  else
    echo $line >> ADDED_or_CHANGED.txt
  fi
done < $FILE1


FILE2=endpoint_list.txt
FILE1=endpoint_list_old.txt

echo Searching for deleted or changed endpoints from the older version of the API...
while read line; do
  if grep $line $FILE2 >> temp.txt; then
    continue
  else
    echo $line >> DELETED_or_CHANGED.txt
  fi
done < $FILE1

echo Finished comparing files...
echo
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++   >> $FILE3
echo The following endpoints have either been added or changed: >> $FILE3
cat ADDED_or_CHANGED.txt >> $FILE3
echo >> $FILE3
echo >> $FILE3
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++   >> $FILE3
echo The following endpoints have either been added or changed: >> $FILE3
cat DELETED_or_CHANGED.txt >> $FILE3
echo >> $FILE3
echo >> $FILE3
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++   >> $FILE3

echo Removing temporary files...
rm temp.txt
rm DELETED_or_CHANGED.txt
rm ADDED_or_CHANGED.txt

echo COMPLETE!
echo
cat $FILE3
echo
echo
