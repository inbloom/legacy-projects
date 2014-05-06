<?xml version='1.0'?>
<xsl:stylesheet
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:suwl="http://nwalsh.com/xslt/ext/com.nwalsh.saxon.UnwrapLinks"
  version='1.0'>

    <!-- simple.link template copied from DocBook XSL file (xsl/html/inline.xsl) and modified as needed -->
    <xsl:template name="simple.xlink">
        <xsl:param name="node" select="."/>
        <xsl:param name="content">
            <xsl:apply-templates/>
        </xsl:param>
        <xsl:param name="linkend" select="$node/@linkend"/>
        <xsl:param name="xhref" select="$node/@xlink:href"/>
        
        <!-- Support for @xlink:show -->
        <xsl:variable name="target.show">
            <xsl:choose>
                <!-- CUSTOMIZATION POINT: added definition for "embed value and a default value for when xlink:show isn't specified -->
                <xsl:when test="$node/@xlink:show = 'new'">_blank</xsl:when>
                <xsl:when test="$node/@xlink:show = 'replace'">_top</xsl:when>
                <xsl:when test="$node/@xlink:show = 'embed'">_self</xsl:when>
                <xsl:otherwise>_self</xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        
        <xsl:variable name="link">
            <xsl:choose>
                <xsl:when test="$xhref and 
                    (not($node/@xlink:type) or 
                    $node/@xlink:type='simple')">
                    
                    <!-- Is it a local idref or a uri? -->
                    <xsl:variable name="is.idref">
                        <xsl:choose>
                            <xsl:when test="starts-with($xhref,'#')
                                and (not(contains($xhref,'&#40;'))
                                or starts-with($xhref,
                                '#xpointer&#40;id&#40;'))">1</xsl:when>
                            <xsl:otherwise>0</xsl:otherwise>
                        </xsl:choose>
                    </xsl:variable>
                    
                    <!-- Is it an olink ? -->
                    <xsl:variable name="is.olink">
                        <xsl:choose>
                            <xsl:when test="contains($xhref,'#') and
                                @xlink:role = $xolink.role">1</xsl:when>
                            <xsl:otherwise>0</xsl:otherwise>
                        </xsl:choose>
                    </xsl:variable>
                    
                    <xsl:choose>
                        <xsl:when test="$is.olink = 1">
                            <xsl:call-template name="olink">
                                <xsl:with-param name="content" select="$content"/>
                            </xsl:call-template>
                        </xsl:when>
                        
                        <xsl:when test="$is.idref = 1">
                            
                            <xsl:variable name="idref">
                                <xsl:call-template name="xpointer.idref">
                                    <xsl:with-param name="xpointer" select="$xhref"/>
                                </xsl:call-template>
                            </xsl:variable>
                            
                            <xsl:variable name="targets" select="key('id',$idref)"/>
                            <xsl:variable name="target" select="$targets[1]"/>
                            
                            <xsl:call-template name="check.id.unique">
                                <xsl:with-param name="linkend" select="$idref"/>
                            </xsl:call-template>
                            
                            <xsl:choose>
                                <xsl:when test="count($target) = 0">
                                    <xsl:message>
                                        <xsl:text>XLink to nonexistent id: </xsl:text>
                                        <xsl:value-of select="$idref"/>
                                    </xsl:message>
                                    <xsl:copy-of select="$content"/>
                                </xsl:when>
                                
                                <xsl:otherwise>
                                    <a>
                                        <xsl:apply-templates select="." mode="common.html.attributes"/>
                                        
                                        <xsl:attribute name="href">
                                            <xsl:call-template name="href.target">
                                                <xsl:with-param name="object" select="$target"/>
                                            </xsl:call-template>
                                        </xsl:attribute>
                                        
                                        <xsl:choose>
                                            <xsl:when test="$node/@xlink:title">
                                                <xsl:attribute name="title">
                                                    <xsl:value-of select="$node/@xlink:title"/>
                                                </xsl:attribute>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:apply-templates select="$target"
                                                    mode="html.title.attribute"/>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                        
                                        <xsl:if test="$target.show !=''">
                                            <xsl:attribute name="target">
                                                <xsl:value-of select="$target.show"/>
                                            </xsl:attribute>
                                        </xsl:if>
                                        
                                        <xsl:copy-of select="$content"/>
                                        
                                    </a>
                                </xsl:otherwise>
                            </xsl:choose>
                        </xsl:when>
                        
                        <!-- otherwise it's a URI -->
                        <xsl:otherwise>
                            <a>
                                <xsl:apply-templates select="." mode="common.html.attributes"/>
                                <xsl:attribute name="href">
                                    <xsl:value-of select="$xhref"/>
                                </xsl:attribute>
                                <xsl:if test="$node/@xlink:title">
                                    <xsl:attribute name="title">
                                        <xsl:value-of select="$node/@xlink:title"/>
                                    </xsl:attribute>
                                </xsl:if>
                                
                                <!-- For URIs, use @xlink:show if defined, otherwise use ulink.target -->
                                <xsl:choose>
                                    <xsl:when test="$target.show !=''">
                                        <xsl:attribute name="target">
                                            <xsl:value-of select="$target.show"/>
                                        </xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="$ulink.target !=''">
                                        <xsl:attribute name="target">
                                            <xsl:value-of select="$ulink.target"/>
                                        </xsl:attribute>
                                    </xsl:when>
                                </xsl:choose>
                                
                                <xsl:copy-of select="$content"/>
                            </a>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:when>
                
                <xsl:when test="$linkend">
                    <xsl:variable name="targets" select="key('id',$linkend)"/>
                    <xsl:variable name="target" select="$targets[1]"/>
                    
                    <xsl:call-template name="check.id.unique">
                        <xsl:with-param name="linkend" select="$linkend"/>
                    </xsl:call-template>
                    
                    <a>
                        <xsl:apply-templates select="." mode="common.html.attributes"/>
                        <xsl:attribute name="href">
                            <xsl:call-template name="href.target">
                                <xsl:with-param name="object" select="$target"/>
                            </xsl:call-template>
                        </xsl:attribute>
                        
                        <xsl:apply-templates select="$target" mode="html.title.attribute"/>
                        
                        <xsl:copy-of select="$content"/>
                        
                    </a>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:copy-of select="$content"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        
        <xsl:choose>
            <xsl:when test="function-available('suwl:unwrapLinks')">
                <xsl:copy-of select="suwl:unwrapLinks($link)"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:copy-of select="$link"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>

