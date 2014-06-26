<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStudentAssessment xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<StudentAssessment>
					<AdministrationDate>
						<xsl:value-of select="AdministrationDate"/>
					</AdministrationDate>
					<AdministrationEndDate>
						<xsl:value-of select="AdministrationEndDate"/>
					</AdministrationEndDate>
					<SerialNumber>
						<xsl:value-of select="SerialNumber"/>
					</SerialNumber>
					<AdministrationLanguage>
						<xsl:value-of select="AdministrationLanguage"/>
					</AdministrationLanguage>
					<AdministrationEnvironment>
						<xsl:value-of select="AdministrationEnvironment"/>
					</AdministrationEnvironment>
					<RetestIndicator>
						<xsl:value-of select="RetestIndicator"/>
					</RetestIndicator>
					<ScoreResults AssessmentReportingMethod="{ScoreResults.AssessmentReportingMethod}">
						<Result>
							<xsl:value-of select="ScoreResults.Result"/>
						</Result>
					</ScoreResults>
					<GradeLevelWhenAssessed>
						<xsl:value-of select="GradeLevelWhenAssessed"/>
					</GradeLevelWhenAssessed>
					<StudentReference>
						<StudentIdentity>
							<StudentUniqueStateId>
								<xsl:value-of select="StudentReference.StudentUniqueStateId"/>
							</StudentUniqueStateId>
						</StudentIdentity>
					</StudentReference>
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
				</StudentAssessment>
			</xsl:for-each>
		</InterchangeStudentAssessment>
	</xsl:template>
</xsl:stylesheet>