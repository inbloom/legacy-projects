<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStudentGrade xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">                        
				<StudentGradebookEntry>
					<DateFulfilled>
						<xsl:value-of select="DateFulfilled"/>
					</DateFulfilled>
					<NumericGradeEarned>
						<xsl:value-of select="NumericGradeEarned"/>
					</NumericGradeEarned>
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
					<GradebookEntryReference>
						<GradebookEntryIdentity>
							<GradebookEntryType>
								<xsl:value-of select="GradebookEntryReference.GradebookEntryType"/>
							</GradebookEntryType>
							<DateAssigned>
								<xsl:value-of select="GradebookEntryReference.DateAssigned"/>
							</DateAssigned>
							<SectionReference>
								<SectionIdentity>
									<EducationalOrgReference>
										<EducationalOrgIdentity>
											<StateOrganizationId>
												<xsl:value-of select="GradebookEntryReference.StateOrganizationId"/>
											</StateOrganizationId>
										</EducationalOrgIdentity>
									</EducationalOrgReference>
									<UniqueSectionCode>
										<xsl:value-of select="GradebookEntryReference.UniqueSectionCode"/>
									</UniqueSectionCode>
								</SectionIdentity>
							</SectionReference>
						</GradebookEntryIdentity>
					</GradebookEntryReference>
				</StudentGradebookEntry>
			</xsl:for-each> 
		</InterchangeStudentGrade>
	</xsl:template>
</xsl:stylesheet>