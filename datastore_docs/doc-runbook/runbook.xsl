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
    <xsl:import href="../common/inbloom-pdf.xsl"/>
    
    <!-- INSTRUCTIONS FOR MARKING CHANGES TO RUNBOOK CONTENT
    
    To mark changes for INLINE TEXT, do one of the following:
        * If an entire paragraph changed, use the "role" attribute in the
          opening "para" tag
        * If part of paragraph changed, or to highlight non-para-tagged
          content, place "phrase" tags around new content and use
          the "role" attribute in the opening "phrase tag.
    The value of the role attribute follows this syntax:
    
                  $N-changeType
                  
       * "$N" is the sprint number in which the associated code
         change is taking place, which should correspond to the
         value of the "CURRENTSPRINT" entity in ../common/entities.ent
       * Reaplce "changeType" with one of the following strings:
          ** "added" - phrase was added since the previous version
          ** "changed" - phrase was changed since the previous version
          ** "deleted" - phrase was deleted since the previous version
          ** "info" - phrase is an information block indicating
             a story or defect link associated with a change
             (see paragraph below about "info" blocks)
             
    When using the "info" block, it should be placed at the end of a 
    paragraph affected by a change that's already marked with one of the
    added, changed, or deleted roles. The following syntax has been used
    when creating these "info" items, replacing "<link>" with the external 
    link to the associated story or defect in the tracking tool (Rally):
    
                  [$N revision(s) shown; see <link>]
    
    To mark changes for a GRAPHIC, simply add an info block
    after the graphic itself. 
    -->
    
    <!-- Roles for styling and controlling revisions using phrase elements -->
    <xsl:template match="d:phrase[@role]">
        <xsl:choose>
            <!-- When it's marked, but for something earlier than the current version... -->
            <xsl:when test="substring-before(@role,'-') != &CURRENTSPRINT;">
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
            </xsl:when>
            <!-- When marked as having changed in the current revision... -->
            <xsl:otherwise>
                <fo:inline xsl:use-attribute-sets="normal.para.spacing">
                    <xsl:choose>
                        <xsl:when test="substring-after(@role,'-') = 'info'">
                            <xsl:attribute name="color">#0099CC</xsl:attribute>
                            <xsl:attribute name="font-style">italic</xsl:attribute>
                        </xsl:when>
                        <xsl:when test="substring-after(@role,'-') = 'added'">
                            <xsl:attribute name="background-color">#CCFFCC</xsl:attribute>
                        </xsl:when>
                        <xsl:when test="substring-after(@role,'-') = 'changed'">
                            <xsl:attribute name="background-color">#99CCFF</xsl:attribute>
                        </xsl:when>
                        <xsl:when test="substring-after(@role,'-') = 'deleted'">
                            <xsl:attribute name="color">#CCCCCC</xsl:attribute>
                            <xsl:attribute name="text-decoration">line-through</xsl:attribute>
                        </xsl:when>
                    </xsl:choose>
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
            <!-- When it's marked, but for something earlier than the current version... -->
            <xsl:when test="substring-before(@role,'-') != &CURRENTSPRINT;">
                <xsl:choose>
                    <xsl:when test="substring-after(@role,'-') = 'info'">
                        <!-- Don't display the text at all -->
                    </xsl:when>
                    <xsl:when test="substring-after(@role,'-') = 'deleted'">
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
            </xsl:when>
            <!-- When marked as having changed in the current revision... -->
            <xsl:otherwise>
                <fo:block xsl:use-attribute-sets="para.properties">
                    <xsl:choose>
                        <xsl:when test="substring-after(@role,'-') = 'info'">
                            <xsl:attribute name="color">#0099CC</xsl:attribute>
                            <xsl:attribute name="font-style">italic</xsl:attribute>
                        </xsl:when>
                        <xsl:when test="substring-after(@role,'-') = 'added'">
                            <xsl:attribute name="background-color">#CCFFCC</xsl:attribute>
                        </xsl:when>
                        <xsl:when test="substring-after(@role,'-') = 'changed'">
                            <xsl:attribute name="background-color">#99CCFF</xsl:attribute>
                        </xsl:when>
                        <xsl:when test="substring-after(@role,'-') = 'deleted'">
                            <xsl:attribute name="color">#CCCCCC</xsl:attribute>
                            <xsl:attribute name="text-decoration">line-through</xsl:attribute>
                        </xsl:when>
                    </xsl:choose>
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