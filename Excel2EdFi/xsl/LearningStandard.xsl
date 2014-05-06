<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeAssessmentMetadata xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<LearningStandard>
					<LearningStandardId>
						<IdentificationCode>
							<xsl:value-of select="LearningStandardId.IdentificationCode"/>
						</IdentificationCode>
					</LearningStandardId>
					<Description>
						<xsl:value-of select="Description"/>
					</Description>
					<ContentStandard>
						<xsl:value-of select="ContentStandard"/>
					</ContentStandard>
					<GradeLevel>
						<xsl:value-of select="GradeLevel"/>
					</GradeLevel>
					<SubjectArea>
						<xsl:value-of select="SubjectArea"/>
					</SubjectArea>
					<CourseTitle>
						<xsl:value-of select="CourseTitle"/>
					</CourseTitle>
				</LearningStandard>
			</xsl:for-each>
		</InterchangeAssessmentMetadata>
	</xsl:template>
</xsl:stylesheet>