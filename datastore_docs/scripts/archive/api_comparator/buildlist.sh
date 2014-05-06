#!/bin/sh

#Builds a list of current endpoints for slc_rest_api_resources.xml
grep "<emphasis>https://" slc_rest_api_resources.xml >> temp.txt
echo Building list...
echo
sed -e 's/<[^>]*>//g' temp.txt >> temp2.txt
echo Removing tags...
echo
cat temp2.txt | sed 's/^[ \t]*//;s/[ \t]*$//' > endpoint_list.txt
echo Removing whitespace...
echo
rm temp*
echo Removing temporary files...
echo

#Compares the endpoint lists
./APIcompare.sh
