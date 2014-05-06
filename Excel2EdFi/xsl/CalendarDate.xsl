<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeEducationOrgCalendar xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<CalendarDate>
					<Date>
						<xsl:value-of select="CalendarDate"/>
					</Date>
					<CalendarEvent>
						<xsl:value-of select="CalendarEventType"/>
					</CalendarEvent>
					<EducationOrgReference>
						<EducationalOrgIdentity>
							<StateOrganizationId>
								<xsl:value-of select="EducationOrgReference.StateOrganizationId"/>
							</StateOrganizationId>
						</EducationalOrgIdentity>
					</EducationOrgReference>
				</CalendarDate>
			</xsl:for-each>
		</InterchangeEducationOrgCalendar>
	</xsl:template>
</xsl:stylesheet>