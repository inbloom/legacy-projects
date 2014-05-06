<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStudentGrade xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">                        
				<StudentAcademicRecord>

					<xsl:choose>
						<xsl:when test="CumulativeCreditsAttempted.CreditConversion != '' and CumulativeCreditsAttempted.CreditType != '' ">
							<CumulativeCreditsAttempted CreditConversion="{CumulativeCreditsAttempted.CreditConversion}" CreditType="{CumulativeCreditsAttempted.CreditType}">
								<Credit>
									<xsl:value-of select="CumulativeCreditsAttempted.Credit"/>
								</Credit>
							</CumulativeCreditsAttempted>
						</xsl:when>
						<xsl:when test="not(CumulativeCreditsAttempted.CreditConversion) and CumulativeCreditsAttempted.CreditType != '' ">
							<CumulativeCreditsAttempted CreditType="{CumulativeCreditsAttempted.CreditType}">
								<Credit>
									<xsl:value-of select="CumulativeCreditsAttempted.Credit"/>
								</Credit>
							</CumulativeCreditsAttempted>
						</xsl:when>
						<xsl:when test="CumulativeCreditsAttempted.CreditConversion != '' and not(CumulativeCreditsAttempted.CreditType)">
							<CumulativeCreditsAttempted CreditConversion="{CumulativeCreditsAttempted.CreditConversion}">
								<Credit>
									<xsl:value-of select="CumulativeCreditsAttempted.Credit"/>
								</Credit>
							</CumulativeCreditsAttempted>
						</xsl:when>
						<xsl:otherwise>
							<CumulativeCreditsAttempted>
								<Credit>
									<xsl:value-of select="CumulativeCreditsAttempted.Credit"/>
								</Credit>
							</CumulativeCreditsAttempted>
						</xsl:otherwise>
					</xsl:choose>

					<CumulativeGradePointAverage>
						<xsl:value-of select="CumulativeGradePointAverage"/>
					</CumulativeGradePointAverage>
					<StudentReference>
						<StudentIdentity>
							<StudentUniqueStateId>
								<xsl:value-of select="StudentReference.StudentUniqueStateId"/>
							</StudentUniqueStateId>
						</StudentIdentity>
					</StudentReference>
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
					<SchoolYear>
						<xsl:value-of select="SchoolYear"/>
					</SchoolYear>
				</StudentAcademicRecord>
			</xsl:for-each> 
		</InterchangeStudentGrade>
	</xsl:template>
</xsl:stylesheet>