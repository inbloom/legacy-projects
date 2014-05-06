# Excel to Ed-Fi XML Tool

## SUMMARY
This tool generates Ed-Fi XML sample data from an Excel workbook template.  It is an intended to support development efforts where custom sample data is necessary to fulfill use cases.  It is released under the Apache 2.0 license.

## INSTALLATION
The Excel to Ed-Fi XML tool is a .NET 4.0 application.  It runs natively in Windows and Mac/Linux with the Mono framework (mono-project.com).

Either compile the source code using Visual Studio (Windows) or Xamarin (Mac) or unzip the Excel2EdFiXml.zip in the "bin" directory.

## USAGE
To use, follow the steps below:

1.)  The sample data set will be generated from a specified Excel workbook (a sample is provided as "demodata.xlsx" under the "SampleData" directory).  Each worksheet (or tab) in the Excel workbook will generate a Ed-Fi XML file.  In the "xsl" contains XSL stylesheets which informs how the Excel data is converted into Ed-Fi XML.  The Excel workbook/tab name must correspond with filename of the XSL stylesheet (which will also become the output filename in Ed-Fi XML).

2.)  Ensure the Excel workbook tab name corresponds with an entry in the "entitymapping.txt" file.  This file specifies which entity maps to which Ed-Fi data interchange to generate the neccessary control file for data ingestion.

3.)  Run "Excel2EdFiXML.exe <Excel workbook name>" on Windows or "mono Excel2EdFiXML.exe <Excel workbook name>" on Mac/Linux.

4.)  The output file will be found as "EdFiIngestion.zip" in the "output" directory.  This is ready for upload to the inBloom secure bulk ingestion zone.

## NOTE

ENSURE ALL SAMPLE DATA DOES NOT INCLUDE PERSONALLY IDENTIFABLE INFORMATION (PII).  SAMPLE DATA IN THE SANDBOX IS ONLY INTENDED FOR DEVELOPMENT PURPOSES AND MUST BE FREE OF REAL NAMES, LOCATIONS OR OTHER FORMS OF PII. 


## CONTRIBUTING
Interested in helping to improve the Excel to Ed-Fi XML tool? Great! You can take look at the backlog on our [Jira issue tracker](https://support.inbloom.org "Jira"). Browse existing issues, or contribute your own ideas for improvement and new features.

Looking to interact with other developers interested in changing the future of education? Check out our [community forums](https://forums.inbloom.org/ "Forums"), and join the conversation!

## LICENSING
The LMAT is licensed under the Apache License, Version 2.0. See LICENSE for full license text.
