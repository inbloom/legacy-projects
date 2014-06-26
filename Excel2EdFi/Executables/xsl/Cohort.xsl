<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStudentCohort xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">        
				<Cohort>
					<CohortIdentifier>
						<xsl:value-of select="CohortIdentifier"/>
					</CohortIdentifier>
					<CohortDescription>
						<xsl:value-of select="CohortDescription"/>
					</CohortDescription>
					<CohortType>
						<xsl:value-of select="CohortType"/>
					</CohortType>
					<CohortScope>
						<xsl:value-of select="CohortScope"/>
					</CohortScope>
					<AcademicSubject>
						<xsl:value-of select="AcademicSubject"/>
					</AcademicSubject>
					<EducationOrgReference>
						<EducationalOrgIdentity>
							<StateOrganizationId>
								<xsl:value-of select="EducationOrgReference.StateOrganizationId"/>
							</StateOrganizationId>
						</EducationalOrgIdentity>
					</EducationOrgReference>
					<ProgramReference>
						<ProgramIdentity>
							<ProgramId>
								<xsl:value-of select="ProgramReference.ProgramId"/>
							</ProgramId>
						</ProgramIdentity>
					</ProgramReference>
				</Cohort>
			</xsl:for-each>
		</InterchangeStudentCohort>
	</xsl:template>
</xsl:stylesheet>