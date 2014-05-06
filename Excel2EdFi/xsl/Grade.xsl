<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStudentGrade xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row"> 
				<Grade>
					<LetterGradeEarned>
						<xsl:value-of select="LetterGradeEarned"/>
					</LetterGradeEarned>
					<GradeType>
						<xsl:value-of select="GradeType"/>
					</GradeType>
					<StudentSectionAssociationReference>
						<StudentSectionAssociationIdentity>
							<StudentReference>
								<StudentIdentity>
									<StudentUniqueStateId>
										<xsl:value-of select="StudentSectionAssociationReference.StudentUniqueStateId"/>
									</StudentUniqueStateId>
								</StudentIdentity>
							</StudentReference>
							<SectionReference>
								<SectionIdentity>
									<EducationalOrgReference>
										<EducationalOrgIdentity>
											<StateOrganizationId>
												<xsl:value-of select="StudentSectionAssociationReference.StateOrganizationId"/>
											</StateOrganizationId>
										</EducationalOrgIdentity>
									</EducationalOrgReference>
									<UniqueSectionCode>
										<xsl:value-of select="StudentSectionAssociationReference.UniqueSectionCode"/>
									</UniqueSectionCode>
								</SectionIdentity>
							</SectionReference>
							<BeginDate>
								<xsl:value-of select="StudentSectionAssociationReference.BeginDate"/>
							</BeginDate>
						</StudentSectionAssociationIdentity>
					</StudentSectionAssociationReference>
					<GradingPeriodReference>
						<GradingPeriodIdentity>
							<EducationalOrgReference>
								<EducationalOrgIdentity>
									<StateOrganizationId>
										<xsl:value-of select="GradingPeriodReference.StateOrganizationId"/>
									</StateOrganizationId>
								</EducationalOrgIdentity>
							</EducationalOrgReference>
							<GradingPeriod>
								<xsl:value-of select="GradingPeriodReference.GradingPeriod"/>
							</GradingPeriod>
							<BeginDate>
								<xsl:value-of select="GradingPeriodReference.BeginDate"/>
							</BeginDate>
						</GradingPeriodIdentity>
					</GradingPeriodReference>
					<SchoolYear>
						<xsl:value-of select="SchoolYear"/>
					</SchoolYear>
				</Grade>
			</xsl:for-each> 
		</InterchangeStudentGrade>
	</xsl:template>
</xsl:stylesheet>