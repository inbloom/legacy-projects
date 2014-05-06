<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet xmlns="http://docbook.org/ns/docbook"
    xmlns:docbk="http://docbook.org/ns/docbook"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    version="2.0">

    <xsl:output method="xml" indent="yes"/>

    <xsl:variable name="baseUri" select="'https://example.com/api/rest'"/>

    <xsl:template match="/">
        <xsl:result-document href="{'../auto-rest_api_resources-v1.3.xml'}">
            <chapter xml:id="rest_api_resources-data-v1.3"
                xmlns="http://docbook.org/ns/docbook"
                xmlns:xi="http://www.w3.org/2001/XInclude"
                xmlns:xlink="http://www.w3.org/1999/xlink" version="5.0">
                <title>API version 1.3: Data Resources</title>
                <para>
                    These are the resources used when reading and performing
                    CRUD operations on educational data.
                </para>
                <xsl:for-each select="application/resources/resource">
                    <xsl:sort select="@path" order="ascending"/>
                    <xsl:if test="(not(contains(@path,'system')))and(not(contains(@path,'search')))and(not(contains(@path,'bulk')))">
                        <xsl:if test="starts-with(@path,'v1.3')">
                            <xsl:variable name="resourceTitle">
                                <xsl:value-of select="substring-after(@path,'v1.3/')"/>
                            </xsl:variable>
                            <xsl:call-template name="processResourceDetail">
                                <xsl:with-param name="apiVersion">v1.3</xsl:with-param>
                                <xsl:with-param name="resourcePath" select="@path"/>
                                <xsl:with-param name="resourceTitle" select="$resourceTitle"/>
                                <xsl:with-param name="resourceId">
                                    <xsl:call-template name="getId">
                                        <xsl:with-param name="rawString" select="$resourceTitle"/>
                                    </xsl:call-template>
                                </xsl:with-param>
                            </xsl:call-template>
                        </xsl:if>
                    </xsl:if>
                </xsl:for-each>
            </chapter>
        </xsl:result-document>
        
        <xsl:result-document href="{'../auto-rest_api_resources-v1.2.xml'}">
            <chapter xml:id="rest_api_resources-data-v1.2"
                xmlns="http://docbook.org/ns/docbook"
                xmlns:xi="http://www.w3.org/2001/XInclude"
                xmlns:xlink="http://www.w3.org/1999/xlink" version="5.0">
                <title>API version 1.2: Data Resources</title>
                <para>
                    These are the resources used when reading and performing
                    CRUD operations on educational data.
                </para>
                <xsl:for-each select="application/resources/resource">
                    <xsl:sort select="@path" order="ascending"/>
                    <xsl:if test="(not(contains(@path,'system')))and(not(contains(@path,'search')))and(not(contains(@path,'bulk')))">
                        <xsl:if test="starts-with(@path,'v1.2')">
                            <xsl:variable name="resourceTitle">
                                <xsl:value-of select="substring-after(@path,'v1.2/')"/>
                            </xsl:variable>
                            <xsl:call-template name="processResourceDetail">
                                <xsl:with-param name="apiVersion">v1.2</xsl:with-param>
                                <xsl:with-param name="resourcePath" select="@path"/>
                                <xsl:with-param name="resourceTitle" select="$resourceTitle"/>
                                <xsl:with-param name="resourceId">
                                    <xsl:call-template name="getId">
                                        <xsl:with-param name="rawString" select="$resourceTitle"/>
                                    </xsl:call-template>
                                </xsl:with-param>
                            </xsl:call-template>
                        </xsl:if>
                    </xsl:if>
                </xsl:for-each>
            </chapter>
        </xsl:result-document>
        
        <xsl:result-document href="{'../auto-rest_api_resources-v1.1.xml'}">
            <chapter xml:id="rest_api_resources-data-v1.1"
                xmlns="http://docbook.org/ns/docbook"
                xmlns:xi="http://www.w3.org/2001/XInclude"
                xmlns:xlink="http://www.w3.org/1999/xlink" version="5.0">
                <title>API version 1.1: Data Resources</title>
                <para>
                    These are the resources used when reading and performing
                    CRUD operations on educational data.
                </para>
                <xsl:for-each select="application/resources/resource">
                    <xsl:sort select="@path" order="ascending"/>
                    <xsl:if test="(not(contains(@path,'system')))and(not(contains(@path,'search')))and(not(contains(@path,'bulk')))">
                        <xsl:if test="starts-with(@path,'v1.1')">
                            <xsl:variable name="resourceTitle">
                                <xsl:value-of select="substring-after(@path,'v1.1/')"/>
                            </xsl:variable>
                            <xsl:call-template name="processResourceDetail">
                                <xsl:with-param name="apiVersion">v1.1</xsl:with-param>
                                <xsl:with-param name="resourcePath" select="@path"/>
                                <xsl:with-param name="resourceTitle" select="$resourceTitle"/>
                                <xsl:with-param name="resourceId">
                                    <xsl:call-template name="getId">
                                        <xsl:with-param name="rawString" select="$resourceTitle"/>
                                    </xsl:call-template>
                                </xsl:with-param>
                            </xsl:call-template>
                        </xsl:if>
                    </xsl:if>
                </xsl:for-each>
            </chapter>
        </xsl:result-document>
        
        <xsl:result-document href="{'../auto-rest_api_resources-v1.0.xml'}">
            <chapter xml:id="rest_api_resources-data-v1.0"
                xmlns="http://docbook.org/ns/docbook"
                xmlns:xi="http://www.w3.org/2001/XInclude"
                xmlns:xlink="http://www.w3.org/1999/xlink" version="5.0">
                <title>API version 1.0: Data Resources</title>
                <para>
                    These are the resources used when reading and performing
                    CRUD operations on educational data.
                </para>
                <xsl:for-each select="application/resources/resource">
                    <xsl:sort select="@path" order="ascending"/>
                    <xsl:if test="(not(contains(@path,'system')))and(not(contains(@path,'search')))and(not(contains(@path,'bulk')))">
                        <xsl:if test="starts-with(@path,'v1.0')">
                            <xsl:variable name="resourceTitle">
                                <xsl:value-of select="substring-after(@path,'v1.0/')"/>
                            </xsl:variable>
                            <xsl:call-template name="processResourceDetail">
                                <xsl:with-param name="apiVersion">v1.0</xsl:with-param>
                                <xsl:with-param name="resourcePath" select="@path"/>
                                <xsl:with-param name="resourceTitle" select="$resourceTitle"/>
                                <xsl:with-param name="resourceId">
                                    <xsl:call-template name="getId">
                                        <xsl:with-param name="rawString" select="$resourceTitle"/>
                                    </xsl:call-template>
                                </xsl:with-param>
                            </xsl:call-template>
                        </xsl:if>
                    </xsl:if>
                </xsl:for-each>
            </chapter>
        </xsl:result-document>

    </xsl:template>

    <!-- Template for handling the details for each resource listing -->
    <xsl:template name="processResourceDetail">
        <xsl:param name="apiVersion"/>
        <xsl:param name="resourcePath"/>
        <xsl:param name="resourceTitle"/>
        <xsl:param name="resourceId"/>
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
        <xsl:variable name="endpointName">
            <xsl:call-template name="getEndpoint">
                <xsl:with-param name="rawString" select="$resourceTitle"/>
            </xsl:call-template>
        </xsl:variable>
        <sect1 xml:id="sect-{$apiVersion}-{$resourceId}">
            <title>
                <xsl:value-of select="$resourceTitle"/>
            </title>
            <glosslist>
                <xsl:if test="string-length(doc)>0">
                    <glossentry>
                        <glossterm>DESCRIPTION</glossterm>
                        <glossdef>
                            <para>
                                <xsl:call-template name="fixLinks">
                                    <xsl:with-param name="rawString" select="doc"/>
                                </xsl:call-template>
                            </para>
                        </glossdef>
                    </glossentry>
                </xsl:if>
                <glossentry>
                    <glossterm>URL STRUCTURE</glossterm>
                    <glossdef>
                        <para>
                            <emphasis>
                                <xsl:value-of select="$fullResourcePath"/>
                            </emphasis>
                        </para>
                    </glossdef>
                </glossentry>
                <glossentry>
                    <glossterm>AVAILABILITY</glossterm>
                    <glossdef>
                        <xsl:choose>
                            <xsl:when test="availableSince">
                                <para>
                                    Since
                                    <xsl:value-of select="availableSince"/>
                                </para>
                            </xsl:when>
                            <xsl:otherwise>
                                <para>
                                    Since version 1.0 or before
                                </para>
                            </xsl:otherwise>
                        </xsl:choose>
                    </glossdef>
                </glossentry>
                <xsl:if test="deprecatedVersion">
                    <glossentry>
                        <glossterm><emphasis role="bold">DEPRECATED</emphasis></glossterm>
                        <glossdef>
                            <para>
                                Since
                                <xsl:value-of select="deprecatedVersion"/>
                                <xsl:if test="deprecatedReason">
                                    - <xsl:value-of select="deprecatedReason"/>
                                </xsl:if>
                            </para>
                        </glossdef>
                    </glossentry>
                </xsl:if>
                <xsl:if test="param">
                    <xsl:call-template name="getResourceParams">
                        <xsl:with-param name="apiVersion" select="$apiVersion"/>
                        <xsl:with-param name="resourceId" select="$resourceId"/>
                    </xsl:call-template>
                </xsl:if>
            </glosslist>
            <xsl:for-each select="method">
                <xsl:variable name="methodName" select="@name"/>
                <xsl:call-template name="getMethodSection">
                    <xsl:with-param name="apiVersion" select="$apiVersion"/>
                    <xsl:with-param name="methodName" select="$methodName"/>
                    <xsl:with-param name="resourceId" select="$resourceId"/>
                    <xsl:with-param name="resourcePath" select="$resourcePath"/>
                </xsl:call-template>
            </xsl:for-each>
        </sect1>
        <!-- Iterate over child resources -->
        <xsl:for-each select="resource">
            <xsl:sort select="@path" order="ascending"/>
            <xsl:if test="not(contains(@path,'aggregat'))">
                <xsl:call-template name="processResourceDetail">
                    <xsl:with-param name="apiVersion" select="$apiVersion"/>
                    <xsl:with-param name="resourcePath" select="concat($resourcePath,'/',@path)"/>
                    <xsl:with-param name="resourceTitle" select="concat($resourceTitle,'/',@path)"/>
                    <xsl:with-param name="resourceId">
                        <xsl:call-template name="getId">
                            <xsl:with-param name="rawString" select="concat($resourceTitle,'/',@path)"/>
                        </xsl:call-template>
                    </xsl:with-param>
                </xsl:call-template>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>

    <xsl:template name="getMethodSection">
        <xsl:param name="apiVersion"/>
        <xsl:param name="methodName"/>
        <xsl:param name="resourceId"/>
        <xsl:param name="resourcePath"/>
        <glosslist xml:id="{$apiVersion}-{$resourceId}-{$methodName}">
            <glossentry>
                <glossterm>METHOD</glossterm>
                <glossdef>
                    <para>
                        <xsl:value-of select="$methodName"/>
                    </para>
                    <para>
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
                    </para>
                </glossdef>
            </glossentry>
            <xsl:if test="$methodName='GET'">
                <xsl:if test="request/param">
                    <xsl:call-template name="getMethodParams">
                        <xsl:with-param name="apiVersion" select="$apiVersion"/>
                        <xsl:with-param name="resourceId" select="$resourceId"/>
                        <xsl:with-param name="methodName" select="$methodName"/>
                    </xsl:call-template>
                </xsl:if>
            </xsl:if>
            <glossentry>
                <glossterm>REQUEST</glossterm>
                <glossdef>
                    <xsl:call-template name="requestBoilerplate">
                        <xsl:with-param name="methodName" select="$methodName"/>
                    </xsl:call-template>
                </glossdef>
            </glossentry>
            <glossentry>
                <glossterm>RESPONSE</glossterm>
                <glossdef>
                    <xsl:call-template name="responseBoilerplate">
                        <xsl:with-param name="methodName" select="$methodName"/>
                    </xsl:call-template>
                </glossdef>
            </glossentry>
            <xsl:if test="$methodName='GET'">
                <xsl:choose>
                    <xsl:when test="contains($resourcePath,'v1') and not(contains($resourcePath,'system'))">
                        <xsl:call-template name="getExampleBlock">
                            <xsl:with-param name="apiVersion" select="$apiVersion"/>
                            <xsl:with-param name="resourceId" select="$resourceId"/>
                        </xsl:call-template>
                        <!-- <xsl:call-template name="getSelectorBlock">
                            <xsl:with-param name="resourceId" select="$resourceId"/>
                        </xsl:call-template> -->
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:call-template name="getSyntaxBlock">
                            <xsl:with-param name="resourceId" select="$resourceId"/>
                        </xsl:call-template>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:if>
        </glosslist>
        <!-- END of method block -->
    </xsl:template>

    <xsl:template name="getResourceParams">
        <xsl:param name="apiVersion" />
        <xsl:param name="resourceId" />
        <glossentry>
            <glossterm>PARAMETERS</glossterm>
            <glossdef>
                <informaltable xml:id="table-{$apiVersion}-{$resourceId}-resource-params">
                    <tgroup cols="2">
                        <colspec colname="firstCol" colwidth="1*"/>
                        <colspec colname="secondCol" colwidth="3*"/>
                        <tbody>
                            <xsl:for-each select="param">
                                <xsl:variable name="paramName" select="@name"/>
                                <row>
                                    <entry>
                                        <para>
                                            <code><xsl:value-of select="$paramName"/></code>
                                        </para>
                                    </entry>
                                    <entry>
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
                                    </entry>
                                </row>
                            </xsl:for-each>
                        </tbody>
                    </tgroup>
                </informaltable>
            </glossdef>
        </glossentry>
    </xsl:template>

    <xsl:template name="getMethodParams">
        <xsl:param name="apiVersion" />
        <xsl:param name="resourceId" />
        <xsl:param name="methodName"/>
        <glossentry>
            <glossterm>PARAMETERS</glossterm>
            <glossdef>
                <informaltable xml:id="table-{$apiVersion}-{$resourceId}-{$methodName}-params">
                    <tgroup cols="2">
                        <colspec colname="firstCol" colwidth="1*"/>
                        <colspec colname="secondCol" colwidth="3*"/>
                        <tbody>
                            <xsl:for-each select="request/param">
                                <xsl:variable name="paramName" select="@name"/>
                                <row>
                                    <entry>
                                        <para>
                                            <code><xsl:value-of select="$paramName"/></code>
                                        </para>
                                    </entry>
                                    <entry>
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
                                    </entry>
                                </row>
                                <xsl:if test="@name='views'">
                                    <xsl:call-template name="displayViews">
                                        <xsl:with-param name="apiVersion" select="$apiVersion"/>
                                        <xsl:with-param name="resourceId" select="$resourceId"/>
                                    </xsl:call-template>
                                </xsl:if>
                            </xsl:for-each>
                        </tbody>
                    </tgroup>
                </informaltable>
            </glossdef>
        </glossentry>
    </xsl:template>

    <xsl:template name="displayViews">
        <xsl:param name="apiVersion" />
        <xsl:param name="resourceId"/>
        <row>
            <entry namest="firstCol" nameend="secondCol">
                <informaltable xml:id="table-views-{$apiVersion}-{$resourceId}">
                    <tgroup cols="2">
                        <colspec colname="firstCol" colwidth="1*"/>
                        <colspec colname="secondCol" colwidth="3*"/>
                        <tbody>
                            <row>
                                <entry>
                                    <para>
                                        <varname>assessments</varname>
                                    </para>
                                </entry>
                                <entry>
                                    <para>
                                        Returns all assessment data for the specified student(s).
                                        The data includes any <varname>assessment</varname> entities
                                        needed to understand the requested <classname>studentAssessment</classname>
                                        data. There is no difference in functionality between the
                                        <filename>/students</filename> and <filename>/sections</filename> endpoints.
                                    </para>
                                    <para>
                                        Look for the following in your response body when adding
                                        this view specifier:
                                    </para>
                                </entry>
                            </row>
                            <row>
                                <entry namest="firstCol" nameend="secondCol">
                                    <programlisting><![CDATA[
 "studentAssessments": [
        {
            "administrationDate": "<date>",
            "administrationEndDate": "<date>",
            "assessmentId": "<id>",
            "assessments": {
                "academicSubject": "<subject>",
                "assessmentCategory": "<category>",
                "assessmentFamilyHierarchyName": "<name>",
                "assessmentIdentificationCode": [
                    {
                        "ID": "<code>",
                        "identificationSystem": "<id system>"
                    }
                ],
                "assessmentPerformanceLevel": [],
                "assessmentPeriodDescriptor": {
                    "beginDate": "<date>",
                    "codeValue": "<value>",
                    "description": "<description>",
                    "endDate": "<date>"
                },
                "assessmentTitle": "<title>",
                "contentStandard": "<standard>",
                "entityType": "assessment",
                "gradeLevelAssessed": "<grade>",
                "id": "<id>",
                "lowestGradeLevelAssessed": "<grade>",
                "maxRawScore": <score>,
                "metaData": {},
                "minRawScore": <score>,
                "objectiveAssessment": [
                    {
                        "identificationCode": "<code>",
                        "maxRawScore": <score>,
                        "percentOfAssessment": <percentage>
                    },
                    …
                ],
                "version": <version>
            },
            "entityType": "studentAssessmentAssociation",
            "gradeLevelWhenAssessed": "<grade>",
            "id": "<id>",
            "metaData": {<metadata>},
            "performanceLevelDescriptors": [<descriptors>],
            "retestIndicator": "<data>",
            "scoreResults": [
                {
                    "assessmentReportingMethod": "<method>",
                    "result": "<score>"
                },
                …
            ],
            "studentId": "<id>",
            "studentObjectiveAssessments": [
                {
                    "objectiveAssessment": {
                        "identificationCode": "<code>"
                    },
                    "scoreResults": [
                        {
                            "assessmentReportingMethod": "<method>",
                            "result": "<score>"
                        },
                        …
                    ]
                },
…
            ]
                                                 }
                                              ],
                     ]]></programlisting>
                                </entry>
                            </row>
                            <row>
                                <entry>
                                    <para>
                                        <varname>attendances</varname>
                                    </para>
                                </entry>
                                <entry>
                                    <para>
                                        On the <filename>/students</filename> endpoint, returns all attendance data
                                        for the specified student(s). On the <filename>/sections</filename> endpoint,
                                        the query can be limited by specifying a qualifier. The format is
                                        <code>attendances.X</code>, where <code>X</code> is a positive integer.
                                        With no qualifier, the default is to return attendance data for the current
                                        session. The qualifier specifies how many years of attendance history to
                                        return, if available. A value of 1 will include the current
                                        year's data, 2 will include this year's and last year's data, 3 will include
                                        this year's and the previous two year's data, and so forth.
                                    </para>
                                    <para>
                                        Look for the following in your response body when adding
                                        this view specifier:
                                    </para>
                                </entry>
                            </row>
                            <row>
                                <entry namest="firstCol" nameend="secondCol">
                                    <programlisting><![CDATA[
"attendances": {
        "attendances.1": [
            {
                "date": "<date>",
                "event": "<event>"
            },
…
],
"attendances.2": [
{
     "date": "<date>",
     "event": "<event>"
},
…
        ],
       …
      }
                     ]]></programlisting>
                                </entry>
                            </row>
                            <row>
                                <entry>
                                    <para>
                                        <varname>gradebook</varname>
                                    </para>
                                </entry>
                                <entry>
                                    <para>
                                        Returns grades for the specified student(s).
                                    </para>
                                    <para>
                                        Returns <classname>studentGradebookEntry</classname> entities for
                                        the specified student(s). On the <filename>/students</filename> endpoint,
                                        all <classname>studentGradebookEntry</classname> entities for the
                                        specified student(s) are returned. This includes all historical
                                        <classname>studentGradebookEntry</classname> entities. On the
                                        <filename>/sections</filename> endpoint,
                                        <classname>studentGradebookEntry</classname> entities for the section
                                        in context are returned for each student. The data includes any
                                        <classname>gradebookEntry</classname> entities needed to understand
                                        the requested <classname>studentGradebookEntry</classname> data.
                                    </para>
                                    <para>
                                        Look for the following in your response body when adding
                                        this view specifier:
                                    </para>
                                </entry>
                            </row>
                            <row>
                                <entry namest="firstCol" nameend="secondCol">
                                    <programlisting><![CDATA[
"studentGradebookEntries": [
        {
            "dateFulfilled": "<date>",
            "diagnosticStatement": "<statement>",
            "entityType": "studentSectionGradebookEntry",
            "gradebookEntries": {
                "dateAssigned": "<date>",
                "entityType": "gradebookEntry",
                "gradebookEntryType": "<type>",
                "id": "<id>",
                "metaData": {},
                "sectionId": "<id>"
            },
            "gradebookEntryId": "<id>",
            "id": "<id>",
            "letterGradeEarned": "<grade>",
            "metaData": {},
            "numericGradeEarned": <grade>,
            "sectionId": "<id>",
            "studentId": "<id>"
        },
                                               …
    ],
                     ]]></programlisting>
                                </entry>
                            </row>
                            <row>
                                <entry>
                                    <para>
                                        <varname>transcript</varname>
                                    </para>
                                </entry>
                                <entry>
                                    <para>
                                        Returns all entities needed to construct transcript information
                                        for the specified student(s). There is no difference in functionality
                                        between the <filename>/students</filename> and
                                        <filename>/sections</filename> endpoints.
                                    </para>
                                    <para>
                                        Look for the following in your response body when adding
                                        this view specifier:
                                    </para>
                                </entry>
                            </row>
                            <row>
                                <entry namest="firstCol" nameend="secondCol">
                                    <programlisting><![CDATA[
"transcript": {
        "courseTranscripts": [
            {
                "courseAttemptResult": "<result>",
                "courseId": "<id>",
                "creditsEarned": {
                    "credit": <credits>
                },
                "entityType": "studentTranscriptAssociation",
                "finalLetterGradeEarned": "<grade>",
                "gradeType": "<type>",
                "id": "<id>",
                "metaData": {},
                "studentAcademicRecordId": "<id>",
                "studentId": "<id>"
            }
        ],
        "studentSectionAssociations": [
            {
                "entityType": "studentSectionAssociation",
                "id": "<id>",
                "metaData": {
                    "created": <date>,
                    "updated": <date>
                },
                "sectionId": "<id>",
                "sections": {
                    "availableCredit": <credit>,
                    "courseId": "<id>",
                    "courses": {
                        "careerPathway": "<pathway>",
                        "courseCode": [
                            {
                                "ID": "<id>",
                                "assigningOrganizationCode": "<code>",
                                "identificationSystem": "<id system>"
                            }
                        ],
                        "courseDefinedBy": "<organization type>",
                        "courseDescription": "<description>",
                        "courseLevel": "<level>",
                        "courseLevelCharacteristics": [
                            "<characteristic>",
                             …
                        ],
                        "courseTitle": "<title>",
                        "dateCourseAdopted": "<date>",
                        "entityType": "course",
                        "highSchoolCourseRequirement": <requirement>,
                        "id": "<id>",
                        "metaData": {},
                        "numberOfParts": <parts>,
                        "subjectArea": "<subject>"
                    },
                    "educationalEnvironment": "<environment>",
                    "entityType": "section",
                    "id": "<id>",
                    "mediumOfInstruction": "<medium>",
                    "metaData": {
                        "created": <date>,
                        "externalId": "<id>",
                        "updated": <date>
                    },
                    "populationServed": "<population>",
                    "programReference": [
                        "<id>"
                    ],
                    "schoolId": "<id>",
                    "sequenceOfCourse": <sequence>,
                    "sessionId": "<id>",
                    "sessions": {
                        "beginDate": "<date>",
                        "endDate": "<date>",
                        "entityType": "session",
                        "gradingPeriodReference": [
                            "<id>",
                            …
                        ],
                        "id": "<id>",
                        "metaData": {},
                        "schoolYear": "<school year>",
                        "sessionName": "<name>",
                        "term": "<term>",
                        "totalInstructionalDays": <days>
                    },
                    "uniqueSectionCode": "<code>"
                },
                "studentId": "<id>"
            },
            …
        ]
    }
                     ]]></programlisting>
                                </entry>
                            </row>
                        </tbody>
                    </tgroup>
                </informaltable>
            </entry>
        </row>
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

    <xsl:template name="getEndpoint">
        <xsl:param name="rawString"/>
        <xsl:choose>
            <xsl:when test="contains($rawString,'/')">
                <xsl:call-template name="getEndpoint">
                    <xsl:with-param name="rawString" select="substring-after($rawString,'/')"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="contains($rawString,'{')">
                <xsl:call-template name="getEndpoint">
                    <xsl:with-param name="rawString" select="translate($rawString,'{','')"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="contains($rawString,'}')">
                <xsl:call-template name="getEndpoint">
                    <xsl:with-param name="rawString" select="translate($rawString,'}','')"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$rawString"/>
            </xsl:otherwise>
        </xsl:choose>
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
        <link xlink:show="embed" xlink:href="{$modelEntityFile}#type-{$modelEntity}"><xsl:value-of select="$modelEntity"/></link>
    </xsl:template>

    <xsl:template name="requestBoilerplate">
        <xsl:param name="methodName"/>
        <xsl:choose>
            <xsl:when test="$methodName='GET'">
                <para>
                    There is no request body for GET. When forming your GET request
                    URI, use REST API's
                    <link linkend="doc-5ee14672-28bd-487e-b6a5-51570151a92e">global parameters</link>
                    and
                    <link linkend="doc-0be599ab-0a18-439f-87b2-3313a5e77793">URI patterns</link>.
                </para>
            </xsl:when>
            <xsl:when test="$methodName='DELETE'">
                <para>
                    There is no request body for DELETE.
                    For information on forming the DELETE request URI, see
                    <!-- "URI Patterns" link -->
                    <xref linkend="doc-0be599ab-0a18-439f-87b2-3313a5e77793"/>.
                    Note that trying to delete a resource that does not exist results
                    in the <code>404 Not Found</code> response code.
                </para>
            </xsl:when>
            <xsl:when test="$methodName='POST'">
                <para>
                    The request body for POST must include the required fields 
                    defined in the
                    <link linkend="data_model">data model</link>. To form 
                    the POST request body, package all required and other 
                    desired fields into a conventional JSON document. It should
                    be similar to JSON response bodies displayed when making
                    a GET request. For information on forming the POST request 
                    URI, <!-- "URI Patterns" link -->
                    <xref linkend="doc-0be599ab-0a18-439f-87b2-3313a5e77793"/>.
                </para>
            </xsl:when>
            <xsl:when test="$methodName='PUT'">
                <para>
                    The request body for PUT must include the data for the 
                    standard fields of the entire resource, not just the fields
                    you're updating. To form the PUT request body, we recommend
                    that you start with a GET response body for the resource 
                    you're updating, remove the metadata and links, and edit 
                    the values for each field you want to update. View a sample
                    GET response body for the resource using the link in the
                    GET method description here. 
                    For information on forming the PUT request URI, see 
                    <!-- "URI Patterns" link -->
                    <xref linkend="doc-0be599ab-0a18-439f-87b2-3313a5e77793"/>.
                    Note that trying to update a resource that does not exist 
                    results in the <code>404 Not Found</code> response code.
                </para>
            </xsl:when>
            <xsl:when test="$methodName='PATCH'">
                <para>
                    The request body for PATCH must includes only the fields 
                    you want to update for that resource. To form the PATCH 
                    request body, we recommend that you start with a GET 
                    response body for the resource you're updating, remove the 
                    metadata and any fields you're not updating, and edit the 
                    values for each field you want to update. View a sample 
                    GET response body for each resources using the link in the
                    GET method description here. 
                    <!-- "URI Patterns" link -->
                    <xref linkend="doc-0be599ab-0a18-439f-87b2-3313a5e77793"/>.
                    Note that trying to update a resource that does not exist 
                    results in the <code>404 Not Found</code> response code.
                </para>
            </xsl:when>
            <xsl:otherwise>
                <para>
                    FIXME... Unexpected method.
                </para>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template name="responseBoilerplate">
        <xsl:param name="methodName"/>
        <xsl:choose>
            <xsl:when test="$methodName='GET'">
                <para>
                    <code>200 OK</code> - The <emphasis>TotalCount</emphasis> 
                    header contains the number of items that were returned. 
                    The response body contains the requested resource 
                    representations, including HATEOAS links to reachable URIs.
                </para>
            </xsl:when>
            <xsl:when test="$methodName='DELETE'">
                <para>
                    <code>204 No Content</code> - The response body is empty.
                </para>
            </xsl:when>
            <xsl:when test="$methodName='POST'">
                <para>
                    <code>201 Created</code> - The <varname>Location</varname>
                    header contains the URI of the new resource.
                </para>
            </xsl:when>
            <xsl:when test="$methodName='PUT'">
                <para>
                    <code>204 No Content</code> - The response body is empty.
                </para>
            </xsl:when>
            <xsl:when test="$methodName='PATCH'">
                <para>
                    <code>204 No Content</code> - The response body is empty.
                </para>
            </xsl:when>
            <xsl:otherwise>
                <para>
                    FIXME... Unexpected method.
                </para>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template name="getExampleBlock">
        <xsl:param name="apiVersion"/>
        <xsl:param name="resourceId"/>
        <xsl:param name="examplesFilename" select="concat('../modules/autogenerated/auto-examples-',$apiVersion,'.xml')"/>
        <xsl:choose>
            <xsl:when test="contains($resourceId,'custom')"/>
            <xsl:otherwise>
                <xsl:variable name="exampleFileTargetSection" select="concat('ex-',$resourceId)"/>
                <xsl:variable name="exampleFileContents">
                    <xsl:value-of select="document($examplesFilename)/docbk:chapter/docbk:simplesect[@xml:id=$exampleFileTargetSection]"/>
                </xsl:variable>
                <xsl:if test="$exampleFileContents">
                    <glossentry>
                        <glossterm/>
                        <glossdef>
                            <para>
                                <link linkend="ex-{$apiVersion}-{$resourceId}">
                                    View example GET request and response
                                </link>
                            </para>
                        </glossdef>
                    </glossentry>
                </xsl:if>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <!-- <xsl:template name="getSelectorBlock">
        <xsl:param name="resourceId" />
        <xsl:choose>
            <xsl:when test="contains($resourceId,'custom')"/>
            <xsl:otherwise>
                <xsl:variable name="exampleFileTargetSection" select="concat('sel-',$resourceId)"/>
                <xsl:variable name="exampleFileContents">
                    <xsl:value-of select="document('ch-selectors.xml')/docbk:chapter/docbk:simplesect[@xml:id=$exampleFileTargetSection]"/>
                </xsl:variable>
                <xsl:if test="$exampleFileContents">
                    <glossentry>
                        <glossterm/>
                        <glossdef>
                            <para>
                                <link linkend="$exampleFileTargetSelection">
                                    View all the selectors you can use with this GET method
                                </link>
                            </para>
                        </glossdef>
                    </glossentry>
                </xsl:if>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template> -->
    
    <xsl:template name="getSyntaxBlock">
        <xsl:param name="resourceId" />
        <xsl:variable name="fileTargetSection" select="concat('ex-',$resourceId)"/>
        <xsl:variable name="fileContents">
            <xsl:value-of select="document('ch-syntaxes.xml')/docbk:chapter/docbk:simplesect[@xml:id=$fileTargetSection]"/>
        </xsl:variable>
        <xsl:if test="$fileContents">
            <glossentry>
                <glossterm/>
                <glossdef>
                    <para>
                        <link linkend="ex-{$resourceId}">
                            View syntax to expect for a successful GET response
                        </link>
                    </para>
                </glossdef>
            </glossentry>
        </xsl:if>
    </xsl:template>

</xsl:stylesheet>
