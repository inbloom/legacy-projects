#!/bin/bash

DOCSERVER=style.slidev.org
DOCPATH=/var/www/storm/release_notes
DOCDIR=release_notes_6.3

if [ ! -e $DOCDIR ];
    then
        echo "Build doesn't exist. Run build.sh first.";
    else
        #if [ "$(ssh $DOCSERVER ls -A $DOCPATH/$DOCDIR)" ];
        #    then
        #        ssh $DOCSERVER rm -rf $DOCPATH/$DOCDIR
        #fi
        scp -r $DOCDIR $DOCSERVER:$DOCPATH/;
        echo "UPLOAD COMPLETE...";
fi
date

