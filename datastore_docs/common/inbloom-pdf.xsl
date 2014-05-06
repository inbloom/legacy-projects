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
    xmlns:fo="http://www.w3.org/1999/XSL/Format"
    version="1.0">
    
    <!-- Import the DocBook XSL -->
    <xsl:import href="&LOCALDOCBOOKXSL;/fo/profile-docbook.xsl"/>
    <xsl:import href="&LOCALDOCBOOKXSL;/fo/highlight.xsl"/>
    <xsl:import href="inbloom-pdf-titlepage_spec.xsl"/>
    
    <!-- Trim colors coordinated with inBloom logo on 1/15/2013 -->
    <xsl:variable name="color-textblock-background">#DDDDDD</xsl:variable>
    <xsl:variable name="color-trim-light">#66CCCC</xsl:variable>
    <xsl:variable name="color-trim-medium">#47C3CD</xsl:variable>
    <xsl:variable name="color-trim-dark">#5D8EBB</xsl:variable>
    
    <!-- Default font size and text alignment -->
    <xsl:param name="title.font.family">Helvetica,sans-serif</xsl:param>
    <xsl:param name="body.font.family">Helvetica,sans-serif</xsl:param>
    <xsl:param name="sans.font.family">Helvetica,sans-serif</xsl:param>
    <xsl:param name="dingbat.font.family">ZapfDingbats,serif</xsl:param>
    <xsl:param name="symbol.font.family">Symbol,serif</xsl:param> 
    <xsl:param name="monospace.font.family">Courier,monospace</xsl:param>
    <xsl:attribute-set name="monospace.properties">
        <xsl:attribute name="font-family">
            <xsl:value-of select="$monospace.font.family"></xsl:value-of>
        </xsl:attribute>
        <xsl:attribute name="font-size">
            <xsl:value-of select="$body.font.master * 0.90"/>
            <xsl:text>pt</xsl:text>
        </xsl:attribute>
    </xsl:attribute-set>
    <xsl:param name="body.font.master">10</xsl:param>
    <xsl:param name="body.font.size">
        <xsl:value-of select="$body.font.master"/>
        <xsl:text>pt</xsl:text>
    </xsl:param>
    <xsl:param name="alignment">left</xsl:param> 
    <!-- <xsl:param name="alignment">justify</xsl:param> -->
    <!-- Adjust monospace verbatims (screen and programlisting) -->
    <xsl:attribute-set name="shade.verbatim.style">
        <xsl:attribute name="background-color">
            <xsl:value-of select="$color-textblock-background"/>
        </xsl:attribute>
    </xsl:attribute-set>
    <xsl:attribute-set name="monospace.verbatim.properties">
        <xsl:attribute name="wrap-option">wrap</xsl:attribute>
        <xsl:attribute name="hyphenation-character">&#x005C;</xsl:attribute>
    </xsl:attribute-set>
    
    <!-- Adjust titles -->
    <xsl:attribute-set name="section.title.properties">
        <xsl:attribute name="font-family">
            <xsl:value-of select="$title.font.family"></xsl:value-of>
        </xsl:attribute>
        <xsl:attribute name="font-weight">bold</xsl:attribute>
        <xsl:attribute name="keep-with-next.within-column">always</xsl:attribute>
        <xsl:attribute name="space-before.minimum">0.8em</xsl:attribute>
        <xsl:attribute name="space-before.optimum">1.0em</xsl:attribute>
        <xsl:attribute name="space-before.maximum">1.2em</xsl:attribute>
        <xsl:attribute name="text-align">start</xsl:attribute>
    </xsl:attribute-set>
    <xsl:attribute-set name="section.title.level1.properties">
        <xsl:attribute name="font-size">
            <xsl:value-of select="$body.font.master * 1.5"/>
            <xsl:text>pt</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="space-before.minimum">1.0em</xsl:attribute>
        <xsl:attribute name="space-before.optimum">1.6em</xsl:attribute>
        <xsl:attribute name="space-before.maximum">2.0em</xsl:attribute>
    </xsl:attribute-set>
    <xsl:attribute-set name="section.title.level2.properties">
        <xsl:attribute name="font-size">
            <xsl:value-of select="$body.font.master * 1.2"/>
            <xsl:text>pt</xsl:text>
        </xsl:attribute>
    </xsl:attribute-set>
    <xsl:attribute-set name="section.title.level3.properties">
        <xsl:attribute name="font-size">
            <xsl:value-of select="$body.font.master"/>
            <xsl:text>pt</xsl:text>
        </xsl:attribute>
    </xsl:attribute-set> 
    
    <!-- Customize the Table of Contents generation. -->
    <xsl:param name="autotoc.label.separator">. </xsl:param>
    <xsl:param name="toc.section.depth">3</xsl:param>
    <xsl:param name="toc.max.depth">6</xsl:param>
    <xsl:param name="generate.toc">
        set       toc,title
        book      toc,title
        part      nop
        chapter   nop
        preface   nop
        section   nop
    </xsl:param>
    
    <!-- Customize auto-labeling -->
    <xsl:param name="appendix.autolabel" select="'A'"/>
    <xsl:param name="preface.autolabel" select="'i'"/>
    <xsl:param name="chapter.autolabel" select="1"/>
    <xsl:param name="section.autolabel" select="1"/> 
    <xsl:param name="section.label.includes.component.label" select="1"/>
    <xsl:param name="local.l10n.xml" select="document('')"/>
    <l:i18n xmlns:l="http://docbook.sourceforge.net/xmlns/l10n/1.0">
        <l:l10n language="en">
            <!-- Text used when the title element renders -->
            <l:context name="title-numbered">
                <l:template name="part" text="%n. %t"/>
                <l:template name="chapter" text="%n. %t"/>
                <l:template name="section" text="%n. %t"/>
                <l:template name="appendix" text="Appendix %n: %t"/>
                <l:template name="table" text="Table %n. %t"/>
                <l:template name="figure" text="Figure %n. %t"/>
            </l:context>
            <!-- Text within the xref links to that element -->
            <l:context name="xref">
                <l:template name="part" text="Part %n: &#8220;%t&#8221;"/>
                <l:template name="chapter" text="Chapter %n: &#8220;%t&#8221;"/>
                <l:template name="section" text="Section %n: &#8220;%t&#8221;"/>
                <l:template name="appendix" text="Appendix %n: &#8220;%t&#8221;"/>
                <l:template name="table" text="the table &#8220;%t&#8221;"/>
                <l:template name="figure" text="Figure %n: &#8220;%t&#8221;"/>
            </l:context>
            <!-- Numbering of xref links to that element, including in the ToC -->
            <l:context name="title-numbered">
                <l:template name="part" text="%n"/>
                <l:template name="chapter" text="%n"/>
                <l:template name="section" text="%n"/>
                <l:template name="appendix" text="Appendix %n"/>
                <l:template name="table" text=""/>
                <l:template name="figure" text="%n"/>
            </l:context>
        </l:l10n>
    </l:i18n>

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
    
    <!-- Control references to other parts of the same doc (xref) -->
    <xsl:param name="insert.xref.page.number">no</xsl:param>
    <xsl:attribute-set name="xref.properties">
        <xsl:attribute name="font-style">italic</xsl:attribute>
    </xsl:attribute-set>
    
    <!-- Set attributes for each list block -->
    <xsl:attribute-set name="list.block.properties">
        <xsl:attribute name="provisional-label-separation">0.2em</xsl:attribute>
        <xsl:attribute name="provisional-distance-between-starts">1.5em</xsl:attribute>
    </xsl:attribute-set>
    <xsl:attribute-set name="list.block.spacing">
        <xsl:attribute name="space-before.optimum">0.1em</xsl:attribute>
        <xsl:attribute name="space-before.minimum">0.0em</xsl:attribute>
        <xsl:attribute name="space-before.maximum">0.3em</xsl:attribute>
        <xsl:attribute name="space-after.optimum">0.3em</xsl:attribute>
        <xsl:attribute name="space-after.minimum">0.0em</xsl:attribute>
        <xsl:attribute name="space-after.maximum">0.5em</xsl:attribute>
    </xsl:attribute-set>
    <xsl:attribute-set name="list.item.spacing">
        <xsl:attribute name="space-before.optimum">0.6em</xsl:attribute>
        <xsl:attribute name="space-before.minimum">0.0em</xsl:attribute>
        <xsl:attribute name="space-before.maximum">0.6em</xsl:attribute>
    </xsl:attribute-set> 
    <xsl:param name="itemizedlist.label.width">1.0em</xsl:param>
    <xsl:attribute-set name="itemizedlist.properties">
        <xsl:attribute name="margin-left">2.0em</xsl:attribute>
        <xsl:attribute name="margin-right">2.0em</xsl:attribute>
    </xsl:attribute-set>
    <xsl:param name="orderedlist.label.width">1.5em</xsl:param>
    <xsl:attribute-set name="orderedlist.properties">
        <xsl:attribute name="margin-left">2.0em</xsl:attribute>
        <xsl:attribute name="margin-right">2.0em</xsl:attribute>
    </xsl:attribute-set>
    <xsl:attribute-set name="procedure.properties" use-attribute-sets="formal.object.properties">
        <xsl:attribute name="keep-together.within-column">auto</xsl:attribute>
        <xsl:attribute name="margin-left">1.2em</xsl:attribute>
        <xsl:attribute name="margin-right">1.2em</xsl:attribute>
    </xsl:attribute-set>
    
    <!-- Layout for all formal objects, like figures and tables -->
    <xsl:attribute-set name="formal.object.properties">
        <xsl:attribute name="space-before.minimum">0.5em</xsl:attribute>
        <xsl:attribute name="space-before.optimum">1em</xsl:attribute>
        <xsl:attribute name="space-before.maximum">2em</xsl:attribute>
        <xsl:attribute name="space-after.minimum">0.5em</xsl:attribute>
        <xsl:attribute name="space-after.optimum">1em</xsl:attribute>
        <xsl:attribute name="space-after.maximum">2em</xsl:attribute>
        <xsl:attribute name="keep-together.within-column">always</xsl:attribute> 
    </xsl:attribute-set>
    <xsl:param name="formal.title.placement">
        figure before
        table before
    </xsl:param>
    <xsl:attribute-set name="formal.title.properties" use-attribute-sets="normal.para.spacing">
        <xsl:attribute name="font-family">
            <xsl:value-of select="$title.font.family"/>
        </xsl:attribute>
        <xsl:attribute name="font-weight">bold</xsl:attribute>
        <xsl:attribute name="font-style">italic</xsl:attribute>
        <xsl:attribute name="font-size">
            <xsl:value-of select="$body.font.master"/>
            <xsl:text>pt</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="keep-with-next.within-column">always</xsl:attribute>
    </xsl:attribute-set>
    
    <!-- Table layout details -->
    <xsl:param name="default.table.width">100%</xsl:param>
    <xsl:param name="default.table.frame">all</xsl:param>
    <xsl:param name="table.frame.border.thickness">1pt</xsl:param>
    <xsl:param name="table.cell.border.thickness">1pt</xsl:param>
    <xsl:param name="default.table.rules">all</xsl:param>
    <xsl:attribute-set name="table.cell.padding">
        <xsl:attribute name="padding-start">5pt</xsl:attribute>
        <xsl:attribute name="padding-end">10pt</xsl:attribute>
        <xsl:attribute name="padding-top">5pt</xsl:attribute>
        <xsl:attribute name="padding-right">5pt</xsl:attribute>
        <xsl:attribute name="padding-bottom">5pt</xsl:attribute>
        <xsl:attribute name="padding-left">5pt</xsl:attribute>
    </xsl:attribute-set>
    <xsl:attribute-set name="table.table.properties">
        <xsl:attribute name="border-before-width.conditionality">retain</xsl:attribute>
        <xsl:attribute name="border-collapse">collapse</xsl:attribute>
    </xsl:attribute-set>
    
    <!-- Admonition layout, such as notes, cautions, and warnings -->
    <xsl:param name="admon.graphics" select="0"/>
    <xsl:attribute-set name="admonition.title.properties">
        <xsl:attribute name="margin-top">15pt</xsl:attribute>
        <xsl:attribute name="border-left">5pt solid <xsl:value-of select="$color-trim-medium"/></xsl:attribute>
        <xsl:attribute name="margin-left">30pt</xsl:attribute>
        <xsl:attribute name="padding-left">10pt</xsl:attribute>
        <xsl:attribute name="font-family">
            <xsl:value-of select="$title.font.family"></xsl:value-of>
        </xsl:attribute>
        <xsl:attribute name="font-size">1.2em</xsl:attribute>
        <xsl:attribute name="color">
            <xsl:value-of select="$color-trim-dark"/>
        </xsl:attribute>
        <xsl:attribute name="hyphenate">false</xsl:attribute>
        <xsl:attribute name="keep-with-next.within-column">always</xsl:attribute>
    </xsl:attribute-set>
    <xsl:attribute-set name="admonition.properties">
        <xsl:attribute name="border-left">5pt solid <xsl:value-of select="$color-trim-medium"/></xsl:attribute>
        <xsl:attribute name="margin-left">30pt</xsl:attribute>
        <xsl:attribute name="padding-left">10pt</xsl:attribute>
        <xsl:attribute name="padding-bottom">2.5pt</xsl:attribute>
        <xsl:attribute name="margin-bottom">15pt</xsl:attribute>
    </xsl:attribute-set>
    
    <!-- Page, header, and footer layouts -->
    <xsl:param name="paper.type">USletter</xsl:param>
    <xsl:param name="page.orientation">portrait</xsl:param>
    <!-- The following URL is a useful reference for setting your margins:
  http://docbook.sourceforge.net/release/xsl/current/doc/fo/general.html -->
    <xsl:param name="page.margin.top">0.5in</xsl:param>
    <xsl:param name="region.before.extent">0.5in</xsl:param>
    <xsl:param name="body.margin.top">0.6in</xsl:param>
    <xsl:param name="body.margin.bottom">0.6in</xsl:param>
    <xsl:param name="region.after.extent">0.5in</xsl:param>
    <xsl:param name="page.margin.bottom">0.5in</xsl:param>
    <!-- The body indent value assumes the use of Apache FOP for processing -->
    <xsl:param name="body.start.indent">0pt</xsl:param>
    <!-- Side margins are NOT set to vary for double-sided page binding -->
    <xsl:param name="page.margin.outer">0.7in</xsl:param>
    <xsl:param name="page.margin.inner">0.7in</xsl:param>
    
    <!-- Custom header style -->
    <xsl:param name="headers.on.blank.pages" select="1"></xsl:param>
    <xsl:param name="header.rule" select="1"></xsl:param>
    <xsl:param name="header.column.widths">1 2 1</xsl:param> 
    <xsl:attribute-set name="header.table.properties">
        <xsl:attribute name="table-layout">fixed</xsl:attribute>
        <xsl:attribute name="width">100%</xsl:attribute>
    </xsl:attribute-set>
    <xsl:attribute-set name="header.content.properties">
        <xsl:attribute name="font-family">
            <xsl:value-of select="$title.font.family"></xsl:value-of>
        </xsl:attribute>
    </xsl:attribute-set>
    
    <!-- Custom footer style -->
    <xsl:param name="footers.on.blank.pages" select="1"></xsl:param>
    <xsl:param name="footer.rule" select="1"></xsl:param>
    <xsl:param name="footer.column.widths">1 2 1</xsl:param>
    <xsl:attribute-set name="footer.table.properties">
        <xsl:attribute name="table-layout">fixed</xsl:attribute>
        <xsl:attribute name="width">100%</xsl:attribute>
    </xsl:attribute-set>
    <xsl:attribute-set name="footer.content.properties">
        <xsl:attribute name="font-family">
            <xsl:value-of select="$title.font.family"></xsl:value-of>
        </xsl:attribute>
    </xsl:attribute-set>
    
    <!-- Customize the glossary appearance -->
    <xsl:attribute-set name="glossterm.block.properties">
        <xsl:attribute name="font-weight">bold</xsl:attribute>
    </xsl:attribute-set>
    
    <!-- Format external links (those that use the "link" element) -->
    <xsl:param name="ulink.show" select="0" />
    
    <!-- Add and customize the front cover for the document itself. -->
    <xsl:template name="front.cover">
        <xsl:call-template name="page.sequence">
            <xsl:with-param name="master-reference">titlepage</xsl:with-param>
            <xsl:with-param name="content">
                <fo:table table-layout="fixed" width="100%">
                    <fo:table-column column-width="proportional-column-width(1)"/>
                    <fo:table-column column-width="proportional-column-width(2)"/>
                    <fo:table-body>
                        <fo:table-row>
                            <fo:table-cell column-number="1">
                                <fo:block>
                                    <fo:external-graphic src="../common/images/inbloom-logo-on-white-200.png"/>
                                </fo:block>
                            </fo:table-cell>
                        </fo:table-row>
                        <fo:table-row>
                            <fo:table-cell column-number="2"
                                padding-top="40pt"
                                border-bottom="2pt solid {$color-trim-medium}">
                                <fo:block text-align="left">
                                    <fo:inline font-family="Helvetica,sans-serif"
                                        font-size="20pt"
                                        font-weight="bold"
                                        color="{$color-trim-dark}">
                                        <xsl:value-of select="d:title|d:info/d:title"/>
                                    </fo:inline>
                                </fo:block>
                            </fo:table-cell>
                        </fo:table-row>
                        <fo:table-row>
                            <fo:table-cell column-number="2"
                                padding-top="10pt">
                                <fo:block text-align="left">
                                    <fo:inline font-family="Helvetica,sans-serif"
                                        font-size="14pt"
                                        color="{$color-trim-medium}">
                                        &COMPANY;
                                    </fo:inline>
                                </fo:block>
                            </fo:table-cell>
                        </fo:table-row>
                        <fo:table-row>
                            <fo:table-cell column-number="2"
                                padding-top="5pt">
                                <fo:block text-align="left">
                                    <fo:inline font-family="Helvetica,sans-serif"
                                        font-size="14pt"
                                        color="{$color-trim-medium}">
                                        <xsl:value-of select="d:title|d:info/d:releaseinfo"/>
                                    </fo:inline>
                                </fo:block>
                            </fo:table-cell>
                        </fo:table-row>
                        <fo:table-row>
                            <fo:table-cell column-number="2"
                                padding-top="300pt">
                                <fo:block text-align="left">
                                    <fo:inline font-family="Helvetica,sans-serif"
                                        font-size="10pt"
                                        font-weight="bold">
                                        Copyright © &PUBYEAR; inBloom, Inc. and its affiliates.
                                    </fo:inline>
                                </fo:block>
                            </fo:table-cell>
                        </fo:table-row>
                        <fo:table-row>
                            <fo:table-cell column-number="2"
                                padding-top="20pt">
                                <fo:block text-align="left">
                                    <fo:inline font-family="Helvetica,sans-serif"
                                        font-size="10pt">
                                        inBloom is a trademark of inBloom, Inc.
                                    </fo:inline>
                                </fo:block>
                            </fo:table-cell>
                        </fo:table-row>
                        <fo:table-row>
                            <fo:table-cell column-number="2"
                                padding-top="20pt">
                                <fo:block text-align="left">
                                    <fo:inline font-family="Arial,sans-serif"
                                        font-size="10pt">
                                        This document and the information contained herein is provided on an "AS IS" 
                                        basis and inBloom, Inc. DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
                                        LIMITED TO ANY WARRANTY THAT THE USE OF THE INFORMATION HEREIN WILL NOT 
                                        INFRINGE ANY RIGHTS OR ANY IMPLIED WARRANTIES OF MERCHANTABILITY OR FITNESS 
                                        FOR A PARTICULAR PURPOSE.
                                    </fo:inline>
                                </fo:block>
                            </fo:table-cell>
                        </fo:table-row>
                    </fo:table-body>
                </fo:table>
            </xsl:with-param>
        </xsl:call-template>
    </xsl:template>
    
    <!-- Remove the title pages since we added a nice cover page -->
    <xsl:template name="book.titlepage.recto"/>
    <xsl:template name="book.titlepage.before.verso"/>
    
    <!-- Revision history table -->
    <xsl:attribute-set name="revhistory.title.properties">
        <xsl:attribute name="font-family">
            <xsl:value-of select="$title.font.family"></xsl:value-of>
        </xsl:attribute>
        <xsl:attribute name="font-size">
            <xsl:value-of select="$body.font.master * 1.2"/>
            <xsl:text>pt</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="font-weight">bold</xsl:attribute>
        <xsl:attribute name="text-align">left</xsl:attribute>
    </xsl:attribute-set>
    <xsl:attribute-set name="revhistory.table.properties">
        <xsl:attribute name="border">0.5pt solid black</xsl:attribute>
        <xsl:attribute name="background-color">
            <xsl:value-of select="$color-textblock-background"/>
        </xsl:attribute>
    </xsl:attribute-set>
    <xsl:attribute-set name="revhistory.table.cell.properties">
        <xsl:attribute name="border">0.5pt solid black</xsl:attribute>
        <xsl:attribute name="font-size">9pt</xsl:attribute>
        <xsl:attribute name="padding">4pt</xsl:attribute>
        <xsl:attribute name="background-color">
            <xsl:value-of select="$color-textblock-background"/>
        </xsl:attribute>
    </xsl:attribute-set>
    <!-- Templates for revhistory and revision adapted from DocBook XSL's fo/titlepage.xsl -->
    <xsl:template match="d:revhistory" mode="titlepage.mode">
        <xsl:variable name="explicit.table.width">
            <xsl:call-template name="pi.dbfo_table-width"/>
        </xsl:variable>
        <xsl:variable name="table.width">
            <xsl:choose>
                <xsl:when test="$explicit.table.width != ''">
                    <xsl:value-of select="$explicit.table.width"/>
                </xsl:when>
                <xsl:when test="$default.table.width = ''">
                    <xsl:text>100%</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="$default.table.width"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <fo:table table-layout="fixed" width="{$table.width}" xsl:use-attribute-sets="revhistory.table.properties">
            <fo:table-column column-number="1" column-width="proportional-column-width(1)"/>
            <fo:table-column column-number="2" column-width="proportional-column-width(1)"/>
            <fo:table-column column-number="3" column-width="proportional-column-width(4)"/>
            <fo:table-body start-indent="0pt" end-indent="0pt">
                <fo:table-row>
                    <fo:table-cell number-columns-spanned="3" xsl:use-attribute-sets="revhistory.table.cell.properties">
                        <fo:block xsl:use-attribute-sets="revhistory.title.properties">
                            <xsl:choose>
                                <xsl:when test="d:title|d:info/d:title">
                                    <xsl:apply-templates select="d:title|d:info/d:title" mode="titlepage.mode"/>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:call-template name="gentext">
                                        <xsl:with-param name="key" select="'RevHistory'"/>
                                    </xsl:call-template>
                                </xsl:otherwise>
                            </xsl:choose>
                        </fo:block>
                    </fo:table-cell>
                </fo:table-row>
                <xsl:apply-templates select="*[not(self::d:title)]" mode="titlepage.mode"/>
            </fo:table-body>
        </fo:table>
    </xsl:template>
    <xsl:template match="d:revhistory/d:revision" mode="titlepage.mode">
        <xsl:variable name="revnumber" select="d:revnumber"/>
        <xsl:variable name="revdate"   select="d:date"/>
        <xsl:variable name="revdescription" select="d:revremark|d:revdescription"/>
        <fo:table-row>
            <fo:table-cell xsl:use-attribute-sets="revhistory.table.cell.properties">
                <fo:block>
                    <xsl:if test="$revnumber">
                        <!-- <xsl:call-template name="gentext">
                            <xsl:with-param name="key" select="'Revision'"/>
                        </xsl:call-template> -->
                        <xsl:call-template name="gentext.space"/>
                        <xsl:apply-templates select="$revnumber[1]" mode="titlepage.mode"/>
                    </xsl:if>
                </fo:block>
            </fo:table-cell>
            <fo:table-cell xsl:use-attribute-sets="revhistory.table.cell.properties">
                <fo:block>
                    <xsl:apply-templates select="$revdate[1]" mode="titlepage.mode"/>
                </fo:block>
            </fo:table-cell>
            <fo:table-cell xsl:use-attribute-sets="revhistory.table.cell.properties">
                <fo:block>
                    <xsl:apply-templates select="$revdescription[1]" mode="titlepage.mode"/>
                </fo:block>
            </fo:table-cell>
        </fo:table-row>
    </xsl:template>
    
</xsl:stylesheet>
