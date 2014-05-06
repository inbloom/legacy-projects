<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeAssessmentMetadata xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<AssessmentPeriodDescriptor>
					<CodeValue>
						<xsl:value-of select="CodeValue"/>
					</CodeValue>
					<Description>
						<xsl:value-of select="Description"/>
					</Description>
					<ShortDescription>
						<xsl:value-of select="ShortDescription"/>
					</ShortDescription>
					<BeginDate>
						<xsl:value-of select="BeginDate"/>
					</BeginDate>
					<EndDate>
						<xsl:value-of select="EndDate"/>
					</EndDate>
				</AssessmentPeriodDescriptor>
			</xsl:for-each>
		</InterchangeAssessmentMetadata>
	</xsl:template>
</xsl:stylesheet>