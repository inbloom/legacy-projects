<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeAssessmentMetadata xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<Assessment>
					<AssessmentTitle>
						<xsl:value-of select="AssessmentTitle"/>
					</AssessmentTitle>
					<AssessmentIdentificationCode IdentificationSystem="{AssessmentIdentificationCode.IdentificationSystem}">
						<ID>
							<xsl:value-of select="AssessmentIdentificationCode.ID"/>
						</ID>
					</AssessmentIdentificationCode>
					<AssessmentCategory>
						<xsl:value-of select="AssessmentCategory"/>
					</AssessmentCategory>
					<GradeLevelAssessed>
						<xsl:value-of select="GradeLevelAssessed"/>
					</GradeLevelAssessed>
					<Version>
						<xsl:value-of select="Version"/>
					</Version>
					<RevisionDate>
						<xsl:value-of select="RevisionDate"/>
					</RevisionDate>
					<MaxRawScore>
						<xsl:value-of select="MaxRawScore"/>
					</MaxRawScore>
					<AssessmentItemReference>
						<AssessmentItemIdentity>
							<AssessmentItemIdentificationCode>
								<xsl:value-of select="AssessmentItemReference.AssessmentItemIdentificationCode"/>
							</AssessmentItemIdentificationCode>
						</AssessmentItemIdentity>
					</AssessmentItemReference>
					<ObjectiveAssessmentReference>
						<ObjectiveAssessmentIdentity>
							<ObjectiveAssessmentIdentificationCode>
								<xsl:value-of select="ObjectiveAssessmentReference.ObjectiveAssessmentIdentificationCode"/>
							</ObjectiveAssessmentIdentificationCode>
						</ObjectiveAssessmentIdentity>
					</ObjectiveAssessmentReference>
					<AssessmentFamilyReference>
						<AssessmentFamilyIdentity>
							<AssessmentFamilyTitle>
								<xsl:value-of select="AssessmentFamilyReference.AssessmentFamilyTitle"/>
							</AssessmentFamilyTitle>
						</AssessmentFamilyIdentity>
					</AssessmentFamilyReference>
				</Assessment>
			</xsl:for-each>
		</InterchangeAssessmentMetadata>
	</xsl:template>
</xsl:stylesheet>