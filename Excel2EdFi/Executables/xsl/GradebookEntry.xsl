<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStudentGrade xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">                        
				<GradebookEntry>
					<GradebookEntryType>
						<xsl:value-of select="GradebookEntryType"/>
					</GradebookEntryType>
					<DateAssigned>
						<xsl:value-of select="DateAssigned"/>
					</DateAssigned>
					<Description>
						<xsl:value-of select="Description"/>
					</Description>
					<LearningStandardReference>
						<LearningStandardIdentity>
							<IdentificationCode>
								<xsl:value-of select="IdentificationCode"/>
							</IdentificationCode>
						</LearningStandardIdentity>
					</LearningStandardReference>
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
				</GradebookEntry>
			</xsl:for-each> 
		</InterchangeStudentGrade>
	</xsl:template>
</xsl:stylesheet>