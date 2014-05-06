<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStudentDiscipline xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<DisciplineIncident>
					<IncidentIdentifier>
						<xsl:value-of select="IncidentIdentifier"/>
					</IncidentIdentifier>
					<IncidentDate>
						<xsl:value-of select="IncidentDate"/>
					</IncidentDate>
					<IncidentTime>
						<xsl:value-of select="IncidentTime"/>
					</IncidentTime>
					<IncidentLocation>
						<xsl:value-of select="IncidentLocation"/>
					</IncidentLocation>
					<ReporterDescription>
						<xsl:value-of select="ReporterDescription"/>
					</ReporterDescription>
					<ReporterName>
						<xsl:value-of select="ReporterName"/>
					</ReporterName>
					<Behaviors>
						<CodeValue>
							<xsl:value-of select="Behaviors.CodeValue"/>
						</CodeValue>
					</Behaviors>
					<Weapons>
						<Weapon>
							<xsl:value-of select="Weapons.Weapon"/>
						</Weapon>
					</Weapons>
					<ReportedToLawEnforcement>
						<xsl:value-of select="ReportedToLawEnforcement"/>
					</ReportedToLawEnforcement>
					<SchoolReference>
						<EducationalOrgIdentity>
							<StateOrganizationId>
								<xsl:value-of select="StateOrganizationId"/>
							</StateOrganizationId>
						</EducationalOrgIdentity>
					</SchoolReference>
					<StaffReference>
						<StaffIdentity>
							<StaffUniqueStateId>
								<xsl:value-of select="StaffUniqueStateId"/>
							</StaffUniqueStateId>
						</StaffIdentity>
					</StaffReference>
				</DisciplineIncident>
			</xsl:for-each>
		</InterchangeStudentDiscipline>
	</xsl:template>
</xsl:stylesheet>