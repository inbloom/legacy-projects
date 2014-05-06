<?xml version="1.0" encoding="UTF-8"?>

<!DOCTYPE book [
<!ENTITY % entities SYSTEM "../common/entities.ent">
<!ENTITY % dynamic SYSTEM "../common/dynamic.ent">
%entities;
%dynamic;
]>

<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:d="http://docbook.org/ns/docbook"
    xmlns:ns="http://docbook.org/ns/docbook"
    exclude-result-prefixes="d"
    xmlns:xlink='http://www.w3.org/1999/xlink'
    xmlns:suwl="http://nwalsh.com/xslt/ext/com.nwalsh.saxon.UnwrapLinks"
    version="1.0">

    <xsl:import href="&LOCALDOCBOOKXSL;/html/profile-docbook.xsl"/>
    <xsl:import href="&LOCALDOCBOOKXSL;/html/highlight.xsl"/>
    <xsl:import href="&LOCALDOCBOOKXSL;/html/chunk-common.xsl"/>
    <xsl:import href="inbloom-html-templates-link.xsl"/>
    <xsl:import href="inbloom-html-templates-list.xsl"/>
    <xsl:include href="&LOCALDOCBOOKXSL;/html/profile-chunk-code.xsl"/>
    <xsl:include href="&LOCALDOCBOOKXSL;/html/manifest.xsl"/>
    
    <!-- Customize the Table of Contents generation. -->
    <xsl:param name="autotoc.label.separator">. </xsl:param>
    <xsl:param name="toc.section.depth">1</xsl:param>
    <xsl:param name="toc.max.depth">3</xsl:param>
    <xsl:param name="generate.toc">
        set       toc
        book      toc
        part      toc
        chapter   nop
        preface   nop
        section   nop
        qandadiv  nop
        qandaset  toc
        appendix  nop
    </xsl:param>
    
    <!-- Apply the CSS and branding with custom header and footer content -->
    <xsl:param name="html.stylesheet.type">text/css</xsl:param>
    <xsl:param name="html.stylesheet">css/techpubs.css</xsl:param>
    <xsl:param name="html.image.directory">images</xsl:param>
    <xsl:param name="header.rule" select="0"></xsl:param>
    <xsl:template name="user.header.navigation">
        <div id="header-branding-block">
            <div id="header-branding-logo">
                <img src="images/inbloom-logo-on-white-100.png"/>
            </div>
            <div id="header-doctitle">
                Developer Documentation
            </div>
            <xsl:call-template name="breadcrumbs"/>
        </div>
    </xsl:template>
    <xsl:param name="footer.rule" select="0"></xsl:param>
    <xsl:template name="user.footer.navigation">
        <div id="footer-branding-block">
            <div id="footer-branding-logo">
                <img src="images/inbloom-logo-on-white-100.png"/>
            </div>
            <div id="footer-branding-legal">
                <p>
                    Copyright © 2012 inBloom, Inc. and its affiliates.
                </p>
                <p>
                    inBloom is a trademark of inBloom, Inc.
                </p>
                <p>
                    This document and the information contained herein is provided on an "AS IS" 
                    basis and inBloom, Inc. DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
                    LIMITED TO ANY WARRANTY THAT THE USE OF THE INFORMATION HEREIN WILL NOT 
                    INFRINGE ANY RIGHTS OR ANY IMPLIED WARRANTIES OF MERCHANTABILITY OR FITNESS 
                    FOR A PARTICULAR PURPOSE.
                </p>
            </div>
        </div>
    </xsl:template>
    <!-- Customize navigation used in the header and footer -->
    <xsl:param name="suppress.navigation" select="0"/>
    <xsl:param name="navig.showtitles" select="0"/>
    <xsl:param name="navig.graphics" select="1"/>
    <xsl:param name="navig.graphics.path">images/</xsl:param>
    <xsl:param name="navig.graphics.extension">.png</xsl:param>
    <xsl:template name="breadcrumbs">
        <xsl:param name="this.node" select="."/>
        <div class="breadcrumbs">
            <xsl:for-each select="$this.node/ancestor::*">
                <span class="breadcrumb-link">
                    <a>
                        <xsl:attribute name="href">
                            <xsl:call-template name="href.target">
                                <xsl:with-param name="object" select="."/>
                                <xsl:with-param name="context" select="$this.node"/>
                            </xsl:call-template>
                        </xsl:attribute>
                        <xsl:apply-templates select="." mode="title.markup"/>
                    </a>
                </span>
                <xsl:text> &gt; </xsl:text>
            </xsl:for-each>
            <!-- And display the current node, but not as a link -->
            <span class="breadcrumb-node">
                <xsl:apply-templates select="$this.node" mode="title.markup"/>
            </span>
        </div>
    </xsl:template>
    
    <!-- Customize chunking and cross-referencing within the HTML -->
    <xsl:param name="generate.id.attributes" select="1"/>
    <xsl:param name="use.id.as.filename" select="1"/>
    <xsl:param name="chunk.section.depth" select="0"/>
    <xsl:param name="chunk.quietly" select="1"/>
    
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
    
    <!-- Turn off admonition graphics -->
    <xsl:param name="admon.graphics" select="0"></xsl:param>
    
    <!-- Use the monospace font for these entities. -->
    <xsl:template match="code">
        <xsl:call-template name="inline.monoseq"/>
    </xsl:template>
    <xsl:template match="command">
        <xsl:call-template name="inline.monoseq"/>
    </xsl:template>
    <xsl:template match="parameter">
        <xsl:call-template name="inline.monoseq"/>
    </xsl:template>
    <xsl:template match="userinput">
        <xsl:call-template name="inline.monoseq"/>
    </xsl:template>
    
    <!-- Apply the italic font to these entities. -->
    <xsl:template match="firstterm">
        <xsl:call-template name="inline.italicseq"/>
    </xsl:template>
    <xsl:template match="citetitle">
        <xsl:call-template name="inline.italicseq"/>
    </xsl:template>
    <xsl:template match="filename">
        <xsl:call-template name="inline.italicseq"/>
    </xsl:template>
    <xsl:template match="guilabel">
        <xsl:call-template name="inline.italicseq"/>
    </xsl:template>
    <xsl:template match="varname">
        <xsl:call-template name="inline.italicseq"/>
    </xsl:template>
    <xsl:template match="methodname">
        <xsl:call-template name="inline.italicseq"/>
    </xsl:template>
    
    <!-- Apply the bold font to these entities. -->
    <xsl:template match="guibutton">
        <xsl:call-template name="inline.boldseq"/>
    </xsl:template>
    <xsl:template match="classname">
        <xsl:call-template name="inline.boldseq"/>
    </xsl:template>    
    
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

</xsl:stylesheet>
