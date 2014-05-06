<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStudentParent xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<StudentParentAssociation>
					<StudentReference>
						<StudentIdentity>
							<StudentUniqueStateId>
								<xsl:value-of select="StudentUniqueStateId"/>
							</StudentUniqueStateId>
						</StudentIdentity>
					</StudentReference>
					<ParentReference>
						<ParentIdentity>
							<ParentUniqueStateId>
								<xsl:value-of select="ParentUniqueStateId"/>
							</ParentUniqueStateId>
						</ParentIdentity>
					</ParentReference>
					<Relation>
						<xsl:value-of select="Relation"/>
					</Relation>
					<PrimaryContactStatus>
						<xsl:value-of select="PrimaryContactStatus"/>
					</PrimaryContactStatus>
					<LivesWith>
						<xsl:value-of select="LivesWith"/>
					</LivesWith>
					<EmergencyContactStatus>
						<xsl:value-of select="EmergencyContactStatus"/>
					</EmergencyContactStatus>
					<ContactPriority>
						<xsl:value-of select="ContactPriority"/>
					</ContactPriority>
					<ContactRestrictions>
						<xsl:value-of select="ContactRestrictions"/>
					</ContactRestrictions>
				</StudentParentAssociation>
			</xsl:for-each>
		</InterchangeStudentParent>
	</xsl:template>
</xsl:stylesheet>