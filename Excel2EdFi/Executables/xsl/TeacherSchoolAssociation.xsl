<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStaffAssociation xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<TeacherSchoolAssociation>
					<TeacherReference>
						<StaffIdentity>
							<StaffUniqueStateId>
								<xsl:value-of select="TeacherReference.StaffUniqueStateId"/>
							</StaffUniqueStateId>
						</StaffIdentity>
					</TeacherReference>
					<SchoolReference>
						<EducationalOrgIdentity>
							<StateOrganizationId>
								<xsl:value-of select="SchoolReference.StateOrganizationId"/>
							</StateOrganizationId>
						</EducationalOrgIdentity>
					</SchoolReference>
					<ProgramAssignment>
						<xsl:value-of select="ProgramAssignment"/>
					</ProgramAssignment>
					<InstructionalGradeLevels>
						<GradeLevel>
							<xsl:value-of select="InstructionalGradeLevels.GradeLevel"/>
						</GradeLevel>
					</InstructionalGradeLevels>
					<AcademicSubjects>
						<AcademicSubject>
							<xsl:value-of select="AcademicSubjects.AcademicSubject"/>
						</AcademicSubject>						
					</AcademicSubjects>
				</TeacherSchoolAssociation>
			</xsl:for-each>
		</InterchangeStaffAssociation>
	</xsl:template>
</xsl:stylesheet>