#/bin/bash

DOCNAME=release_notes
RELEASE=Alpha.0

echo "Converting $RALLYDEFECTS...";
xsltproc --xinclude -o rally_defects.xml ../rally_defects_to_docbook.xsl rally_defects-raw.xml
echo "Converting $RALLYSTORIES...";
xsltproc --xinclude -o rally_stories.xml ../rally_stories_to_docbook.xsl rally_stories-raw.xml
echo "Building document $DOCNAME...";
xsltproc --xinclude -o $DOCNAME-$RELEASE.html ../../common/slc-html-onepage.xsl $DOCNAME.xml
echo "HTML build complete: $DOCNAME-$RELEASE.html"
