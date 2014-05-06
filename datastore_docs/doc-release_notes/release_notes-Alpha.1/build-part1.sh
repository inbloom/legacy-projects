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

echo "Converting rally_op_resolved_defects.xml...";
xsltproc --xinclude -o rally_op_resolved_defects.xml ../rally_resolved_defects_to_docbook.xsl rally_op_resolved_defects-raw.xml
echo "Converting rally_op_defect.xml...";
xsltproc --xinclude -o rally_op_defects.xml ../rally_defects_to_docbook.xsl rally_op_defects-raw.xml

echo "Release notes conversions complete"
date

