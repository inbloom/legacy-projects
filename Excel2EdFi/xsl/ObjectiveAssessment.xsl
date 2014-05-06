<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeAssessmentMetadata xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<ObjectiveAssessment>
					<IdentificationCode>
						<xsl:value-of select="IdentificationCode"/>
					</IdentificationCode>
					<MaxRawScore>
						<xsl:value-of select="MaxRawScore"/>
					</MaxRawScore>
					<ObjectiveAssessmentReference>
						<ObjectiveAssessmentIdentity>
							<ObjectiveAssessmentIdentificationCode>
								<xsl:value-of select="ObjectiveAssessmentReference.ObjectiveAssessmentIdentificationCode"/>
							</ObjectiveAssessmentIdentificationCode>
						</ObjectiveAssessmentIdentity>
					</ObjectiveAssessmentReference>
					<AssessmentReference>
						<AssessmentIdentity>
							<AssessmentTitle>
								<xsl:value-of select="AssessmentReference.AssessmentTitle"/>
							</AssessmentTitle>
							<GradeLevelAssessed>
								<xsl:value-of select="AssessmentReference.GradeLevelAssessed"/>
							</GradeLevelAssessed>
							<Version>
								<xsl:value-of select="AssessmentReference.Version"/>
							</Version>
						</AssessmentIdentity>
					</AssessmentReference>
				</ObjectiveAssessment>
			</xsl:for-each>
		</InterchangeAssessmentMetadata>
	</xsl:template>
</xsl:stylesheet>