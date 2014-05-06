<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeEducationOrganization xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">         
				<Program>
					<ProgramId>
						<xsl:value-of select="ProgramId"/>
					</ProgramId>
					<ProgramType>
						<xsl:value-of select="ProgramType"/>
					</ProgramType>
					<ProgramSponsor>
						<xsl:value-of select="ProgramSponsor"/>
					</ProgramSponsor>
					<Services>
						<CodeValue>
							<xsl:value-of select="Services.CodeValue"/>
						</CodeValue>
					</Services>
				</Program>
			</xsl:for-each>
		</InterchangeEducationOrganization>
	</xsl:template>
</xsl:stylesheet>
