#!/bin/bash

DOCSERVER=style.slidev.org
DOCPATH=/var/www/storm/release_notes
DOCDIR=Alpha.1_Release_Notes

if [ ! -e $DOCDIR ];
    then
        echo "Build doesn't exist. Run build.sh first.";
    else
        if [ "$(ssh $DOCSERVER ls -A $DOCPATH/$DOCDIR)" ];
            then
                ssh $DOCSERVER rm -rf $DOCPATH/$DOCDIR
        fi
        scp -r $DOCDIR $DOCSERVER:$DOCPATH/;
        echo "UPLOAD COMPLETE...";
fi
date

