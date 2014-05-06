<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeMasterSchedule xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">  
				<CourseOffering>
					<LocalCourseCode>
						<xsl:value-of select="LocalCourseCode"/>
					</LocalCourseCode>
					<LocalCourseTitle>
						<xsl:value-of select="LocalCourseTitle"/>
					</LocalCourseTitle>
					<SchoolReference>
						<EducationalOrgIdentity>
							<StateOrganizationId>
								<xsl:value-of select="SchoolReference.StateOrganizationId"/>
							</StateOrganizationId>
						</EducationalOrgIdentity>
					</SchoolReference>
					<SessionReference>
						<SessionIdentity>
							<EducationalOrgReference>
								<EducationalOrgIdentity>
									<StateOrganizationId>
										<xsl:value-of select="SessionReference.StateOrganizationId"/>
									</StateOrganizationId>
								</EducationalOrgIdentity>
							</EducationalOrgReference>
							<SessionName>
								<xsl:value-of select="SessionReference.SessionName"/>
							</SessionName>
						</SessionIdentity>
					</SessionReference>
					<CourseReference>
						<CourseIdentity>
							<EducationalOrgReference>
								<EducationalOrgIdentity>
									<StateOrganizationId>
										<xsl:value-of select="CourseReference.StateOrganizationId"/>
									</StateOrganizationId>
								</EducationalOrgIdentity>
							</EducationalOrgReference>
							<UniqueCourseId>
								<xsl:value-of select="CourseReference.UniqueCourseId"/>
							</UniqueCourseId>
						</CourseIdentity>
					</CourseReference>
				</CourseOffering>
			</xsl:for-each>
		</InterchangeMasterSchedule>
	</xsl:template>
</xsl:stylesheet>