<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStudentEnrollment xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">                        
				<StudentSchoolAssociation>
					<StudentReference>
						<StudentIdentity>
							<StudentUniqueStateId>
								<xsl:value-of select="StudentReference.StudentUniqueStateId"/>
							</StudentUniqueStateId>
						</StudentIdentity>
					</StudentReference>
					<SchoolReference>
						<EducationalOrgIdentity>
							<StateOrganizationId>
								<xsl:value-of select="SchoolReference.StateOrganizationId"/>
							</StateOrganizationId>
						</EducationalOrgIdentity>
					</SchoolReference>
					<EntryDate>
						<xsl:value-of select="EntryDate"/>
					</EntryDate>
					<EntryGradeLevel>
						<xsl:value-of select="EntryGradeLevel"/>
					</EntryGradeLevel>
					<ExitWithdrawDate>
						<xsl:value-of select="ExitWithdrawDate"/>
					</ExitWithdrawDate>
					<ExitWithdrawType>
						<xsl:value-of select="ExitWithdrawType"/>
					</ExitWithdrawType>
				</StudentSchoolAssociation>
			</xsl:for-each>
		</InterchangeStudentEnrollment>
	</xsl:template>
</xsl:stylesheet>
