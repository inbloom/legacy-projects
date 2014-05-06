using System;
using System.IO;
using System.Xml;
using System.Xml.XPath;
using Excel;
using System.Data;
using ICSharpCode.SharpZipLib.Core;
using ICSharpCode.SharpZipLib.Zip;
using System.Text;
using System.Collections.Generic;

namespace Excel2EdFiXML
{
	class MainClass
	{

		public static void Main(string[] args)
		{
			if (ExcelFileExists(args)) {
				string outputPath = "./output";
				string outputXmlPath = "./output/xml";
				outputPath = NormalizePath(outputPath);
				outputXmlPath = NormalizePath(outputXmlPath);

				CreateCleanOutputDirectory(outputXmlPath);

				ProcessExcelWorkbookIntoEdFiXML(args[0]);

				CreateControlFile("MainControlFile.ctl", outputXmlPath);

				CreateZip(outputPath + Path.DirectorySeparatorChar + "EdFiIngestion.zip", outputXmlPath);
			}
		
		}

		/// <summary>
		/// Determines if the Excel file exists or not, if not, display error message.
		/// </summary>
		/// <returns><c>true</c>, if file exists, <c>false</c> otherwise.</returns>
		/// <param name="args">Command line arguments.</param>
		private static bool ExcelFileExists(string[] args)
		{
			if (args == null || args.GetLength(0) <= 0 || args[0].ToLower().IndexOf(".xlsx") <= 0) {
				Console.WriteLine("Please specify a filename for the Excel spreadsheet (xlsx format).");
				Console.WriteLine();
				Console.WriteLine("Usage:  Excel2EdFiXML <Excel File>");
				Console.WriteLine();
				Console.WriteLine();
				return false;
			} else {
				if (!File.Exists(args[0])) {
					Console.Write(args[0]);
					Console.WriteLine(" does not exist.");
					Console.WriteLine();
					Console.WriteLine("Please specify a filename for the Excel spreadsheet (xlsx format).");
					Console.WriteLine();
					Console.WriteLine("Usage:  Excel2EdFiXML <Excel File>");
					Console.WriteLine();
					Console.WriteLine();
					return false;
				} else {
					return true;
				}
			}
		}

		/// <summary>
		/// Creates a clean output directory (if exists, delete and re-create).
		/// </summary>
		/// <param name="outputDirectory">Output directory path.</param>
		private static void CreateCleanOutputDirectory(string outputDirectory)
		{
			if (!Directory.Exists(outputDirectory)) {
				Directory.CreateDirectory(outputDirectory);
			}
			else {
				Directory.Delete(outputDirectory, true);
				Directory.CreateDirectory(outputDirectory);
			}
		}

