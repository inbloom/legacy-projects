<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStudentGrade xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">  
				<CourseTranscript>
					<CourseAttemptResult>
						<xsl:value-of select="CourseAttemptResult"/>
					</CourseAttemptResult>
					<CreditsEarned CreditConversion="{CreditsEarned.CreditConversion}" CreditType="{CreditsEarned.CreditType}">
						<Credit>
							<xsl:value-of select="CreditsEarned.Credit"/>
						</Credit>
					</CreditsEarned>
					<GradeLevelWhenTaken>
						<xsl:value-of select="GradeLevelWhenTaken"/>
					</GradeLevelWhenTaken>
					<FinalLetterGradeEarned>
						<xsl:value-of select="FinalLetterGradeEarned"/>
					</FinalLetterGradeEarned>
					<FinalNumericGradeEarned>
						<xsl:value-of select="FinalNumericGradeEarned"/>
					</FinalNumericGradeEarned>
					<CourseReference>
						<CourseIdentity>
							<EducationalOrgReference>
								<EducationalOrgIdentity>
									<StateOrganizationId>
										<xsl:value-of select="CourseReference.StateOrganizationId"/>
									</StateOrganizationId>
								</EducationalOrgIdentity>
							</EducationalOrgReference>
							<UniqueCourseId>
								<xsl:value-of select="CourseReference.UniqueCourseId"/>
							</UniqueCourseId>
						</CourseIdentity>
					</CourseReference>
					<EducationOrganizationReference>
						<EducationalOrgIdentity>
							<StateOrganizationId>
								<xsl:value-of select="EducationOrganizationReference.StateOrganizationId"/>
							</StateOrganizationId>
						</EducationalOrgIdentity>
					</EducationOrganizationReference>
					<StudentAcademicRecordReference>
						<StudentAcademicRecordIdentity>
							<StudentReference>
								<StudentIdentity>
									<StudentUniqueStateId>
										<xsl:value-of select="StudentAcademicRecordReference.StudentUniqueStateId"/>
									</StudentUniqueStateId>
								</StudentIdentity>
							</StudentReference>
							<SessionReference>
								<SessionIdentity>
									<EducationalOrgReference>
										<EducationalOrgIdentity>
											<StateOrganizationId>
												<xsl:value-of select="StudentAcademicRecordReference.StateOrganizationId"/>
											</StateOrganizationId>
										</EducationalOrgIdentity>
									</EducationalOrgReference>
									<SessionName>
										<xsl:value-of select="StudentAcademicRecordReference.SessionName"/>
									</SessionName>
								</SessionIdentity>
							</SessionReference>
							<SchoolYear>
								<xsl:value-of select="StudentAcademicRecordReference.SchoolYear"/>
							</SchoolYear>
						</StudentAcademicRecordIdentity>
					</StudentAcademicRecordReference>
				</CourseTranscript>
			</xsl:for-each> 
		</InterchangeStudentGrade>
	</xsl:template>
</xsl:stylesheet>