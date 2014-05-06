<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="2.0">
    
    <xsl:output method="html" indent="yes"/>
    
    <xsl:variable name="baseUri" select="'https://example.com/api/rest'"/>
    
    <xsl:template match="/">
        <xsl:for-each select="application/resources/resource">
            <xsl:choose>
                <!-- Version 1.2... -->
                <xsl:when test="contains(@path,'v1.2')">
                    <xsl:variable name="resourceTitle">
                        <xsl:value-of select="substring-after(@path,'v1.2/')"/>
                    </xsl:variable>
                    <xsl:variable name="resourceId">
                        <xsl:call-template name="getId">
                            <xsl:with-param name="rawString" select="$resourceTitle"/>
                        </xsl:call-template>
                    </xsl:variable>
                    <xsl:variable name="resourcePath">
                        <xsl:value-of select="@path" />
                    </xsl:variable>
                    <xsl:variable name="fullResourcePath">
                        <xsl:choose>
                            <xsl:when test="starts-with($resourcePath,'/')">
                                <xsl:value-of select="concat($baseUri,$resourcePath)"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="concat($baseUri,'/',$resourcePath)"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:variable>
                    <xsl:variable name="availableSince">
                        <xsl:choose>
                            <xsl:when test="availableSince">
                                <xsl:value-of select="availableSince"/>
                            </xsl:when>
                            <xsl:otherwise>
                                1.0 or before
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:variable>
                    <xsl:variable name="deprecatedVersion">
                        <xsl:choose>
                            <xsl:when test="deprecatedVersion">
                                <xsl:value-of select="deprecatedVersion"/>
                            </xsl:when>
                            <xsl:otherwise>empty</xsl:otherwise>
                        </xsl:choose>
                    </xsl:variable>
                    <xsl:variable name="description">
                        <xsl:choose>
                            <xsl:when test="string-length(doc)>0">
                                <xsl:call-template name="fixLinks">
                                    <xsl:with-param name="rawString" select="doc"/>
                                </xsl:call-template>
                            </xsl:when>
                            <xsl:otherwise>empty</xsl:otherwise>
                        </xsl:choose>
                    </xsl:variable>
                    <xsl:variable name="filename"
                        select="concat('api-resources/1.2/',$resourceId,'.html')" />
                    <xsl:result-document href="{$filename}">
                        <xsl:call-template name="testLayout">
                            <xsl:with-param name="apiVersion" select="string('1.2')"/>
                            <xsl:with-param name="resourceTitle" select="$resourceTitle"/>
                            <xsl:with-param name="fullPath" select="$fullResourcePath"/>
                            <xsl:with-param name="availableSince" select="$availableSince"/>
                            <xsl:with-param name="deprecatedVersion" select="$deprecatedVersion"/>
                            <xsl:with-param name="description" select="$description"/>
                        </xsl:call-template>
                    </xsl:result-document>
                </xsl:when>
                <!-- Version 1.1... -->
                <xsl:when test="contains(@path,'v1.1')">
                    <xsl:variable name="resourceTitle">
                        <xsl:value-of select="substring-after(@path,'v1.1/')"/>
                    </xsl:variable>
                    <xsl:variable name="resourceId">
                        <xsl:call-template name="getId">
                            <xsl:with-param name="rawString" select="$resourceTitle"/>
                        </xsl:call-template>
                    </xsl:variable>
                    <xsl:variable name="resourcePath">
                        <xsl:value-of select="@path" />
                    </xsl:variable>
                    <xsl:variable name="fullResourcePath">
                        <xsl:choose>
                            <xsl:when test="starts-with($resourcePath,'/')">
                                <xsl:value-of select="concat($baseUri,$resourcePath)"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="concat($baseUri,'/',$resourcePath)"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:variable>
                    <xsl:variable name="availableSince">
                        <xsl:choose>
                            <xsl:when test="availableSince">
                                <xsl:value-of select="availableSince"/>
                            </xsl:when>
                            <xsl:otherwise>
                                1.0 or before
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:variable>
                    <xsl:variable name="deprecatedVersion">
                        <xsl:choose>
                            <xsl:when test="deprecatedVersion">
                                <xsl:value-of select="deprecatedVersion"/>
                            </xsl:when>
                            <xsl:otherwise>empty</xsl:otherwise>
                        </xsl:choose>
                    </xsl:variable>
                    <xsl:variable name="description">
                        <xsl:choose>
                            <xsl:when test="string-length(doc)>0">
                                <xsl:call-template name="fixLinks">
                                    <xsl:with-param name="rawString" select="doc"/>
                                </xsl:call-template>
                            </xsl:when>
                            <xsl:otherwise>empty</xsl:otherwise>
                        </xsl:choose>
                    </xsl:variable>
                    <xsl:variable name="filename"
                        select="concat('api-resources/1.1/',$resourceId,'.html')" />
                    <xsl:result-document href="{$filename}">
                        <xsl:call-template name="testLayout">
                            <xsl:with-param name="apiVersion" select="string('1.1')"/>
                            <xsl:with-param name="resourceTitle" select="$resourceTitle"/>
                            <xsl:with-param name="fullPath" select="$fullResourcePath"/>
                            <xsl:with-param name="availableSince" select="$availableSince"/>
                            <xsl:with-param name="deprecatedVersion" select="$deprecatedVersion"/>
                            <xsl:with-param name="description" select="$description"/>
                        </xsl:call-template>
                    </xsl:result-document>
                </xsl:when>
                <!-- Version 1.0... -->
                <xsl:when test="contains(@path,'v1.0')">
                    <xsl:variable name="resourceTitle">
                        <xsl:value-of select="substring-after(@path,'v1.0/')"/>
                    </xsl:variable>
                    <xsl:variable name="resourceId">
                        <xsl:call-template name="getId">
                            <xsl:with-param name="rawString" select="$resourceTitle"/>
                        </xsl:call-template>
                    </xsl:variable>
                    <xsl:variable name="resourcePath">
                        <xsl:value-of select="@path" />
                    </xsl:variable>
                    <xsl:variable name="fullResourcePath">
                        <xsl:choose>
                            <xsl:when test="starts-with($resourcePath,'/')">
                                <xsl:value-of select="concat($baseUri,$resourcePath)"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="concat($baseUri,'/',$resourcePath)"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:variable>
                    <xsl:variable name="availableSince">
                        <xsl:choose>
                            <xsl:when test="availableSince">
                                <xsl:value-of select="availableSince"/>
                            </xsl:when>
                            <xsl:otherwise>
                                1.0 or before
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:variable>
                    <xsl:variable name="deprecatedVersion">
                        <xsl:choose>
                            <xsl:when test="deprecatedVersion">
                                <xsl:value-of select="deprecatedVersion"/>
                            </xsl:when>
                            <xsl:otherwise>empty</xsl:otherwise>
                        </xsl:choose>
                    </xsl:variable>
                    <xsl:variable name="description">
                        <xsl:choose>
                            <xsl:when test="string-length(doc)>0">
                                <xsl:call-template name="fixLinks">
                                    <xsl:with-param name="rawString" select="doc"/>
                                </xsl:call-template>
                            </xsl:when>
                            <xsl:otherwise>empty</xsl:otherwise>
                        </xsl:choose>
                    </xsl:variable>
                    <xsl:variable name="filename"
                        select="concat('api-resources/1.0/',$resourceId,'.html')" />
                    <xsl:result-document href="{$filename}">
                        <xsl:call-template name="testLayout">
                            <xsl:with-param name="apiVersion" select="string('1.0')"/>
                            <xsl:with-param name="resourceTitle" select="$resourceTitle"/>
                            <xsl:with-param name="fullPath" select="$fullResourcePath"/>
                            <xsl:with-param name="availableSince" select="$availableSince"/>
                            <xsl:with-param name="deprecatedVersion" select="$deprecatedVersion"/>
                            <xsl:with-param name="description" select="$description"/>
                        </xsl:call-template>
                    </xsl:result-document>
                </xsl:when>
            </xsl:choose>
        </xsl:for-each>
    </xsl:template>
    
    <xsl:template name="testLayout">
        <xsl:param name="apiVersion" />
        <xsl:param name="resourceTitle" />
        <xsl:param name="fullPath" />
        <xsl:param name="availableSince" />
        <xsl:param name="deprecatedVersion" />
        <xsl:param name="description" />
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="../css/techpubs.css"/>
            </head>
            <body>
                <h1><xsl:value-of select="$resourceTitle" /></h1>
                <p>
                    API Version: <xsl:value-of select="$apiVersion" />
                </p>
                <p>
                    Available since: <xsl:value-of select="$availableSince" />
                </p>
                <xsl:if test="not(starts-with($deprecatedVersion,'empty'))">
                    <p>
                        <b>DEPRECATED:</b> This resource was deprecated 
                        starting with API version
                        <xsl:value-of select="$deprecatedVersion" />.
                    </p>
                </xsl:if>
                <p>
                    URI: <xsl:value-of select="$fullPath" />
                </p>
                <xsl:if test="not(starts-with($description,'empty'))">
                    <p>
                        DESCRIPTION:<br />
                        <xsl:value-of select="$description" />
                    </p>
                </xsl:if>
                <xsl:if test="param">
                    <xsl:call-template name="getResourceParams" />
                </xsl:if>
                <xsl:for-each select="method">
                    <xsl:variable name="methodName" select="@name"/>
                    <xsl:call-template name="getMethodSection">
                        <xsl:with-param name="apiVersion" select="$apiVersion"/>
                        <xsl:with-param name="methodName" select="$methodName"/>
                    </xsl:call-template>
                </xsl:for-each>
            </body>
        </html>
    </xsl:template>
    
    <xsl:template name="getId">
        <xsl:param name="rawString"/>
        <xsl:variable name="stringWithBeginBracesRemoved">
            <xsl:value-of select="translate($rawString, '{', '')"/>
        </xsl:variable>
        <xsl:variable name="stringWithEndBracesRemoved">
            <xsl:value-of select="translate($stringWithBeginBracesRemoved, '}', '')"/>
        </xsl:variable>
        <xsl:variable name="stringWithSlashesReplaced">
            <xsl:value-of select="translate($stringWithEndBracesRemoved, '/', '-')"/>
        </xsl:variable>
        <xsl:value-of select="$stringWithSlashesReplaced"/>
    </xsl:template>
    
    <xsl:template name="fixLinks">
        <xsl:param name="rawString" />
        <xsl:choose>
            <xsl:when test="contains($rawString, '$$')">
                <xsl:variable name="beginningSubstring">
                    <xsl:value-of select="substring-before($rawString,'$$')"/>
                </xsl:variable>
                <xsl:variable name="endingWithLinkText">
                    <xsl:value-of select="substring-after($rawString,'$$')"/>
                </xsl:variable>
                <xsl:variable name="linkText">
                    <xsl:value-of select="substring-before($endingWithLinkText,'$$')"/>
                </xsl:variable>
                <xsl:variable name="endingSubstring">
                    <xsl:value-of select="substring-after($endingWithLinkText,'$$')"/>
                </xsl:variable>
                <xsl:value-of select="$beginningSubstring"/>
                <xsl:call-template name="getModelLink">
                    <xsl:with-param name="modelEntity" select="$linkText"/>
                </xsl:call-template>
                <xsl:call-template name="fixLinks">
                    <xsl:with-param name="rawString" select="$endingSubstring"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$rawString"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template name="getModelLink">
        <xsl:param name="modelEntity"/>
        <xsl:variable name="modelEntityFile">
            <xsl:value-of select="'data_model-entities.html'"/>
        </xsl:variable>
        <a href="{$modelEntityFile}#type-{$modelEntity}"><xsl:value-of select="$modelEntity"/></a>
    </xsl:template>
    
    <xsl:template name="getResourceParams">
        <p>
            PARAMETERS
        </p>
        <table width="70%">
            <xsl:for-each select="param">
                <xsl:variable name="paramName" select="@name"/>
                <tr>
                    <td style="width: 30%; border:1pt solid black; align: left;">
                        <p>
                            <xsl:value-of select="$paramName"/>
                        </p>
                    </td>
                    <td style="width: 70%; border:1pt solid black; align: left;">
                        <xsl:choose>
                            <xsl:when test="string-length(doc)>0">
                                <xsl:call-template name="fixLinks">
                                    <xsl:with-param name="rawString" select="doc"/>
                                </xsl:call-template>
                            </xsl:when>
                            <xsl:otherwise>
                                FIXME... Parameter description not available.
                            </xsl:otherwise>
                        </xsl:choose>
                    </td>
                </tr>
            </xsl:for-each>
        </table>
    </xsl:template>
    
    <xsl:template name="getMethodSection">
        <xsl:param name="apiVersion"/>
        <xsl:param name="methodName"/>
        <hr />
        <p>
            METHOD: <xsl:value-of select="$methodName"/>
        </p>
        <p>
            <xsl:choose>
                <xsl:when test="string-length(doc)>0">
                    <xsl:call-template name="fixLinks">
                        <xsl:with-param name="rawString" select="doc"/>
                    </xsl:call-template>
                </xsl:when>
                <xsl:otherwise>
                    FIXME... Method description expected but not available.
                </xsl:otherwise>
            </xsl:choose>
        </p>
        <xsl:if test="$methodName='GET'">
            <xsl:if test="request/param">
                <xsl:call-template name="getMethodParams">
                    <xsl:with-param name="methodName" select="$methodName"/>
                </xsl:call-template>
            </xsl:if>
        </xsl:if>
        <p>
            REQUEST:<br />
            <xsl:call-template name="requestBoilerplate">
                <xsl:with-param name="methodName" select="$methodName"/>
            </xsl:call-template>
        </p>
        <p>
            RESPONSE:<br />
            <xsl:call-template name="responseBoilerplate">
                <xsl:with-param name="methodName" select="$methodName"/>
            </xsl:call-template>
        </p>
        <xsl:if test="$methodName='GET'">
            <p>
                <i>Place example here.</i>
            </p>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="getMethodParams">
        <xsl:param name="methodName"/>
        <p>
            PARAMETERS
        </p>
        <table width="70%">
            <xsl:for-each select="request/param">
                <xsl:variable name="paramName" select="@name"/>
                <tr>
                    <td style="width: 30%; border:1pt solid black; align: left;">
                        <p>
                            <xsl:value-of select="$paramName"/>
                        </p>
                    </td>
                    <td style="width: 70%; border:1pt solid black; align: left;">
                        <xsl:choose>
                            <xsl:when test="string-length(doc)>0">
                                <xsl:call-template name="fixLinks">
                                    <xsl:with-param name="rawString" select="doc"/>
                                </xsl:call-template>
                            </xsl:when>
                            <xsl:otherwise>
                                FIXME... Parameter description not available.
                            </xsl:otherwise>
                        </xsl:choose>
                    </td>
                </tr>
                <xsl:if test="@name='views'">
                    <xsl:call-template name="displayViews" />
                </xsl:if>
            </xsl:for-each>
        </table>
    </xsl:template>
    
    <xsl:template name="displayViews">
        <tr>
            <td colspan="2">
                <table>
                    <tr>
                        <td>
                            assessments
                        </td>
                        <td>
                            <p>
                                Returns all assessment data for the specified 
                                student(s). The data includes any 
                                <i>assessment</i> entities needed to understand
                                the requested <i>studentAssessment</i>
                                data. There is no difference in functionality 
                                between the <i>/students</i> and 
                                <i>/sections</i> endpoints.
                            </p>
                            <para>
                                Look for the following in your response body 
                                when adding this view specifier:
                            </para>
                        </td>
                    </tr>
                    <tr>
                       <td colspan="2">
                           <i>Code block here.</i>
                       </td> 
                    </tr>
                    <tr>
                        <td>
                            attendances
                        </td>
                        <td>
                            <p>
                                On the <i>/students</i> endpoint, returns all 
                                attendance data for the specified student(s). 
                                On the <i>/sections</i> endpoint, the query 
                                can be limited by specifying a qualifier. 
                                The format is <i>attendances.X</i>, where 
                                <i>X</i> is a positive integer. With no 
                                qualifier, the default is to return attendance 
                                data for the current session. The qualifier 
                                specifies how many years of attendance history 
                                to return, if available. A value of 1 will 
                                include the current year's data, 2 will 
                                include this year's and last year's data, 3 
                                will include this year's and the previous 
                                two year's data, and so forth.
                            </p>
                            <p>
                                Look for the following in your response body 
                                when adding this view specifier:
                            </p>
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2">
                            <i>Code block here.</i>
                        </td> 
                    </tr>
                    <tr>
                        <td>
                            gradebook
                        </td>
                        <td>
                            <p>
                                Returns grades for the specified student(s).
                            </p>
                            <p>
                                Returns <i>studentGradebookEntry</i> entities 
                                for the specified student(s). On the 
                                <i>/students</i> endpoint, all 
                                <i>studentGradebookEntry</i> entities for the
                                specified student(s) are returned. This 
                                includes all historical
                                <i>studentGradebookEntry</i> entities. On the
                                <i>/sections</i> endpoint,
                                <i>studentGradebookEntry</i> entities for the 
                                section in context are returned for each 
                                student. The data includes any
                                <i>gradebookEntry</i> entities needed to 
                                understand the requested 
                                <i>studentGradebookEntry</i> data.
                            </p>
                            <p>
                                Look for the following in your response body 
                                when adding this view specifier:
                            </p>
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2">
                            <i>Code block here.</i>
                        </td> 
                    </tr>
                    <tr>
                        <td>
                            transcript
                        </td>
                        <td>
                            <p>
                                Returns all entities needed to construct 
                                transcript information for the specified 
                                student(s). There is no difference in 
                                functionality between the 
                                <i>/students</i> and <i>/sections</i> endpoints.
                            </p>
                            <p>
                                Look for the following in your response body 
                                when adding this view specifier:
                            </p>
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2">
                            <i>Code block here.</i>
                        </td> 
                    </tr>
                </table>
            </td>
        </tr>
    </xsl:template>
    
    <xsl:template name="requestBoilerplate">
        <xsl:param name="methodName"/>
        <xsl:choose>
            <xsl:when test="$methodName='GET'">
                    There is no request body for GET. When forming your GET request
                    URI, use REST API's global parameters [[LINK!!!]]
                    and URI patterns [[LINK!!!]].
            </xsl:when>
            <xsl:when test="$methodName='DELETE'">
                    There is no request body for DELETE.
                    For information on forming the DELETE request URI, see
                    <!-- "URI Patterns" link --> [[LINK!!!]].
                    Note that trying to delete a resource that does not exist results
                    in the <i>404 Not Found</i> response code.
            </xsl:when>
            <xsl:when test="$methodName='POST'">
                    The request body for POST must include the required fields 
                    defined in the
                    data model [[LINK!!!]]. To form 
                    the POST request body, package all required and other 
                    desired fields into a conventional JSON document. It should
                    be similar to JSON response bodies displayed when making
                    a GET request. For information on forming the POST request 
                    URI, <!-- "URI Patterns" link --> [[LINK!!!]].
            </xsl:when>
            <xsl:when test="$methodName='PUT'">
                    The request body for PUT must include the data for the 
                    standard fields of the entire resource, not just the fields
                    you're updating. To form the PUT request body, we recommend
                    that you start with a GET response body for the resource 
                    you're updating, remove the metadata and links, and edit 
                    the values for each field you want to update. View a sample
                    GET response body for the resource using the link in the
                    GET method description here. 
                    For information on forming the PUT request URI, see 
                    <!-- "URI Patterns" link --> [[LINK!!!]].
                    Note that trying to update a resource that does not exist 
                    results in the <i>404 Not Found</i> response code.
            </xsl:when>
            <xsl:when test="$methodName='PATCH'">
                    The request body for PATCH must includes only the fields 
                    you want to update for that resource. To form the PATCH 
                    request body, we recommend that you start with a GET 
                    response body for the resource you're updating, remove the 
                    metadata and any fields you're not updating, and edit the 
                    values for each field you want to update. View a sample 
                    GET response body for each resources using the link in the
                    GET method description here. [[LINK!!!]]
                    Note that trying to update a resource that does not exist 
                    results in the <i>404 Not Found</i> response code.
            </xsl:when>
            <xsl:otherwise>
                    FIXME... Unexpected method.
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template name="responseBoilerplate">
        <xsl:param name="methodName"/>
        <xsl:choose>
            <xsl:when test="$methodName='GET'">
                    200 OK - The <i>TotalCount</i> 
                    header contains the number of items that were returned. 
                    The response body contains the requested resource 
                    representations, including HATEOAS links to reachable URIs.
            </xsl:when>
            <xsl:when test="$methodName='DELETE'">
                    204 No Content - The response body is empty.
            </xsl:when>
            <xsl:when test="$methodName='POST'">
                    201 Created - The <i>Location</i>
                    header contains the URI of the new resource.
            </xsl:when>
            <xsl:when test="$methodName='PUT'">
                    204 No Content - The response body is empty.
            </xsl:when>
            <xsl:when test="$methodName='PATCH'">
                    204 No Content - The response body is empty.
            </xsl:when>
            <xsl:otherwise>
                    FIXME... Unexpected method.
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
</xsl:stylesheet>