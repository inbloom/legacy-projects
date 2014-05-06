<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStudentProgram xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<StudentProgramAssociation>
					<StudentReference>
						<StudentIdentity>
							<StudentUniqueStateId>
								<xsl:value-of select="StudentReference.StudentUniqueStateId"/>
							</StudentUniqueStateId>
						</StudentIdentity>
					</StudentReference>
					<ProgramReference>
						<ProgramIdentity>
							<ProgramId>
								<xsl:value-of select="ProgramReference.ProgramId"/>
							</ProgramId>
						</ProgramIdentity>
					</ProgramReference>
					<BeginDate>
						<xsl:value-of select="BeginDate"/>
					</BeginDate>
					<EducationOrganizationReference>
						<EducationalOrgIdentity>
							<StateOrganizationId>
								<xsl:value-of select="EducationOrganizationReference.StateOrganizationId"/>
							</StateOrganizationId>
						</EducationalOrgIdentity>
					</EducationOrganizationReference>
				</StudentProgramAssociation>
			</xsl:for-each>
		</InterchangeStudentProgram>
	</xsl:template>
</xsl:stylesheet>