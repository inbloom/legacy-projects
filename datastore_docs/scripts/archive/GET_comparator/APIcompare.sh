#!/bin/sh

# Comparing the new list of endpoints with the previous version of the API
if diff endpoint_list.txt example_list.txt  >/dev/null ; then
  echo The versions of the API being compared are identical. Have a nice day!
  echo
else
  echo The versions of the API being compared are different. 
  echo See ADDED_or_CHANGED_in_new_version.txt and/or DELETED_or_CHANGED_from_old_version.txt for further details.
  echo
fi

