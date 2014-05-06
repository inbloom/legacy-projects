<?xml version="1.0" encoding="UTF-8"?>

<!DOCTYPE book [
<!ENTITY % entities SYSTEM "entities.ent">
%entities;
]>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:xs="http://www.w3.org/2001/XMLSchema" 
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns="http://docbook.org/ns/docbook" version="1.0">
    
    <xsl:output method="xml" indent="yes"/>
    
    <xsl:template match="/">
        <part xml:id="data_model"
            xmlns="http://docbook.org/ns/docbook" 
            xmlns:xi="http://www.w3.org/2001/XInclude"
            xmlns:xlink="http://www.w3.org/1999/xlink" version="5.0">
            
            <info>
                <title>&DATAMODEL;</title>
            </info>
            
            <preface xml:id="data_model-intro">
                <title>Introduction to the &DATAMODEL;</title>
                <para>
                    This portion of &COMPANYABBR; documentation describes the
                    data model for the &COMPANYABBR; data store. We've organized
                    this document as follows:
                </para>
                <itemizedlist>
                    <listitem>
                        <para>
                            First is a catalog of "data domains," which are virtual
                            groups of interdependent data related by some common
                            real-world scenario. Domains can help you visualize
                            why certain data has certain relationships. Each domain
                            includes a diagram and a list of entities. Each entity
                            links to its corresponding section in the chapter
                            that follows.
                        </para>
                    </listitem>
                    <listitem>
                        <para>
                            Second is a catalog of the entities in the data store,
                            each with its corresponding list of attributes, references,
                            and associations. Each reference and association links
                            to its corresponding entity, and each attribute links
                            to an enumeration or data type in the chapters that follow.
                        </para>
                        <para>
                            The term "entity" refers to the entity component of 
                            the industry standard entity-attribute-value model (EAV)
                            when describing data models. When working with the
                            &RESTAPI;, note that each entity in the data store 
                            corresponds to a
                            <glossterm linkend="def-resource">resource</glossterm>
                            in the REST API.
                        </para>
                    </listitem>
                    <listitem>
                        <para>
                            Third is a catalog of the enumerations in the data store,
                            with each data object in the enumeration linked back to
                            its data type. These data types are linked to its
                            corresponding listing either in the chapter that follows 
                            or in the W3C standards document
                            <link xlink:show="new" xlink:href="http://www.w3.org/TR/xmlschema-2/"><citetitle>XML Schema Part 2: Datatypes Second Edition</citetitle></link>.
                        </para>
                    </listitem>
                    <listitem>
                        <para>
                            Fourth is a table of the data types used throughout the
                            data store other than the enumerations previously listed.
                            These data types are described in terms of the primitive
                            data types and linked to corresponding sections in the 
                            W3C standards document
                            <link xlink:show="new" xlink:href="http://www.w3.org/TR/xmlschema-2/"><citetitle>XML Schema Part 2: Datatypes Second Edition</citetitle></link>.
                        </para>
                    </listitem>
                </itemizedlist>
            </preface>
            
            <xsl:for-each select="domains">
            
            <chapter xml:id="data_model-domains">
                <title>Data Domains</title>
                <para>
                    The &DATAMODEL;
                </para>
                    <xsl:for-each select="domain">
                        <xsl:sort select="title" order="ascending"/>
                        <xsl:variable name="domainName">
                            <xsl:value-of select="title"/> Domain
                        </xsl:variable>
                        <xsl:variable name="domainId">
                            <xsl:value-of select="translate(title,' /','')"/>
                        </xsl:variable>
                        <section xml:id="data_model-domains-{$domainId}">
                            <title><xsl:value-of select="$domainName"/></title>
                            <para>
                                <xsl:choose>
                                    <xsl:when test="string-length(description)>1">
                                        <xsl:value-of select="description"/>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        No description available.
                                    </xsl:otherwise>
                                </xsl:choose>
                            </para>
                            <figure xml:id="figure-{$domainId}">
                                <title />
                                <mediaobject>
                                    <imageobject>
                                        <imagedata align="center"
                                            fileref="images/domain-{$domainId}.png"
                                            width="700px" scalefit="1" />
                                    </imageobject>
                                </mediaobject>
                            </figure>
                            <para>
                                <link xlink:show="new" xlink:href="images/domain-{$domainId}.png">View this image at full size</link>
                            </para>
                            <table xml:id="table-{$domainId}">
                                <title>Entities in the <xsl:value-of select="$domainName"/></title>
                                <tgroup cols="2">
                                    <colspec colname="firstCol" colwidth="1"/>
                                    <colspec colname="secondCol" colwidth="3"/>
                                    <thead>
                                        <row>
                                            <entry>Entity</entry>
                                            <entry>Description</entry>
                                        </row>
                                    </thead>
                                    <tbody>
                                        <xsl:choose>
                                            <xsl:when test="entity">
                                                <xsl:for-each select="entity">
                                                    <xsl:variable name="entityId">
                                                        <xsl:value-of select="class/@xmi.idref"/>
                                                    </xsl:variable>
                                                    <row>
                                                        <entry>
                                                            <para>
                                                                <link linkend="type-{name}">
                                                                    <xsl:value-of select="name"/>
                                                                </link>
                                                            </para>
                                                        </entry>
                                                        <entry>
                                                            <para>
                                                                <xsl:value-of select="description"/>
                                                            </para>
                                                        </entry>
                                                    </row>
                                                </xsl:for-each>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <row>
                                                    <entry namest="firstCol" nameend="secondCol">
                                                        Class list not available.
                                                    </entry>
                                                </row>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </tbody>
                                </tgroup>
                            </table>
                        </section> 
                    </xsl:for-each>
            </chapter>  <!-- end of "domains" chapter -->
            
            <chapter xml:id="data_model-entities">
                <title>Entities</title>
                <xsl:for-each select="class">
                    <xsl:sort select="name" order="ascending"/>
                    <xsl:variable name="entityName">
                        <xsl:value-of select="name"/>
                    </xsl:variable>
                    <xsl:variable name="entityId">
                        <xsl:value-of select="translate(name,' /','')"/>
                    </xsl:variable>
                    <section xml:id="type-{$entityId}">
                        <title><xsl:value-of select="$entityName"/></title>
                        <xsl:if test="generalization/name">
                            <para>
                                Derived from type 
                                <link linkend="type-{generalization/name}"><xsl:value-of select="generalization/name"/></link>.
                            </para>
                        </xsl:if>
                        <para>
                            <xsl:value-of select="description"/>
                        </para>
                        <xsl:choose>
                            <xsl:when test="feature">
                                <table xml:id="table-entity-{$entityId}-features">
                                    <title>Attributes &amp; References for <xsl:value-of select="$entityName"/></title>
                                    <tgroup cols="4">
                                        <colspec colname="firstCol" colwidth="3*"/>
                                        <colspec colname="secondCol" colwidth="1*" align="center"/>
                                        <colspec colname="thirdCol" colwidth="7*"/>
                                        <colspec colname="fourthCol" colwidth="2*" align="center"/>
                                        <colspec colname="fifth" colwidth="3*"/>
                                        <thead>
                                            <row>
                                                <entry>
                                                    Name
                                                </entry>
                                                <entry>
                                                    Key Fields
                                                </entry>
                                                <entry>
                                                    Description
                                                </entry>
                                                <entry>
                                                    Cardinality
                                                </entry>
                                                <entry>
                                                    Type
                                                </entry>
                                            </row>
                                        </thead>
                                        <tbody>
                                            <xsl:for-each select="feature">
                                                <xsl:sort select="@embedded" order="descending"/>
                                                <xsl:sort select="name" order="ascending"/>
                                                <xsl:call-template name="getFeatureRow">
                                                    <xsl:with-param name="name" select="name"/>
                                                    <xsl:with-param name="description" select="description"/>
                                                    <xsl:with-param name="cardinality" select="concat(lower,'..',upper)"/>
                                                    <xsl:with-param name="type" select="type/name"/>
                                                    <xsl:with-param name="embeddedState" select="@embedded"/>
                                                    <xsl:with-param name="naturalKey" select="@naturalKey"/>
                                                </xsl:call-template>
                                            </xsl:for-each>
                                        </tbody>
                                    </tgroup>
                                </table>
                            </xsl:when>
                            <xsl:otherwise>
                                <para>
                                    This entity has no defined attributes or references.
                                </para>
                            </xsl:otherwise>
                        </xsl:choose>
                    </section>
                </xsl:for-each>
            </chapter>  <!-- end of "entities" chapter -->
        
            <chapter xml:id="data_model-enums">
                <title>Enumerations</title>
                <xsl:for-each select="enumeration">
                    <xsl:sort select="name" order="ascending"/>
                    <xsl:variable name="enumId">
                        <xsl:value-of select="translate(name,' /','')"/>
                    </xsl:variable>
                    <section xml:id="type-{$enumId}">
                        <title><xsl:value-of select="name"/></title>
                        <para>
                            <xsl:value-of select="description"/>
                            Like all enumerations in &PRODUCTABBR;, <xsl:value-of select="name"/> 
                            is derived from the W3C data type
                            <link xlink:show="new" xlink:href="http://www.w3.org/TR/xmlschema-2/#token">token</link>.
                        </para>
                        <xsl:choose>
                            <xsl:when test="literal">
                                <itemizedlist>
                                    <xsl:for-each select="literal">
                                        <listitem>
                                            <para>
                                                <xsl:value-of select="@value"/>
                                            </para>
                                        </listitem>
                                    </xsl:for-each>
                                </itemizedlist>
                            </xsl:when>
                        </xsl:choose>
                    </section>
                </xsl:for-each>
            </chapter> <!-- end of "enumeration" level -->
        
            <chapter xml:id="data_model-datatypes">
                <title>Data Types</title>
                <para>
                    The data types listed below are those implemented specifically for the &PRODUCTABBR;.
                    Each of these is derived from one of the W3C data types described in
                    <link xlink:show="new" xlink:href="http://www.w3.org/TR/xmlschema-2/">XML Schema Part 2: Datatypes Second Edition</link>.
                </para>
                <table xml:id="table-devportal-model-datatypes">
                    <title />
                    <tgroup cols="2">
                        <colspec colname="firstCol" colwidth="1*"/>
                        <colspec colname="secondCol" colwidth="3*"/>
                        <thead>
                            <row>
                                <entry>
                                    <para>
                                        Type
                                    </para>
                                </entry>
                                <entry>
                                    <para>
                                        Description
                                    </para>
                                </entry>
                            </row>
                        </thead>
                        <tbody>
                            <xsl:for-each select="datatype">
                                <xsl:sort select="name" order="ascending"/>
                                <xsl:choose>
                                    <xsl:when test="namespace='http://www.w3.org/2001/XMLSchema'"/>
                                    <xsl:otherwise>
                                        <row>
                                            <entry>
                                                <para>
                                                    <phrase xml:id="type-{translate(name,' /','')}">
                                                        <xsl:value-of select="name"/>
                                                    </phrase>
                                                </para>
                                            </entry>
                                            <entry>
                                                <para>
                                                    <xsl:value-of select="description"/>
                                                </para>
                                                <xsl:if test="pattern">
                                                    <para>
                                                        Pattern: <xsl:value-of select="pattern"/>
                                                    </para>
                                                </xsl:if>
                                                <para>
                                                    Derived from 
                                                    <xsl:choose>
                                                        <xsl:when test="generalization">
                                                            <xsl:choose>
                                                                <xsl:when test="generalization/namespace">
                                                                    <xsl:choose>
                                                                        <xsl:when test="contains(generalization/namespace,'www.w3.org/2001/XMLSchema')">
                                                                            <link xlink:show="new" xlink:href="http://www.w3.org/TR/xmlschema-2/#{generalization/name}"><xsl:value-of select="generalization/name"/></link>.
                                                                        </xsl:when>
                                                                        <xsl:otherwise>
                                                                            <link xlink:show="embed" xlink:href="{generalization/namespace}"><xsl:value-of select="generalization/name"/></link>.                                                                            
                                                                        </xsl:otherwise>
                                                                    </xsl:choose>
                                                                </xsl:when>
                                                                <xsl:otherwise>
                                                                    <xsl:value-of select="generalization/name"/>.
                                                                </xsl:otherwise>
                                                            </xsl:choose>
                                                        </xsl:when>
                                                        <xsl:otherwise>
                                                            <link xlink:show="new" xlink:href="http://www.w3.org/TR/xmlschema-2/#string">string</link>.
                                                        </xsl:otherwise>
                                                    </xsl:choose>
                                                </para>
                                                <xsl:if test="minLength">
                                                    <para>
                                                        Length: <xsl:value-of select="minLength"/> to <xsl:value-of select="maxLength"/>
                                                    </para>
                                                </xsl:if>
                                            </entry>
                                        </row>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:for-each>
                        </tbody>
                    </tgroup>
                </table>
            </chapter> <!-- end of "datatype" chapter -->
                
            </xsl:for-each> <!-- end of for loop encasing the entire schema XML content (a single top-level entity "domains") -->
            
        </part>
    </xsl:template>
    
    <xsl:template name="getFeatureRow">
        <xsl:param name="name"/>
        <xsl:param name="description"/>
        <xsl:param name="cardinality"/>
        <xsl:param name="type"/>
        <xsl:param name="embeddedState"/>
        <xsl:param name="naturalKey"/>
        <row>
            <entry>
                <para>
                    <xsl:value-of select="$name"/>
                </para>
            </entry>
            <xsl:choose>
                <xsl:when test="$naturalKey='true'">
                    <entry>
                        <para>
                            Yes
                        </para>
                    </entry>
                </xsl:when>
                <xsl:otherwise>
                    <entry>
                        <para>No</para>
                    </entry>
                </xsl:otherwise>
            </xsl:choose>
            <entry>
                <para>
                    <xsl:value-of select="$description"/>
                </para>
            </entry>
            <entry>
                <xsl:value-of select="$cardinality"/>
            </entry>
            <entry>
                <para>
                    <xsl:choose>
                        <xsl:when test="$embeddedState='true'"/>
                        <xsl:otherwise>
                            <emphasis>Reference to </emphasis>
                        </xsl:otherwise>
                    </xsl:choose>
                    <xsl:choose>
                        <xsl:when test="contains(type/namespace,'www.w3.org/2001/XMLSchema')">
                            <link xlink:show="new" xlink:href="http://www.w3.org/TR/xmlschema-2/#{$type}"><xsl:value-of select="$type"/></link>
                        </xsl:when>
                        <xsl:otherwise>
                            <link linkend="type-{$type}"><xsl:value-of select="$type"/></link>
                        </xsl:otherwise>
                    </xsl:choose>
                </para>
            </entry>
        </row>
    </xsl:template>
    
</xsl:stylesheet>
