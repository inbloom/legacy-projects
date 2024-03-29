<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStaffAssociation xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<StaffProgramAssociation>
					<StaffReference>
						<StaffIdentity>
							<StaffUniqueStateId>
								<xsl:value-of select="StaffReference.StaffUniqueStateId"/>
							</StaffUniqueStateId>
						</StaffIdentity>
					</StaffReference>
					<ProgramReference>
						<ProgramIdentity>
							<ProgramId>
								<xsl:value-of select="ProgramReference.ProgramId"/>
							</ProgramId>
						</ProgramIdentity>
					</ProgramReference>
					<BeginDate>
						<xsl:value-of select="BeginDate"/>
					</BeginDate>
					<EndDate>
						<xsl:value-of select="EndDate"/>
					</EndDate>
					<StudentRecordAccess>
						<xsl:value-of select="StudentRecordAccess"/>
					</StudentRecordAccess>
				</StaffProgramAssociation>
			</xsl:for-each>
		</InterchangeStaffAssociation>
	</xsl:template>
</xsl:stylesheet>
