<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeEducationOrganization xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">         
				<Course>
					<CourseTitle>
						<xsl:value-of select="CourseTitle"/>
					</CourseTitle>
					<NumberOfParts>
						<xsl:value-of select="NumberOfParts"/>
					</NumberOfParts>
					<CourseCode IdentificationSystem="{CourseCode.IdentificationSystem}"> 
						<ID>
							<xsl:value-of select="CourseCode.ID"/>
						</ID>
					</CourseCode>
					<GradesOffered>
						<GradeLevel>
							<xsl:value-of select="GradesOffered.GradeLevel"/>
						</GradeLevel>
					</GradesOffered>
					<SubjectArea>
						<xsl:value-of select="SubjectArea"/>
					</SubjectArea>
					<DateCourseAdopted>
						<xsl:value-of select="DateCourseAdopted"/>
					</DateCourseAdopted>
					<HighSchoolCourseRequirement>
						<xsl:value-of select="HighSchoolCourseRequirement"/>
					</HighSchoolCourseRequirement>
					<MinimumAvailableCredit>
						<Credit>
							<xsl:value-of select="MinimumAvailableCredit.Credit"/>
						</Credit>
					</MinimumAvailableCredit>
					<MaximumAvailableCredit>
						<Credit>
							<xsl:value-of select="MaximumAvailableCredit.Credit"/>
						</Credit>
					</MaximumAvailableCredit>
					<EducationOrganizationReference>
						<EducationalOrgIdentity>
							<StateOrganizationId>
								<xsl:value-of select="EducationOrganizationReference.StateOrganizationId"/>
							</StateOrganizationId>
						</EducationalOrgIdentity>
					</EducationOrganizationReference>
					<UniqueCourseId>
						<xsl:value-of select="UniqueCourseId"/>
					</UniqueCourseId>
				</Course>
			</xsl:for-each>
		</InterchangeEducationOrganization>
	</xsl:template>
</xsl:stylesheet>
