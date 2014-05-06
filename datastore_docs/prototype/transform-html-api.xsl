<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                xmlns:d="http://docbook.org/ns/docbook"
                xmlns:xlink='http://www.w3.org/1999/xlink'
                xmlns:suwl="http://nwalsh.com/xslt/ext/com.nwalsh.saxon.UnwrapLinks"
                version="1.0">
    
    <xsl:include href="transform-html-common.xsl"/>
    
    <xsl:param name="html.stylesheet.type">text/css</xsl:param>
    <xsl:param name="html.stylesheet">../css/techpubs.css</xsl:param>
    <xsl:param name="html.image.directory">../images</xsl:param>
    
    <xsl:param name="suppress.navigation" select="1"/>
    
    <xsl:template name="user.head.content">
        <script src="../js/live_query_form.js" />
    </xsl:template>
    
    <xsl:template name="user.header.navigation">
        <div id="header-branding-block">
            <div id="header-branding-logo">
                <img src="../images/inbloom-logo-on-white-100.png"/>
            </div>
            <div id="header-doctitle">
                Developer Documentation
            </div>
            <div id="header-search">
                <div id="header-search-entry">
                    Enter search term
                </div>
                <div id="header-search-button">
                    Search
                </div>
            </div>
            <ul id="menu-top">
                <li class="selected">
                    <a href="../api/index.html">API</a>
                </li>
                <li>
                    <a href="../sdk/index.html">SDK</a>
                </li>
                <li>
                    <a href="../data_model/index.html">Data Model</a>
                </li>
                <li>
                    <a href="../sandbox/index.html">Sandbox Guide</a>
                </li>
                <li>
                    <a href="../security/index.html">Security Guide</a>
                </li>
            </ul>
        </div>
        <div id="menu-left">
            <ul>
                <li>
                    <a href="../api/doc-api-overview.html" target="_top">Overview</a>
                </li>
                <li>
                    <a href="../api/doc-api-getting_started.html" target="_top">Getting Started</a>
                </li>
                <li>
                    <a href="../api/doc-api-parameters_and_patterns.html" target="_top">Parameters</a>
                    <ul>
                        <li>
                            <a href="../api/doc-api-parameters_and_patterns.html#doc-api-parameters" target="_top">Parameters</a>
                        </li>
                        <li>
                            <a href="../api/doc-api-parameters_and_patterns.html#doc-api-patterns" target="_top">Patterns</a>
                        </li>
                    </ul>
                </li>
                <li>
                    <a href="../api/doc-api-resources.html" target="_top">Resources</a>
                    <ul>
                        <li>
                            <a href="../api/api-resource-data-sample.html" target="_top">students</a>
                        </li>
                    </ul>
                </li>
                <li>
                    <b><a href="../api/doc-api-live_query_form.html" target="_top">Live API</a></b>
                    <ul>
                        <li style="font-size:smaller">
                            <i>Test your GET requests with live sample data!</i>
                        </li>
                    </ul>
                </li>
            </ul>
        </div>
    </xsl:template>
    
    <xsl:template name="user.footer.navigation">
        <div id="footer-branding-block">
            <div id="footer-branding-logo">
                <img src="../images/inbloom-logo-on-white-100.png"/>
            </div>
            <div id="footer-branding-legal">
                <p>
                    Copyright © 2014 inBloom, Inc. and its affiliates.
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

</xsl:stylesheet>
