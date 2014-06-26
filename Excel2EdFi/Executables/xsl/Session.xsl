<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeEducationOrgCalendar xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">    
				<Session>
					<SessionName>
						<xsl:value-of select="SessionName"/>
					</SessionName>
					<SchoolYear>
						<xsl:value-of select="SchoolYear"/>
					</SchoolYear>
					<Term>
						<xsl:value-of select="Term"/>
					</Term>
					<BeginDate>
						<xsl:value-of select="BeginDate"/>
					</BeginDate>
					<EndDate>
						<xsl:value-of select="EndDate"/>
					</EndDate>
					<TotalInstructionalDays>
						<xsl:value-of select="TotalInstructionalDays"/>
					</TotalInstructionalDays>
					<EducationOrganizationReference>
						<EducationalOrgIdentity>
							<StateOrganizationId>
								<xsl:value-of select="EducationOrganizationReference.StateOrganizationId"/>
							</StateOrganizationId>
						</EducationalOrgIdentity>
					</EducationOrganizationReference>
					<GradingPeriodReference>
						<GradingPeriodIdentity>
							<EducationalOrgReference>
								<EducationalOrgIdentity>
									<StateOrganizationId>
										<xsl:value-of select="GradingPeriodReference.StateOrganizationId"/>
									</StateOrganizationId>
								</EducationalOrgIdentity>
							</EducationalOrgReference>
							<GradingPeriod>
								<xsl:value-of select="GradingPeriodReference.GradingPeriod"/>
							</GradingPeriod>
							<BeginDate>
								<xsl:value-of select="GradingPeriodReference.BeginDate"/>
							</BeginDate>
						</GradingPeriodIdentity>
					</GradingPeriodReference>
				</Session>
			</xsl:for-each>
		</InterchangeEducationOrgCalendar>
	</xsl:template>
</xsl:stylesheet>