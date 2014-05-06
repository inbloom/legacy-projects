<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStudentAssessment xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<StudentObjectiveAssessment>
					<ScoreResults AssessmentReportingMethod="{ScoreResults.AssessmentReportingMethod}">
						<Result>
							<xsl:value-of select="ScoreResults.Result"/>
						</Result>
					</ScoreResults>
					<StudentAssessmentReference>
						<StudentAssessmentIdentity>
							<AdministrationDate>
								<xsl:value-of select="StudentAssessmentReference.AdministrationDate"/>
							</AdministrationDate>
							<StudentReference>
								<StudentIdentity>
									<StudentUniqueStateId>
										<xsl:value-of select="StudentAssessmentReference.StudentUniqueStateId"/>
									</StudentUniqueStateId>
								</StudentIdentity>
							</StudentReference>
							<AssessmentReference>
								<AssessmentIdentity>
									<AssessmentTitle>
										<xsl:value-of select="StudentAssessmentReference.AssessmentTitle"/>
									</AssessmentTitle>
									<GradeLevelAssessed>
										<xsl:value-of select="StudentAssessmentReference.GradeLevelAssessed"/>
									</GradeLevelAssessed>
									<Version>
										<xsl:value-of select="StudentAssessmentReference.Version"/>
									</Version>
								</AssessmentIdentity>
							</AssessmentReference>
						</StudentAssessmentIdentity>
					</StudentAssessmentReference>
					<ObjectiveAssessmentReference>
						<ObjectiveAssessmentIdentity>
							<ObjectiveAssessmentIdentificationCode>
								<xsl:value-of select="ObjectiveAssessmentReference.ObjectiveAssessmentIdentificationCode"/>
							</ObjectiveAssessmentIdentificationCode>
						</ObjectiveAssessmentIdentity>
					</ObjectiveAssessmentReference>
				</StudentObjectiveAssessment>
			</xsl:for-each>
		</InterchangeStudentAssessment>
	</xsl:template>
</xsl:stylesheet>