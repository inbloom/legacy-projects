<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" indent="yes" />
	<xsl:template match="rows">
		<InterchangeStaffAssociation xmlns="http://ed-fi.org/0100">
			<xsl:for-each select="row">
				<Staff>
					<StaffUniqueStateId>
						<xsl:value-of select="StaffUniqueStateId"/>
					</StaffUniqueStateId>
					<xsl:choose>
						<xsl:when test="StaffIdentificationCode.AssigningOrganizationCode">
							<StaffIdentificationCode AssigningOrganizationCode='{StaffIdentificationCode.AssigningOrganizationCode}' IdentificationSystem='{StaffIdentificationCode.IdentificationSystem}'>
								<ID>
									<xsl:value-of select="StaffIdentificationCode.ID"/>
								</ID>
							</StaffIdentificationCode>
						</xsl:when>
						<xsl:otherwise>
							<StaffIdentificationCode IdentificationSystem='{StaffIdentificationCode.IdentificationSystem}'>
								<ID>
									<xsl:value-of select="StaffIdentificationCode.ID"/>
								</ID>
							</StaffIdentificationCode>
						</xsl:otherwise>
					</xsl:choose>
					
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
					<BirthDate>
						<xsl:value-of select="BirthDate"/>
					</BirthDate>

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

					<xsl:choose>
						<xsl:when test="Telephone.PrimaryTelephoneNumberIndicator != '' and Telephone.TelephoneNumberType != '' ">
							<Telephone PrimaryTelephoneNumberIndicator='{Telephone.PrimaryTelephoneNumberIndicator}' TelephoneNumberType='{Telephone.TelephoneNumberType}'>
								<TelephoneNumber>
									<xsl:value-of select="Telephone.TelephoneNumber"/>
								</TelephoneNumber>
							</Telephone>
						</xsl:when>
						<xsl:when test="not(Telephone.PrimaryTelephoneNumberIndicator) and Telephone.TelephoneNumberType != '' ">
							<Telephone TelephoneNumberType='{Telephone.TelephoneNumberType}'>
								<TelephoneNumber>
									<xsl:value-of select="Telephone.TelephoneNumber"/>
								</TelephoneNumber>
							</Telephone>
						</xsl:when>
						<xsl:when test="Telephone.PrimaryTelephoneNumberIndicator != '' and not(Telephone.TelephoneNumberType)">
							<Telephone PrimaryTelephoneNumberIndicator='{Telephone.PrimaryTelephoneNumberIndicator}' >
								<TelephoneNumber>
									<xsl:value-of select="Telephone.TelephoneNumber"/>
								</TelephoneNumber>
							</Telephone>
						</xsl:when>
						<xsl:otherwise>
							<Telephone>
								<TelephoneNumber>
									<xsl:value-of select="Telephone.TelephoneNumber"/>
								</TelephoneNumber>
							</Telephone>
						</xsl:otherwise>
					</xsl:choose>

					<xsl:choose>
						<xsl:when test="ElectronicMail.EmailAddressType">
							<ElectronicMail EmailAddressType="{ElectronicMail.EmailAddressType}">
								<EmailAddress>
									<xsl:value-of select="ElectronicMail.EmailAddress"/>
								</EmailAddress>
							</ElectronicMail>
						</xsl:when>
						<xsl:otherwise>
							<ElectronicMail>
								<EmailAddress>
									<xsl:value-of select="ElectronicMail.EmailAddress"/>
								</EmailAddress>
							</ElectronicMail>
						</xsl:otherwise>
					</xsl:choose>

					<HispanicLatinoEthnicity>
						<xsl:value-of select="HispanicLatinoEthnicity"/>
					</HispanicLatinoEthnicity>
					<OldEthnicity>
						<xsl:value-of select="OldEthnicity"/>
					</OldEthnicity>
					<Race>
						<RacialCategory>
							<xsl:value-of select="Race.RacialCategory"/>
						</RacialCategory>
					</Race>
					<HighestLevelOfEducationCompleted>
						<xsl:value-of select="HighestLevelOfEducationCompleted"/>
					</HighestLevelOfEducationCompleted>
					<YearsOfPriorProfessionalExperience>
						<xsl:value-of select="YearsOfPriorProfessionalExperience"/>
					</YearsOfPriorProfessionalExperience>
					<YearsOfPriorTeachingExperience>
						<xsl:value-of select="YearsOfPriorTeachingExperience"/>
					</YearsOfPriorTeachingExperience>
					<Credentials>
						<CredentialType>
							<xsl:value-of select="Credentials.CredentialType"/>
						</CredentialType>
						<CredentialField>
							<CodeValue>
								<xsl:value-of select="Credentials.CodeValue"/>
							</CodeValue>
						</CredentialField>
						<Level>
							<xsl:value-of select="Credentials.Level"/>
						</Level>
						<TeachingCredentialType>
							<xsl:value-of select="Credentials.TeachingCredentialType"/>
						</TeachingCredentialType>
						<CredentialIssuanceDate>
							<xsl:value-of select="Credentials.CredentialIssuanceDate"/>
						</CredentialIssuanceDate>
					</Credentials>
					<LoginId>
						<xsl:value-of select="LoginId"/>
					</LoginId>
				</Staff>
			</xsl:for-each>
		</InterchangeStaffAssociation>
	</xsl:template>
</xsl:stylesheet>
