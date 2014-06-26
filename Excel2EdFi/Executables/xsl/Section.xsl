<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeMasterSchedule xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">                        
				<Section>
					<UniqueSectionCode>
						<xsl:value-of select="UniqueSectionCode"/>
					</UniqueSectionCode>
					<SequenceOfCourse>
						<xsl:value-of select="SequenceOfCourse"/>
					</SequenceOfCourse>
					<EducationalEnvironment>
						<xsl:value-of select="EducationalEnvironment"/>
					</EducationalEnvironment>
					<MediumOfInstruction>
						<xsl:value-of select="MediumOfInstruction"/>
					</MediumOfInstruction>
					<PopulationServed>
						<xsl:value-of select="PopulationServed"/>
					</PopulationServed>
					<CourseOfferingReference>
						<CourseOfferingIdentity>
							<LocalCourseCode>
								<xsl:value-of select="CourseOfferingReference.LocalCourseCode"/>
							</LocalCourseCode>
							<SessionReference>
								<SessionIdentity>
									<EducationalOrgReference>
										<EducationalOrgIdentity>
											<StateOrganizationId>
												<xsl:value-of select="CourseOfferingReference.StateOrganizationId"/>
											</StateOrganizationId>
										</EducationalOrgIdentity>
									</EducationalOrgReference>
									<SessionName>
										<xsl:value-of select="CourseOfferingReference.SessionName"/>
									</SessionName>
								</SessionIdentity>
							</SessionReference>
							<EducationalOrgReference>
								<EducationalOrgIdentity>
									<StateOrganizationId>
										<xsl:value-of select="CourseOfferingReference.StateOrganizationId"/>
									</StateOrganizationId>
								</EducationalOrgIdentity>
							</EducationalOrgReference>
						</CourseOfferingIdentity>
					</CourseOfferingReference>
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
				</Section>
			</xsl:for-each>
		</InterchangeMasterSchedule>
	</xsl:template>
</xsl:stylesheet>
