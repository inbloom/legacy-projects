<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:d="http://docbook.org/ns/docbook"
    xmlns:ns="http://docbook.org/ns/docbook"
    exclude-result-prefixes="d"
    xmlns:fo="http://www.w3.org/1999/XSL/Format"
    version="1.0">
    <xsl:import href="../common/inbloom-pdf.xsl"/>
    
    <!-- Roles for styling and controlling revisions within phrase elements -->
    <xsl:template match="d:phrase[@role]">
        <xsl:choose>
            <xsl:when test="substring-after(@role,'-') = 'info'">
                <!-- Don't display the text at all -->
            </xsl:when>
            <xsl:when test="contains(@role,'html')">
                <!-- Don't display the text at all -->
            </xsl:when>
            <xsl:when test="substring-after(@role,'-') = 'deleted'">
                <!-- Don't display the text at all -->
            </xsl:when>
            <xsl:when test="@role = 'html'">
                <!-- Don't display the text at all -->
            </xsl:when>
            <xsl:otherwise>
                <fo:inline xsl:use-attribute-sets="normal.para.spacing">
                    <xsl:apply-templates/>
                </fo:inline>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <!-- Roles for styling and controlling revisions within paragraph elements -->
    <xsl:template match="d:para[@role]">
        <xsl:variable name="keep.together">
            <xsl:call-template name="pi.dbfo_keep-together"/>
        </xsl:variable>
        <xsl:choose>
            <xsl:when test="substring-after(@role,'-') = 'info'">
                <!-- Don't display the text at all -->
            </xsl:when>
            <xsl:when test="substring-after(@role,'-') = 'deleted'">
                <!-- Don't display the text at all -->
            </xsl:when>
            <xsl:when test="@role = 'html'">
                <!-- Don't display the text at all -->
            </xsl:when>
            <xsl:otherwise>
                <fo:block xsl:use-attribute-sets="para.properties">
                    <xsl:if test="$keep.together != ''">
                        <xsl:attribute name="keep-together.within-column"><xsl:value-of
                            select="$keep.together"/></xsl:attribute>
                    </xsl:if>
                    <xsl:call-template name="anchor"/>
                    <xsl:apply-templates/>
                </fo:block>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
</xsl:stylesheet>
