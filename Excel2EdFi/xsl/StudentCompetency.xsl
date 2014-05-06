<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStudentGrade xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<StudentCompetency>
					<LearningObjectiveReference>
						<LearningObjectiveIdentity>
							<Objective>
								<xsl:value-of select="LearningObjectiveReference.Objective"/>
							</Objective>
							<AcademicSubject>
								<xsl:value-of select="LearningObjectiveReference.AcademicSubject"/>
							</AcademicSubject>
							<ObjectiveGradeLevel>
								<xsl:value-of select="LearningObjectiveReference.ObjectiveGradeLevel"/>
							</ObjectiveGradeLevel>
						</LearningObjectiveIdentity>
					</LearningObjectiveReference>
					<CompetencyLevel>
						<CodeValue>
							<xsl:value-of select="CompetencyLevel.CodeValue"/>
						</CodeValue>
					</CompetencyLevel>
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
				</StudentCompetency>
			</xsl:for-each> 
		</InterchangeStudentGrade>
	</xsl:template>
</xsl:stylesheet>