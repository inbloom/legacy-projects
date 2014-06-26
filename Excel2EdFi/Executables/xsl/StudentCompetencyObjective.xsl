<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStudentGrade xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<StudentCompetencyObjective>
					<StudentCompetencyObjectiveId>
						<xsl:value-of select="StudentCompetencyObjectiveId"/>
					</StudentCompetencyObjectiveId>
					<Objective>
						<xsl:value-of select="Objective"/>
					</Objective>
					<Description>
						<xsl:value-of select="Description"/>
					</Description>
					<ObjectiveGradeLevel>
						<xsl:value-of select="ObjectiveGradeLevel"/>
					</ObjectiveGradeLevel>
					<EducationOrganizationReference>
						<EducationalOrgIdentity>
							<StateOrganizationId>
								<xsl:value-of select="StateOrganizationId"/>
							</StateOrganizationId>
						</EducationalOrgIdentity>
					</EducationOrganizationReference>
				</StudentCompetencyObjective>
			</xsl:for-each>
		</InterchangeStudentGrade>
	</xsl:template>
</xsl:stylesheet>