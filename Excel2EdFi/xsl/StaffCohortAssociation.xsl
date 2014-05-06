<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStudentCohort xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">        
				<StaffCohortAssociation>
					<StaffReference>
						<StaffIdentity>
							<StaffUniqueStateId>
								<xsl:value-of select="StaffReference.StaffUniqueStateId"/>
							</StaffUniqueStateId>
						</StaffIdentity>
					</StaffReference>
					<CohortReference>
						<CohortIdentity>
							<CohortIdentifier>
								<xsl:value-of select="CohortReference.CohortIdentifier"/>
							</CohortIdentifier>
							<EducationalOrgReference>
								<EducationalOrgIdentity>
									<StateOrganizationId>
										<xsl:value-of select="CohortReference.StateOrganizationId"/>
									</StateOrganizationId>
								</EducationalOrgIdentity>
							</EducationalOrgReference>
						</CohortIdentity>
					</CohortReference>
					<BeginDate>
						<xsl:value-of select="BeginDate"/>
					</BeginDate>
					<EndDate>
						<xsl:value-of select="EndDate"/>
					</EndDate>
					<StudentRecordAccess>
						<xsl:value-of select="StudentRecordAccess"/>
					</StudentRecordAccess>
				</StaffCohortAssociation>
			</xsl:for-each>
		</InterchangeStudentCohort>
	</xsl:template>
</xsl:stylesheet>