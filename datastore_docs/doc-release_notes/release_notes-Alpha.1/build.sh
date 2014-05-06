#/bin/bash

DOCNAME=release_notes
RELEASE=Alpha.2
TARGETDIR=Alpha.2_Release_Notes

echo "Converting rally_resolved_defects-raw.xml...";
xsltproc --xinclude -o rally_resolved_defects.xml ../rally_resolved_defects_to_docbook.xsl rally_resolved_defects-raw.xml
echo "Converting rally_defects-raw.xml...";
xsltproc --xinclude -o rally_defects.xml ../rally_defects_to_docbook.xsl rally_defects-raw.xml
echo "Converting rally_stories-raw.xml...";
xsltproc --xinclude -o rally_stories.xml ../rally_stories_to_docbook.xsl rally_stories-raw.xml
echo "Building end-user release notes...";
xsltproc --xinclude -o user-$DOCNAME-$RELEASE.html ../../common/slc-html-onepage.xsl user_$DOCNAME.xml
echo "HTML build complete: user-$DOCNAME-$RELEASE.html"

echo "Converting rally_op_resolved_defects.xml...";
xsltproc --xinclude -o rally_op_resolved_defects.xml ../rally_resolved_defects_to_docbook.xsl rally_op_resolved_defects-raw.xml
echo "Converting rally_op_defect.xml...";
xsltproc --xinclude -o rally_op_defects.xml ../rally_defects_to_docbook.xsl rally_op_defects-raw.xml
echo "Building operator release notes...";
xsltproc --xinclude -o operator-$DOCNAME-$RELEASE.html ../../common/slc-html-onepage.xsl operator_$DOCNAME.xml
echo "HTML build complete: operator-$DOCNAME-$RELEASE.html"

echo "Packaging release notes"
mkdir $TARGETDIR
mv "user-$DOCNAME-$RELEASE.html" $TARGETDIR/
mv "operator-$DOCNAME-$RELEASE.html" $TARGETDIR/
cp -r ../../common/css $TARGETDIR/
mkdir $TARGETDIR/images
cp ../../common/images/slcheader_960.png $TARGETDIR/images/
echo "Release notes build complete"
date

