<?xml version="1.0" encoding="UTF-8"?>

<!DOCTYPE book [
<!ENTITY % entities SYSTEM "../common/entities.ent">
%entities;
]>

<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:d="http://docbook.org/ns/docbook"
    xmlns:ns="http://docbook.org/ns/docbook"
    exclude-result-prefixes="d"
    xmlns:fo="http://www.w3.org/1999/XSL/Format"
    version="1.0">
    
    <!-- Import the main PDF styling.... -->
    <xsl:import href="inbloom-pdf.xsl"/>
    
    <!-- ... and then turn on DRAFT MODE -->
    <xsl:param name="draft.mode">yes</xsl:param>
    <xsl:param name="draft.watermark.image">../common/images/draft.png</xsl:param>
    
</xsl:stylesheet>
