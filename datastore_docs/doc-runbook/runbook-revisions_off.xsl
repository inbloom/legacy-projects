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
    <xsl:import href="../common/slc-pdf.xsl"/>
    
    <!-- Roles for styling and controlling revisions -->
    <xsl:template match="d:phrase[@role]">
        <xsl:choose>
            <xsl:when test="substring-after(@role,'-') = 'info'">
                <!-- Don't display the text at all -->
            </xsl:when>
            <xsl:when test="substring-after(@role,'-') = 'deleted'">
                <!-- Don't display the text at all -->
            </xsl:when>
            <xsl:otherwise>
                <fo:inline xsl:use-attribute-sets="normal.para.spacing">
                    <xsl:apply-templates/>
                </fo:inline>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
</xsl:stylesheet>