		/// <summary>
		/// Process an Excel workbook into Ed-Fi XML.
		/// </summary>
		/// <param name="excelFilePath">File path of Excel workbook.</param>
		private static void ProcessExcelWorkbookIntoEdFiXML(string excelFilePath)
		{
			// Open the Excel workbook and map the data to a dataset
			FileStream stream = File.Open(excelFilePath, FileMode.Open, FileAccess.Read);
			IExcelDataReader excelReader = ExcelReaderFactory.CreateOpenXmlReader(stream);
			DataSet sheets = excelReader.AsDataSet();
			sheets = MapColumnNamesFromFirstRow(sheets);

			// For each spreadsheet/tab in the Excel workbook, create a Ed-Fi XML file
			foreach (DataTable table in sheets.Tables) {
				try {
					// Parse Excel spreadsheet and convert to XML
					XmlDocument xmlDoc = new XmlDocument();
					XmlElement xmlRows = xmlDoc.CreateElement("rows");
					XmlElement xmlRow;
					XmlElement xmlItem;
					xmlDoc.AppendChild(xmlRows);
					XmlDeclaration xmlDec = xmlDoc.CreateXmlDeclaration("1.0", null, null);
					xmlDoc.InsertBefore(xmlDec, xmlRows);
					foreach (DataRow row in table.Rows) {
						xmlRow = xmlDoc.CreateElement("row");
						foreach (DataColumn col in table.Columns) {
							if (row[col] != null && row[col].ToString() != string.Empty) {
								xmlItem = xmlDoc.CreateElement(col.ColumnName);
								if (row[col] is DateTime) {
									xmlItem.InnerText = ((DateTime)row[col]).Date.ToString("yyyy-MM-dd");
								}
								else {
									xmlItem.InnerText = row[col].ToString();
								}
								xmlRow.AppendChild(xmlItem);
							}
						}
						xmlRows.AppendChild(xmlRow);
					}

					// Transform XML into Ed-Fi XML using XSLT
					string xslFileName = "./xsl/" + table.TableName + ".xsl";
					if (!File.Exists(xslFileName)) {
						Console.WriteLine("WARNING: XSL does not exist for Excel spreadsheet: " + table.TableName);
					}
					else {
						System.Xml.Xsl.XslCompiledTransform xsl = new System.Xml.Xsl.XslCompiledTransform();
						xsl.Load(xslFileName);
						// StringWriter writer = new StringWriter();
						string outputEdFiXmlFileName = "./output/xml/" + table.TableName + ".xml";
						StreamWriter writer = new StreamWriter(outputEdFiXmlFileName);
						xsl.Transform(xmlDoc.CreateNavigator(), null, writer);
						writer.Close();

						XmlDocument edFiXml = new XmlDocument();
						edFiXml.Load(outputEdFiXmlFileName);

						// Remove empty nodes for optional fields within the Excel spreadsheet
						XmlNodeList emptyElements = edFiXml.SelectNodes(@"//*[not(descendant::text()[normalize-space()])]");
						for (int i = emptyElements.Count - 1; i > -1; i--)
						{
							XmlNode nodeToBeRemoved = emptyElements[ i ];
							nodeToBeRemoved.ParentNode.RemoveChild(nodeToBeRemoved);
						}

						writer = new StreamWriter(outputEdFiXmlFileName);
						edFiXml.Save(writer);
						writer.Close();
					}
				} catch (Exception ex) {
					Console.WriteLine("ERROR:  Cannot process tab: " + table.TableName);
					Console.WriteLine();
					Console.WriteLine(ex.Message);
				}
			}
		}

		/// <summary>
		/// Creates the ingestion control file.  Entitymapping.txt is a static config file
		/// which must exist to specify which files map to Ed-Fi entities in the control
		/// file.
		/// </summary>
		/// <param name="controlFile">Control file.</param>
		/// <param name="path">Path.</param>
		private static void CreateControlFile(string controlFile, string path) {
			// Read the entity mapping file

			bool entitiesMapped = false;
			string line;
			Dictionary<string, string> entityMappingList = new Dictionary<string, string>();
			string[] keyvalue;

			if (File.Exists("entitymapping.txt")) {
				StreamReader entityMapping = new StreamReader("entitymapping.txt");
				while((line = entityMapping.ReadLine()) != null)
				{
					keyvalue = line.Split(',');
					if (keyvalue != null && keyvalue.GetLength(0) == 2) {
						entityMappingList.Add(keyvalue[0], keyvalue[1]);
					}
				}
				entityMapping.Close();

				if (entityMappingList.Count > 0) {
					entitiesMapped = true;
				}
			} else {
				Console.WriteLine("entitymapping.txt file does not exist");
			}

			if (entitiesMapped) {
				if (Directory.Exists(path)) {
					StringBuilder sb = new StringBuilder();
					string fileName;
					string entityName;

					foreach (string fullFileName in Directory.EnumerateFiles(path,"*.xml")) {
						using (StreamReader sr = new StreamReader(fullFileName)) {
							if (fullFileName.IndexOf(Path.DirectorySeparatorChar) > 0) {
								fileName = fullFileName.Substring(fullFileName.LastIndexOf(Path.DirectorySeparatorChar) + 1);
							} else {
								fileName = fullFileName;
							}

							entityName = fileName.Substring(0, fileName.IndexOf(".xml"));

							if (entityMappingList.ContainsKey(entityName)) {
								sb.AppendFormat("edfi-xml,{0},{1}", entityMappingList[entityName], fileName);
								sb.AppendLine();
							} else {
								Console.WriteLine("WARNING:  Skipping file, could not find entity mapping for: " + entityName);
							}
						}
					}

					using (StreamWriter outfile = new StreamWriter(path + @"/MainControl.ctl")) {
						outfile.Write(sb.ToString());
					}
				} else {
					Console.Write("ERROR:  Error creating control file, path does not exist: " + path);
				}
			}
		}

