<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStudentDiscipline xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<DisciplineAction>
					<DisciplineActionIdentifier>
						<xsl:value-of select="DisciplineActionIdentifier"/>
					</DisciplineActionIdentifier>
					<Disciplines>
						<Description>
							<xsl:value-of select="Disciplines.Description"/>
						</Description>
					</Disciplines>
					<DisciplineDate>
						<xsl:value-of select="DisciplineDate"/>
					</DisciplineDate>
					<DisciplineActionLength>
						<xsl:value-of select="DisciplineActionLength"/>
					</DisciplineActionLength>
					<ActualDisciplineActionLength>
						<xsl:value-of select="ActualDisciplineActionLength"/>
					</ActualDisciplineActionLength>
					<DisciplineActionLengthDifferenceReason>
						<xsl:value-of select="DisciplineActionLengthDifferenceReason"/>
					</DisciplineActionLengthDifferenceReason>
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
					<StaffReference>
						<StaffIdentity>
							<StaffUniqueStateId>
								<xsl:value-of select="StaffReference.StaffUniqueStateId"/>
							</StaffUniqueStateId>
						</StaffIdentity>
					</StaffReference>
					<ResponsibilitySchoolReference>
						<EducationalOrgIdentity>
							<StateOrganizationId>
								<xsl:value-of select="ResponsibilitySchoolReference.StateOrganizationId"/>
							</StateOrganizationId>
						</EducationalOrgIdentity>
					</ResponsibilitySchoolReference>
					<AssignmentSchoolReference>
						<EducationalOrgIdentity>
							<StateOrganizationId>
								<xsl:value-of select="AssignmentSchoolReference.StateOrganizationId"/>
							</StateOrganizationId>
						</EducationalOrgIdentity>
					</AssignmentSchoolReference>
				</DisciplineAction>
			</xsl:for-each>
		</InterchangeStudentDiscipline>
	</xsl:template>
</xsl:stylesheet>