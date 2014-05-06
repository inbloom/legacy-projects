<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStudentAssessment xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<StudentAssessmentItem>
					<AssessmentResponse>
						<xsl:value-of select="AssessmentResponse"/>
					</AssessmentResponse>
					<AssessmentItemResult>
						<xsl:value-of select="AssessmentItemResult"/>
					</AssessmentItemResult>
					<RawScoreResult>
						<xsl:value-of select="RawScoreResult"/>
					</RawScoreResult>
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
					<AssessmentItemReference>
						<AssessmentItemIdentity>
							<AssessmentItemIdentificationCode>
								<xsl:value-of select="AssessmentItemReference.AssessmentItemIdentificationCode"/>
							</AssessmentItemIdentificationCode>
						</AssessmentItemIdentity>
					</AssessmentItemReference>
				</StudentAssessmentItem>
			</xsl:for-each>
		</InterchangeStudentAssessment>
	</xsl:template>
</xsl:stylesheet>