		/// <summary>
		/// Get the column names from the first row in each file and rename the column tables in the data set.
		/// </summary>
		/// <returns>The column names from first row.</returns>
		/// <param name="dataSet">Data set.</param>
		private static DataSet MapColumnNamesFromFirstRow(DataSet dataSet)
		{
			foreach (DataTable table in dataSet.Tables) {
				if (table.Rows.Count == 0)
					continue;
				foreach (DataColumn dc in table.Columns) {

					string colName = table.Rows[0][dc.Ordinal].ToString().Trim();
					colName = colName.Replace(" ", "");
					if (!string.IsNullOrEmpty(colName) && !table.Columns.Contains(colName)) {

						table.Columns[dc.Ordinal].ColumnName = colName;
					}
				}
				table.Rows[0].Delete();
			}
			dataSet.AcceptChanges();
			return dataSet;
		}

		/// <summary>
		/// Create a zip file of the output XML files and control file.
		/// </summary>
		/// <param name="outPathname">Output file name.</param>
		/// <param name="folderName">Input folder name.</param>
		private static void CreateZip(string outPathname, string folderName) {

			FileStream fsOut = File.Create(outPathname);
			ZipOutputStream zipStream = new ZipOutputStream(fsOut);

			int folderOffset = folderName.Length + (folderName.EndsWith(Path.DirectorySeparatorChar.ToString()) ? 0 : 1);

			CompressFolder(folderName, zipStream, folderOffset);

			zipStream.IsStreamOwner = true;
			zipStream.Close();
		}

		/// <summary>
		/// Compresses the folder.
		/// </summary>
		/// <param name="path">Path.</param>
		/// <param name="zipStream">Zip stream.</param>
		/// <param name="folderOffset">Folder offset.</param>
		private static void CompressFolder(string path, ZipOutputStream zipStream, int folderOffset) {

			string[] files = Directory.GetFiles(path);

			foreach (string filename in files) {

				FileInfo fi = new FileInfo(filename);

				string entryName = filename.Substring(folderOffset); // Makes the name in zip based on the folder
				entryName = ZipEntry.CleanName(entryName); // Removes drive from name and fixes slash direction
				ZipEntry newEntry = new ZipEntry(entryName);
				newEntry.DateTime = fi.LastWriteTime; // Note the zip format stores 2 second granularity
				newEntry.Size = fi.Length;

				zipStream.PutNextEntry(newEntry);

				// Zip the file in buffered chunks
				// the "using" will close the stream even if an exception occurs
				byte[ ] buffer = new byte[4096];
				using (FileStream streamReader = File.OpenRead(filename)) {
					StreamUtils.Copy(streamReader, zipStream, buffer);
				}
				zipStream.CloseEntry();
			}
			string[ ] folders = Directory.GetDirectories(path);
			foreach (string folder in folders) {
				CompressFolder(folder, zipStream, folderOffset);
			}
		}
	
		/// <summary>
		/// Normalizes a path between Windows and UNIX/Linux/Mac
		/// </summary>
		/// <param name="path">Path.</param>
		private static string NormalizePath(string path) {
			string normalizedPath = path;

			if (path.Contains("/") && '/' != Path.DirectorySeparatorChar) {
				normalizedPath = normalizedPath.Replace("/", Path.DirectorySeparatorChar.ToString());
			} else {
				if (path.Contains(@"\") && '\\' != Path.DirectorySeparatorChar) {
					normalizedPath = normalizedPath.Replace(@"\", Path.DirectorySeparatorChar.ToString());
				}
			}

			return normalizedPath;
		}
	}
}
