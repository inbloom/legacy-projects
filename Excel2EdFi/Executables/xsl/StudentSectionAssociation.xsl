<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStudentEnrollment xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">                        
				<StudentSectionAssociation>
					<StudentReference>
						<StudentIdentity>
							<StudentUniqueStateId>
								<xsl:value-of select="StudentReference.StudentUniqueStateId"/>
							</StudentUniqueStateId>
						</StudentIdentity>
					</StudentReference>
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
					<BeginDate>
						<xsl:value-of select="BeginDate"/>
					</BeginDate>
					<EndDate>
						<xsl:value-of select="EndDate"/>
					</EndDate>
				</StudentSectionAssociation>
			</xsl:for-each>
		</InterchangeStudentEnrollment>
	</xsl:template>
</xsl:stylesheet>