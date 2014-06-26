<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeAssessmentMetadata xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<LearningObjective>
					<LearningObjectiveId>
						<IdentificationCode>
							<xsl:value-of select="LearningObjectiveId.IdentificationCode"/>
						</IdentificationCode>
					</LearningObjectiveId>
					<Objective>
						<xsl:value-of select="Objective"/>
					</Objective>
					<AcademicSubject>
						<xsl:value-of select="AcademicSubject"/>
					</AcademicSubject>
					<ObjectiveGradeLevel>
						<xsl:value-of select="ObjectiveGradeLevel"/>
					</ObjectiveGradeLevel>
					<LearningStandardReference>
						<LearningStandardIdentity>
							<IdentificationCode>
								<xsl:value-of select="LearningStandardReference.IdentificationCode"/>
							</IdentificationCode>
						</LearningStandardIdentity>
					</LearningStandardReference>
				</LearningObjective>
			</xsl:for-each>
		</InterchangeAssessmentMetadata>
	</xsl:template>
</xsl:stylesheet>