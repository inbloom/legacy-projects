<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                xmlns:d="http://docbook.org/ns/docbook"
                xmlns:xlink='http://www.w3.org/1999/xlink'
                xmlns:suwl="http://nwalsh.com/xslt/ext/com.nwalsh.saxon.UnwrapLinks"
                version="1.0">

    <!-- Imports and includes -->
    <xsl:import href="../docbook/xsl/html/profile-docbook.xsl"/>
    <xsl:import href="../docbook/xsl/html/highlight.xsl"/>
    <xsl:import href="../docbook/xsl/oxygen_custom_html.xsl"/>
    <xsl:import href="../docbook/xsl/html/chunk-common.xsl"/>
    <xsl:import href="transform-html-templates-link.xsl"/>
    <xsl:import href="transform-html-templates-list.xsl"/>
    <xsl:include href="../docbook/xsl/html/profile-chunk-code.xsl"/>
    <xsl:include href="../docbook/xsl/html/manifest.xsl"/>
    
    <!-- Turn off admonition graphics -->
    <xsl:param name="admon.graphics" select="0"></xsl:param>
    
    <!-- Roles for styling and controlling revisions,
         remove anything marked as info or deleted when
         producing HTML; this is for FO/PDF only. -->
    <xsl:template match="d:phrase[@role]">
        <xsl:choose>
            <xsl:when test="substring-after(@role,'-') = 'info'">
                <!-- Don't display the text at all -->
            </xsl:when>
            <xsl:when test="substring-after(@role,'-') = 'deleted'">
                <!-- Don't display the text at all -->
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    
    <!-- Add a manifest file in the base directory alongside the HTML -->
    <xsl:param name="generate.manifest" select="1"></xsl:param>
    <xsl:param name="manifest.in.base.dir" select="1"></xsl:param>
    
    <!-- Turn off auto-generated numbers for parts, chapters, and sections. -->
    <xsl:param name="part.autolabel" select="0"/>
    <xsl:param name="chapter.autolabel" select="0"/>
    <xsl:param name="section.autolabel" select="0"/>
    <!-- Turn on auto-generated numbers for tables and figures. -->
    <xsl:param name="table.autolabel" select="1"/>
    <xsl:param name="figure.autolabel" select="1"/>
    
    <!-- Customize the automatic text for organizational elements. -->
    <xsl:param name="local.l10n.xml" select="document('')"/>
    <l:i18n xmlns:l="http://docbook.sourceforge.net/xmlns/l10n/1.0">
        <l:l10n language="en">
            <!-- Text used when the title element renders -->
            <l:context name="title">
                <l:template name="part" text="%t"/>
                <l:template name="chapter" text="%t"/>
                <l:template name="section" text="%t"/>
                <l:template name="figure" text="Figure %n. %t"/>
                <l:template name="table" text="Table %n. %t"/>
            </l:context>
            <!-- Text within the xref links to that element -->
            <l:context name="xref">
                <l:template name="part" text="%t"/>
                <l:template name="chapter" text="%t"/>
                <l:template name="section" text="%t"/>
                <l:template name="figure" text="Figure %n"/>
                <l:template name="table" text="Table %n"/>
            </l:context>
            <l:context name="xref-number">
                <l:template name="part" text="Part&#160;%n"/>
                <l:template name="chapter" text="Chapter&#160;%n"/>
                <l:template name="section" text="Section&#160;%n"/>
                <l:template name="figure" text="Figure&#160;%n"/>
                <l:template name="table" text="Table&#160;%n"/>
            </l:context>
            <l:context name="xref-number-and-title">
                <l:template name="part" text="Part&#160;%n, %t"/>
                <l:template name="chapter" text="Chapter&#160;%n, %t"/>
                <l:template name="section" text="Section&#160;%n, %t"/>
                <l:template name="figure" text="Figure&#160;%n"/>
                <l:template name="table" text="Table&#160;%n"/>
            </l:context>
            <!-- Numbering of xref links to that element, including in the ToC -->
            <l:context name="title-numbered">
                <l:template name="part" text=""/>
                <l:template name="chapter" text=""/>
                <l:template name="section" text=""/>
                <l:template name="table" text=""/>
                <l:template name="figure" text=""/>
            </l:context>
        </l:l10n>
    </l:i18n>
    
    <!-- Where to place numbers and titles for auto-numbered objects. -->
    <xsl:param name="formal.title.placement">
        figure before
        example before
        equation before
        table before
        procedure before
    </xsl:param>
    
    <!-- Set the default table width. -->
    <xsl:param name="default.table.width">100%</xsl:param>
    
    <!-- Allow programlisting and screen blocks to wrap text. -->
    <xsl:attribute-set name="monospace.verbatim.properties">
        <xsl:attribute name="wrap-option">wrap</xsl:attribute>
        <xsl:attribute name="hyphenation-character">\</xsl:attribute>
    </xsl:attribute-set>
    
    <!-- Default for simpleset.in.toc is 0, but we're stating it explicitly anyway -->
    <xsl:param name="simplesect.in.toc" select="0"></xsl:param>
      
    <!-- Customize chunking and cross-referencing within the HTML -->
    <xsl:param name="generate.id.attributes" select="1"/>
    <xsl:param name="use.id.as.filename" select="1"/>
    <xsl:param name="chunk.section.depth" select="0"/>
    <xsl:param name="chunk.quietly" select="1"/>
    <!-- Customize the Table of Contents generation. -->
    <xsl:param name="toc.section.depth">1</xsl:param>
    <xsl:param name="toc.max.depth">3</xsl:param>
    <xsl:param name="generate.toc">
        set       nop
        book      nop
        part      nop
        chapter   nop
        section   nop
        sect1     nop
    </xsl:param>

</xsl:stylesheet>
