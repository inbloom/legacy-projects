<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStudentDiscipline xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<StudentDisciplineIncidentAssociation>
					<StudentReference>
						<StudentIdentity>
							<StudentUniqueStateId>
								<xsl:value-of select="StudentReference.StudentUniqueStateId"/>
							</StudentUniqueStateId>
						</StudentIdentity>
					</StudentReference>
					<DisciplineIncidentReference>
						<DisciplineIncidentIdentity>
							<IncidentIdentifier>
								<xsl:value-of select="DisciplineIncidentReference.IncidentIdentifier"/>
							</IncidentIdentifier>
							<EducationalOrgReference>
								<EducationalOrgIdentity>
									<StateOrganizationId>
										<xsl:value-of select="DisciplineIncidentReference.StateOrganizationId"/>
									</StateOrganizationId>
								</EducationalOrgIdentity>
							</EducationalOrgReference>
						</DisciplineIncidentIdentity>
					</DisciplineIncidentReference>
					<StudentParticipationCode>
						<xsl:value-of select="StudentParticipationCode"/>
					</StudentParticipationCode>
					<Behaviors>
						<CodeValue>
							<xsl:value-of select="Behaviors.CodeValue"/>
						</CodeValue>
					</Behaviors>
				</StudentDisciplineIncidentAssociation>
			</xsl:for-each>
		</InterchangeStudentDiscipline>
	</xsl:template>
</xsl:stylesheet>