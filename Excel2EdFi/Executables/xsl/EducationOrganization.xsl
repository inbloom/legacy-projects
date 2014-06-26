<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeEducationOrganization xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<EducationOrganization>
					<StateOrganizationId>
						<xsl:value-of select="StateOrganizationId"/>
					</StateOrganizationId>
					<EducationOrgIdentificationCode IdentificationSystem="{EducationOrgIdentificationCode.IdentificationSystem}">
						<ID>
							<xsl:value-of select="EducationOrgIdentificationCode.ID"/>
						</ID>
					</EducationOrgIdentificationCode>
					<NameOfInstitution>
						<xsl:value-of select="NameOfInstitution"/>
					</NameOfInstitution>
					<OrganizationCategories>
						<OrganizationCategory>
							<xsl:value-of select="OrganizationCategories.OrganizationCategory"/>
						</OrganizationCategory>
					</OrganizationCategories>
					<ParentEducationAgencyReference>
						<EducationalOrgIdentity>
							<StateOrganizationId>
								<xsl:value-of select="ParentEducationAgencyReference.StateOrganizationId"/>
							</StateOrganizationId>
						</EducationalOrgIdentity>
					</ParentEducationAgencyReference>
					<Address>
						<StreetNumberName>
							<xsl:value-of select="Address.StreetNumberName"/>
						</StreetNumberName>
						<City>
							<xsl:value-of select="Address.City"/>
						</City>
						<StateAbbreviation>
							<xsl:value-of select="Address.StateAbbreviation"/>
						</StateAbbreviation>
						<PostalCode>
							<xsl:value-of select="Address.PostalCode"/>
						</PostalCode>
						<NameOfCounty>
							<xsl:value-of select="Address.NameOfCounty"/>
						</NameOfCounty>
					</Address>
					<xsl:choose>
						<xsl:when test="Telephone.InstitutionTelephoneNumberType">
							<Telephone InstitutionTelephoneNumberType="{Telephone.InstitutionTelephoneNumberType}">
								<TelephoneNumber>
									<xsl:value-of select="Telephone.Number"/>
								</TelephoneNumber>
							</Telephone>
						</xsl:when>
						<xsl:otherwise>
							<Telephone>
								<TelephoneNumber>
									<xsl:value-of select="Telephone.Number"/>
								</TelephoneNumber>
							</Telephone>
						</xsl:otherwise>
					</xsl:choose>
					<LEACategory>
						<xsl:value-of select="LEACategory"/>
					</LEACategory>
					<GradesOffered>
						<GradeLevel>
							<xsl:value-of select="GradesOffered.GradeLevel"/>
						</GradeLevel>
					</GradesOffered>
					<SchoolCategories>
						<SchoolCategory>
							<xsl:value-of select="SchoolCategories.SchoolCategory"/>
						</SchoolCategory>
					</SchoolCategories>
				</EducationOrganization>
			</xsl:for-each>
		</InterchangeEducationOrganization>
	</xsl:template>
</xsl:stylesheet>
