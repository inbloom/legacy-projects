<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStaffAssociation xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">   
				<TeacherSectionAssociation>
					<TeacherReference>
						<StaffIdentity>
							<StaffUniqueStateId>
								<xsl:value-of select="TeacherReference.StaffUniqueStateId"/>
							</StaffUniqueStateId>
						</StaffIdentity>
					</TeacherReference>
					<SectionReference>
						<SectionIdentity>
							<EducationalOrgReference>
								<EducationalOrgIdentity>
									<StateOrganizationId>
										<xsl:value-of select="SectionReference.StateOrganizationId"/>
									</StateOrganizationId>
								</EducationalOrgIdentity>
							</EducationalOrgReference>
							<UniqueSectionCode>
								<xsl:value-of select="SectionReference.UniqueSectionCode"/>
							</UniqueSectionCode>
						</SectionIdentity>
					</SectionReference>
					<ClassroomPosition>
						<xsl:value-of select="ClassroomPosition"/>
					</ClassroomPosition>
					<BeginDate>
						<xsl:value-of select="BeginDate"/>
					</BeginDate>
					<EndDate>
						<xsl:value-of select="EndDate"/>
					</EndDate>
					<HighlyQualifiedTeacher>
						<xsl:value-of select="HighlyQualifiedTeacher"/>
					</HighlyQualifiedTeacher>
				</TeacherSectionAssociation>
			</xsl:for-each>
		</InterchangeStaffAssociation>
	</xsl:template>
</xsl:stylesheet>
