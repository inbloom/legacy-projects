<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStudentGrade xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">  
				<CourseTranscript>
					<CourseAttemptResult>Pass</CourseAttemptResult>
					<CreditsEarned CreditConversion="0" CreditType="Semester hour credit">
						<Credit>1</Credit>
					</CreditsEarned>
					<GradeLevelWhenTaken>Fourth grade</GradeLevelWhenTaken>
					<FinalLetterGradeEarned>A-</FinalLetterGradeEarned>
					<CourseReference>
						<CourseIdentity>
							<EducationalOrgReference>
								<EducationalOrgIdentity>
									<StateOrganizationId>South Daybreak Elementary</StateOrganizationId>
								</EducationalOrgIdentity>
							</EducationalOrgReference>
							<UniqueCourseId>Phys-Ed-4A-95</UniqueCourseId>
						</CourseIdentity>
					</CourseReference>
					<EducationOrganizationReference>
						<EducationalOrgIdentity>
							<StateOrganizationId>South Daybreak Elementary</StateOrganizationId>
						</EducationalOrgIdentity>
					</EducationOrganizationReference>
					<StudentAcademicRecordReference>
						<StudentAcademicRecordIdentity>
							<StudentReference>
								<StudentIdentity>
									<StudentUniqueStateId>800000025</StudentUniqueStateId>
								</StudentIdentity>
							</StudentReference>
							<SessionReference>
								<SessionIdentity>
									<EducationalOrgReference>
										<EducationalOrgIdentity>
											<StateOrganizationId>South Daybreak Elementary</StateOrganizationId>
										</EducationalOrgIdentity>
									</EducationalOrgReference>
									<SessionName>Fall 2007 South Daybreak Elementary</SessionName>
								</SessionIdentity>
							</SessionReference>
							<SchoolYear>2009-2010</SchoolYear>
						</StudentAcademicRecordIdentity>
					</StudentAcademicRecordReference>
				</CourseTranscript>
			</xsl:for-each> 
		</InterchangeStudentGrade>
	</xsl:template>
</xsl:stylesheet>