<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStaffAssociation xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<StaffEducationOrgAssignmentAssociation>
					<StaffReference>
						<StaffIdentity>
							<StaffUniqueStateId>
								<xsl:value-of select="StaffReference.StaffUniqueStateId"/>
							</StaffUniqueStateId>
						</StaffIdentity>
					</StaffReference>
					<EducationOrganizationReference>
						<EducationalOrgIdentity>
							<StateOrganizationId>
								<xsl:value-of select="EducationOrganizationReference.StateOrganizationId"/>
							</StateOrganizationId>
						</EducationalOrgIdentity>
					</EducationOrganizationReference>
					<StaffClassification>
						<xsl:value-of select="StaffClassification"/>
					</StaffClassification>
					<BeginDate>
						<xsl:value-of select="BeginDate"/>
					</BeginDate>
					<EndDate>
						<xsl:value-of select="EndDate"/>
					</EndDate>
				</StaffEducationOrgAssignmentAssociation>
			</xsl:for-each>
		</InterchangeStaffAssociation>
	</xsl:template>
</xsl:stylesheet>