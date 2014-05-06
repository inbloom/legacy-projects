<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStudentGrade xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<ReportCard>
					<GradeReference>
						<GradeIdentity>
							<StudentReference>
								<StudentIdentity>
									<StudentUniqueStateId>
										<xsl:value-of select="GradeReference.StudentUniqueStateId"/>
									</StudentUniqueStateId>
								</StudentIdentity>
							</StudentReference>
							<SectionReference>
								<SectionIdentity>
									<EducationalOrgReference>
										<EducationalOrgIdentity>
											<StateOrganizationId>
												<xsl:value-of select="GradeReference.StateOrganizationId"/>
											</StateOrganizationId>
										</EducationalOrgIdentity>
									</EducationalOrgReference>
									<UniqueSectionCode>
										<xsl:value-of select="GradeReference.UniqueSectionCode"/>
									</UniqueSectionCode>
								</SectionIdentity>
							</SectionReference>
							<GradingPeriodReference>
								<GradingPeriodIdentity>
									<EducationalOrgReference>
										<EducationalOrgIdentity>
											<StateOrganizationId>
												<xsl:value-of select="GradeReference.StateOrganizationId"/>
											</StateOrganizationId>
										</EducationalOrgIdentity>
									</EducationalOrgReference>
									<GradingPeriod>
										<xsl:value-of select="GradeReference.GradingPeriod"/>
									</GradingPeriod>
									<BeginDate>
										<xsl:value-of select="GradeReference.BeginDate"/>
									</BeginDate>
								</GradingPeriodIdentity>
							</GradingPeriodReference>
							<SchoolYear>
								<xsl:value-of select="GradeReference.SchoolYear"/>
							</SchoolYear>
						</GradeIdentity>
					</GradeReference>
					<StudentCompetencyReference>
						<StudentCompetencyIdentity>
							<LearningObjectiveReference>
								<LearningObjectiveIdentity>
									<Objective>
										<xsl:value-of select="StudentCompetencyReference.Objective"/>
									</Objective>
									<AcademicSubject>
										<xsl:value-of select="StudentCompetencyReference.AcademicSubject"/>
									</AcademicSubject>
									<ObjectiveGradeLevel>
										<xsl:value-of select="StudentCompetencyReference.ObjectiveGradeLevel"/>
									</ObjectiveGradeLevel>
								</LearningObjectiveIdentity>
							</LearningObjectiveReference>
							<CodeValue>
								<xsl:value-of select="StudentCompetencyReference.CodeValue"/>
							</CodeValue>
							<StudentSectionAssociationReference>
								<StudentSectionAssociationIdentity>
									<StudentReference>
										<StudentIdentity>
											<StudentUniqueStateId>
												<xsl:value-of select="StudentCompetencyReference.StudentUniqueStateId"/>
											</StudentUniqueStateId>
										</StudentIdentity>
									</StudentReference>
									<SectionReference>
										<SectionIdentity>
											<EducationalOrgReference>
												<EducationalOrgIdentity>
													<StateOrganizationId>
														<xsl:value-of select="StudentCompetencyReference.StateOrganizationId"/>
													</StateOrganizationId>
												</EducationalOrgIdentity>
											</EducationalOrgReference>
											<UniqueSectionCode>
												<xsl:value-of select="StudentCompetencyReference.UniqueSectionCode"/>
											</UniqueSectionCode>
										</SectionIdentity>
									</SectionReference>
									<BeginDate>
										<xsl:value-of select="StudentCompetencyReference.BeginDate"/>
									</BeginDate>
								</StudentSectionAssociationIdentity>
							</StudentSectionAssociationReference>
						</StudentCompetencyIdentity>
					</StudentCompetencyReference>
					<GPAGivenGradingPeriod>
						<xsl:value-of select="GPAGivenGradingPeriod"/>
					</GPAGivenGradingPeriod>
					<GPACumulative>
						<xsl:value-of select="GPACumulative"/>
					</GPACumulative>
					<StudentReference>
						<StudentIdentity>
							<StudentUniqueStateId>
								<xsl:value-of select="StudentReference.StudentUniqueStateId"/>
							</StudentUniqueStateId>
						</StudentIdentity>
					</StudentReference>
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
				</ReportCard>
			</xsl:for-each>
		</InterchangeStudentGrade>
	</xsl:template>
</xsl:stylesheet>