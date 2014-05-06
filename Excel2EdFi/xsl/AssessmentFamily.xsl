<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeAssessmentMetadata xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<AssessmentFamily>
					<AssessmentFamilyTitle>
						<xsl:value-of select="AssessmentFamilyTitle"/>
					</AssessmentFamilyTitle>
					<AssessmentFamilyIdentificationCode IdentificationSystem="{AssessmentFamilyIdentificationCode.IdentificationSystem}">
						<ID>
							<xsl:value-of select="AssessmentFamilyIdentificationCode.ID"/>
						</ID>
					</AssessmentFamilyIdentificationCode>
					<AssessmentFamilyReference>
						<AssessmentFamilyIdentity>
							<AssessmentFamilyTitle>
								<xsl:value-of select="AssessmentFamilyReference.AssessmentFamilyTitle"/>
							</AssessmentFamilyTitle>
						</AssessmentFamilyIdentity>
					</AssessmentFamilyReference>
				</AssessmentFamily>
			</xsl:for-each>
		</InterchangeAssessmentMetadata>
	</xsl:template>
</xsl:stylesheet>