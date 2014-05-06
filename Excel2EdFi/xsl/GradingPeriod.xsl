<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeEducationOrgCalendar xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<GradingPeriod>
					<GradingPeriod>
						<xsl:value-of select="GradingPeriod"/>
					</GradingPeriod>
					<SchoolYear>
						<xsl:value-of select="SchoolYear"/>
					</SchoolYear>
					<EducationOrganizationReference>
						<EducationalOrgIdentity>
							<StateOrganizationId>
								<xsl:value-of select="EducationOrganizationReference.StateOrganizationId"/>
							</StateOrganizationId>
						</EducationalOrgIdentity>
					</EducationOrganizationReference>
					<BeginDate>
						<xsl:value-of select="BeginDate"/>
					</BeginDate>
					<EndDate>
						<xsl:value-of select="EndDate"/>
					</EndDate>
					<TotalInstructionalDays>
						<xsl:value-of select="TotalInstructionalDays"/>
					</TotalInstructionalDays>
					<CalendarDateReference>
						<CalendarDateIdentity>
							<Date>
								<xsl:value-of select="CalendarDateReference.Date"/>
							</Date>
							<EducationOrgReference>
								<EducationalOrgIdentity>
									<StateOrganizationId>
										<xsl:value-of select="CalendarDateReference.StateOrganizationId"/>
									</StateOrganizationId>
								</EducationalOrgIdentity>
							</EducationOrgReference>
						</CalendarDateIdentity>
					</CalendarDateReference>
				</GradingPeriod>
			</xsl:for-each>
		</InterchangeEducationOrgCalendar>
	</xsl:template>
</xsl:stylesheet>