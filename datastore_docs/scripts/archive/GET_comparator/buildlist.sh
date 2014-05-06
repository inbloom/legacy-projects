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

#Build a list of the current GET examples
grep "GET https://" slc_rest_api_resources.xml >> temp.txt
echo Building list...
echo
sed -e 's/<[^>]*>//g' temp.txt >> temp2.txt
sed -e 's/GET//' temp2.txt >> temp3.txt
echo Removing tags...
echo
cat temp3.txt | sed 's/^[ \t]*//;s/[ \t]*$//' > example_list.txt
echo Removing whitespace...
echo
cat example_list.txt | sed s/"localhost"/"example.com"/g >> temp_example_list.txt
mv temp_example_list.txt example_list.txt
cat example_list.txt | sed s/"placeholder_id"/"id"/g >> temp_example_list.txt
mv temp_example_list.txt example_list.txt
rm temp*
echo Removing temporary files...
echo

#Compares the endpoint lists
#./GETcompare.sh
