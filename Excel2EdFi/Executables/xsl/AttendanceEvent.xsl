<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStudentAttendance xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<AttendanceEvent>
					<SchoolYear>
						<xsl:value-of select="SchoolYear"/>
					</SchoolYear>
					<EventDate>
						<xsl:value-of select="EventDate"/>
					</EventDate>
					<AttendanceEventCategory>
						<xsl:value-of select="AttendanceEventCategory"/>
					</AttendanceEventCategory>
					<EducationalEnvironment>
						<xsl:value-of select="EducationalEnvironment"/>
					</EducationalEnvironment>
					<StudentReference>
						<StudentIdentity>
							<StudentUniqueStateId>
								<xsl:value-of select="StudentReference.StudentUniqueStateId"/>
							</StudentUniqueStateId>
						</StudentIdentity>
					</StudentReference>
					<SchoolReference>
						<EducationalOrgIdentity>
							<StateOrganizationId>
								<xsl:value-of select="SchoolReference.StateOrganizationId"/>
							</StateOrganizationId>
						</EducationalOrgIdentity>
					</SchoolReference>
				</AttendanceEvent>
			</xsl:for-each>
		</InterchangeStudentAttendance>
	</xsl:template>
</xsl:stylesheet>