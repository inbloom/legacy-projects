<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStudentParent xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<Parent>
					<ParentUniqueStateId>
						<xsl:value-of select="ParentUniqueStateId"/>
					</ParentUniqueStateId>
					
					<xsl:choose>
						<xsl:when test="Name.Verification">
							<Name Verification='{Name.Verification}'>
								<PersonalTitlePrefix>
									<xsl:value-of select="Name.PersonalTitlePrefix"/>
								</PersonalTitlePrefix>
								<FirstName>
									<xsl:value-of select="Name.FirstName"/>
								</FirstName>
								<MiddleName>
									<xsl:value-of select="Name.MiddleName"/>
								</MiddleName>
								<LastSurname>
									<xsl:value-of select="Name.LastSurname"/>
								</LastSurname>
								<GenerationCodeSuffix>
									<xsl:value-of select="Name.GenerationCodeSuffix"/>
								</GenerationCodeSuffix>
								<MaidenName>
									<xsl:value-of select="Name.MaidenName"/>
								</MaidenName>
							</Name>
						</xsl:when>
						<xsl:otherwise>
							<Name>
								<PersonalTitlePrefix>
									<xsl:value-of select="Name.PersonalTitlePrefix"/>
								</PersonalTitlePrefix>
								<FirstName>
									<xsl:value-of select="Name.FirstName"/>
								</FirstName>
								<MiddleName>
									<xsl:value-of select="Name.MiddleName"/>
								</MiddleName>
								<LastSurname>
									<xsl:value-of select="Name.LastSurname"/>
								</LastSurname>
								<GenerationCodeSuffix>
									<xsl:value-of select="Name.GenerationCodeSuffix"/>
								</GenerationCodeSuffix>
								<MaidenName>
									<xsl:value-of select="Name.MaidenName"/>
								</MaidenName>
							</Name>
						</xsl:otherwise>
					</xsl:choose>
					
					<Sex>
						<xsl:value-of select="Sex"/>
					</Sex>
					<xsl:choose>
						<xsl:when test="Address.AddressType">
							<Address AddressType="{Address.AddressType}">
								<StreetNumberName>
									<xsl:value-of select="Address.StreetNumberName"/>
								</StreetNumberName>
								<ApartmentRoomSuiteNumber>
									<xsl:value-of select="Address.ApartmentRoomSuiteNumber"/>
								</ApartmentRoomSuiteNumber>
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
								<Latitude>
									<xsl:value-of select="Address.Latitude"/>
								</Latitude>
								<Longitude>
									<xsl:value-of select="Address.Longitude"/>
								</Longitude>
								<BeginDate>
									<xsl:value-of select="Address.BeginDate"/>
								</BeginDate>
								<EndDate>
									<xsl:value-of select="Address.EndDate"/>
								</EndDate>						
							</Address>
						</xsl:when>
						<xsl:otherwise>
							<Address>
								<StreetNumberName>
									<xsl:value-of select="Address.StreetNumberName"/>
								</StreetNumberName>
								<ApartmentRoomSuiteNumber>
									<xsl:value-of select="Address.ApartmentRoomSuiteNumber"/>
								</ApartmentRoomSuiteNumber>
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
								<Latitude>
									<xsl:value-of select="Address.Latitude"/>
								</Latitude>
								<Longitude>
									<xsl:value-of select="Address.Longitude"/>
								</Longitude>
								<BeginDate>
									<xsl:value-of select="Address.BeginDate"/>
								</BeginDate>
								<EndDate>
									<xsl:value-of select="Address.EndDate"/>
								</EndDate>						
							</Address>
						</xsl:otherwise>
					</xsl:choose>
					<Telephone TelephoneNumberType="Home">
						<TelephoneNumber>
							<xsl:value-of select="Telephone.Home"/>
						</TelephoneNumber>
					</Telephone>
					<Telephone TelephoneNumberType="Work">
						<TelephoneNumber>
							<xsl:value-of select="Telephone.Work"/>
						</TelephoneNumber>
					</Telephone>
					<Telephone TelephoneNumberType="Other">
						<TelephoneNumber>
							<xsl:value-of select="Telephone.Other"/>
						</TelephoneNumber>
					</Telephone>
					<ElectronicMail EmailAddressType="Home/Personal">
						<EmailAddress>
							<xsl:value-of select="EmailAddress.Home"/>
						</EmailAddress>
					</ElectronicMail>
					<ElectronicMail EmailAddressType="Work">
						<EmailAddress>
							<xsl:value-of select="EmailAddress.Work"/>
						</EmailAddress>
					</ElectronicMail>
				</Parent>
			</xsl:for-each>
		</InterchangeStudentParent>
	</xsl:template>
</xsl:stylesheet>
