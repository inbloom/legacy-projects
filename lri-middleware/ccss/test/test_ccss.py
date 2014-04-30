import BeautifulSoup
import ccss
import json
from xml.sax import saxutils

LOG = None
DEBUG = False

def application(environ, start_response):
    global LOG
    LOG = environ["wsgi.errors"]

    global DEBUG

    output = [
        "============",
        "Test Results",
        "============"]

    queriesOpts = [
        ("/subjects", {}),
        ("/subjects", {"format":"json"}),
        ("/subjects", {"format":"json","sort":True}),
        ("/subjects", {"format":"xml"}),
        ("/subjects", {"format":"xml","sort":True}),
        ("/subjects", {"format":"johnxml"}),
        ("/subjects", {"format":"johnxml","sort":True}),
        ("/subjects", {"format":"oldxml"}),
        ("/subjects", {"format":"oldxml","sort":True}),
        ("", {}),

        ("/grade_levels", {"subject":"uri://ccss/subject/ela"}),
        ("/grade_levels", {"subject":"uri://ccss/subject/ela","format":"json"}),
        ("/grade_levels", {"subject":"uri://ccss/subject/ela","format":"json","sort":True}),
        ("/grade_levels", {"subject":"uri://ccss/subject/ela","format":"xml"}),
        ("/grade_levels", {"subject":"uri://ccss/subject/ela","format":"xml","sort":True}),
        ("/grade_levels", {"subject":"uri://ccss/subject/ela","format":"johnxml"}),
        ("/grade_levels", {"subject":"uri://ccss/subject/ela","format":"johnxml","sort":True}),
        ("/grade_levels", {"subject":"uri://ccss/subject/ela","format":"oldxml"}),
        ("/grade_levels", {"subject":"uri://ccss/subject/ela","format":"oldxml","sort":True}),
        ("", {}),

        ("/domains", {"grade_level":"uri://ccss/grade_level/ela/4"}),
        ("/domains", {"grade_level":"uri://ccss/grade_level/ela/4","format":"json"}),
        ("/domains", {"grade_level":"uri://ccss/grade_level/ela/4","format":"json","sort":True}),
        ("/domains", {"grade_level":"uri://ccss/grade_level/ela/4","format":"xml"}),
        ("/domains", {"grade_level":"uri://ccss/grade_level/ela/4","format":"xml","sort":True}),
        ("/domains", {"grade_level":"uri://ccss/grade_level/ela/4","format":"johnxml"}),
        ("/domains", {"grade_level":"uri://ccss/grade_level/ela/4","format":"johnxml","sort":True}),
        ("/domains", {"grade_level":"uri://ccss/grade_level/ela/4","format":"oldxml"}),
        ("/domains", {"grade_level":"uri://ccss/grade_level/ela/4","format":"oldxml","sort":True}),
        ("", {}),

        ("/clusters", {"domain":"uri://ccss/domain/N.VM"}),
        ("/clusters", {"domain":"uri://ccss/domain/N.VM","format":"json"}),
        ("/clusters", {"domain":"uri://ccss/domain/N.VM","format":"json","sort":True}),
        ("/clusters", {"domain":"uri://ccss/domain/N.VM","format":"xml"}),
        ("/clusters", {"domain":"uri://ccss/domain/N.VM","format":"xml","sort":True}),
        ("/clusters", {"domain":"uri://ccss/domain/N.VM","format":"johnxml"}),
        ("/clusters", {"domain":"uri://ccss/domain/N.VM","format":"johnxml","sort":True}),
        ("/clusters", {"domain":"uri://ccss/domain/N.VM","format":"oldxml"}),
        ("/clusters", {"domain":"uri://ccss/domain/N.VM","format":"oldxml","sort":True}),
        ("", {}),

        ("/anchor_standard_sections", {"domain":"uri://ccss/domain/L.4"}),
        ("/anchor_standard_sections", {"domain":"uri://ccss/domain/L.4","format":"json"}),
        ("/anchor_standard_sections", {"domain":"uri://ccss/domain/L.4","format":"json","sort":True}),
        ("/anchor_standard_sections", {"domain":"uri://ccss/domain/L.4","format":"xml"}),
        ("/anchor_standard_sections", {"domain":"uri://ccss/domain/L.4","format":"xml","sort":True}),
        ("/anchor_standard_sections", {"domain":"uri://ccss/domain/L.4","format":"johnxml"}),
        ("/anchor_standard_sections", {"domain":"uri://ccss/domain/L.4","format":"johnxml","sort":True}),
        ("/anchor_standard_sections", {"domain":"uri://ccss/domain/L.4","format":"oldxml"}),
        ("/anchor_standard_sections", {"domain":"uri://ccss/domain/L.4","format":"oldxml","sort":True}),
        ("", {}),

        ("/standards", {"cluster":"uri://ccss/cluster/N.VM.A"}),
        ("/standards", {"cluster":"uri://ccss/cluster/N.VM.A","format":"json"}),
        ("/standards", {"cluster":"uri://ccss/cluster/N.VM.A","format":"json","sort":True}),
        ("/standards", {"cluster":"uri://ccss/cluster/N.VM.A","format":"xml"}),
        ("/standards", {"cluster":"uri://ccss/cluster/N.VM.A","format":"xml","sort":True}),
        ("/standards", {"cluster":"uri://ccss/cluster/N.VM.A","format":"johnxml"}),
        ("/standards", {"cluster":"uri://ccss/cluster/N.VM.A","format":"johnxml","sort":True}),
        ("/standards", {"cluster":"uri://ccss/cluster/N.VM.A","format":"oldxml"}),
        ("/standards", {"cluster":"uri://ccss/cluster/N.VM.A","format":"oldxml","sort":True}),
        ("", {}),

        ("/standard_components", {"standard":"uri://ccss/standard/W.4.1"}),
        ("/standard_components", {"standard":"uri://ccss/standard/W.4.1","format":"json"}),
        ("/standard_components", {"standard":"uri://ccss/standard/W.4.1","format":"json","sort":True}),
        ("/standard_components", {"standard":"uri://ccss/standard/W.4.1","format":"xml"}),
        ("/standard_components", {"standard":"uri://ccss/standard/W.4.1","format":"xml","sort":True}),
        ("/standard_components", {"standard":"uri://ccss/standard/W.4.1","format":"johnxml"}),
        ("/standard_components", {"standard":"uri://ccss/standard/W.4.1","format":"johnxml","sort":True}),
        ("/standard_components", {"standard":"uri://ccss/standard/W.4.1","format":"oldxml"}),
        ("/standard_components", {"standard":"uri://ccss/standard/W.4.1","format":"oldxml","sort":True}),
        ("", {}),

        ("/anchor_standard_sections", {"domain":"uri://ccss/domain/W.4"}),
        ("/anchor_standard_sections", {"domain":"uri://ccss/domain/W.4","format":"json"}),
        ("/anchor_standard_sections", {"domain":"uri://ccss/domain/W.4","format":"json","sort":True}),
        ("/anchor_standard_sections", {"domain":"uri://ccss/domain/W.4","format":"xml"}),
        ("/anchor_standard_sections", {"domain":"uri://ccss/domain/W.4","format":"xml","sort":True}),
        ("/anchor_standard_sections", {"domain":"uri://ccss/domain/W.4","format":"johnxml"}),
        ("/anchor_standard_sections", {"domain":"uri://ccss/domain/W.4","format":"johnxml","sort":True}),
        ("/anchor_standard_sections", {"domain":"uri://ccss/domain/W.4","format":"oldxml"}),
        ("/anchor_standard_sections", {"domain":"uri://ccss/domain/W.4","format":"oldxml","sort":True}),
        ("", {}),

        ("/anchor_standards", 
         {"anchor_standard_section":"uri://ccss/anchor_standard_section/W.4.A"}),
        ("/anchor_standards", 
         {"anchor_standard_section":"uri://ccss/anchor_standard_section/W.4.A","format":"json"}),
        ("/anchor_standards", 
         {"anchor_standard_section":"uri://ccss/anchor_standard_section/W.4.A","format":"json","sort":True}),
        ("/anchor_standards", 
         {"anchor_standard_section":"uri://ccss/anchor_standard_section/W.4.A","format":"xml"}),
        ("/anchor_standards", {"format":"xml","sort":True}),
        ("/anchor_standards", 
         {"anchor_standard_section":"uri://ccss/anchor_standard_section/W.4.A","format":"johnxml"}),
        ("/anchor_standards", 
         {"anchor_standard_section":"uri://ccss/anchor_standard_section/W.4.A","format":"johnxml","sort":True}),
        ("/anchor_standards", 
         {"anchor_standard_section":"uri://ccss/anchor_standard_section/W.4.A","format":"oldxml"}),
        ("/anchor_standards", 
         {"anchor_standard_section":"uri://ccss/anchor_standard_section/W.4.A","format":"oldxml","sort":True}),
        ("", {}),

        ("/strands", {}),
        ("/strands", {"format":"json"}),
        ("/strands", {"format":"json","sort":True}),
        ("/strands", {"format":"xml"}),
        ("/strands", {"format":"xml","sort":True}),
        ("/strands", {"format":"johnxml"}),
        ("/strands", {"format":"johnxml","sort":True}),
        ("/strands", {"format":"oldxml"}),
        ("/strands", {"format":"oldxml","sort":True}),
        ("", {}),

        ("/competency_paths", {}),
        ("/competency_paths", {"format":"json"}),
        ("/competency_paths", {"format":"json","sort":True}),
        ("/competency_paths", {"format":"xml"}),
        ("/competency_paths", {"format":"xml","sort":True}),
        ("/competency_paths", {"format":"johnxml"}),
        ("/competency_paths", {"format":"johnxml","sort":True}),
        ("/competency_paths", {"format":"oldxml"}),
        ("/competency_paths", {"format":"oldxml","sort":True}),
        ("/competency_paths", {"format":"json","author":"Sharren Bates"}),
        ("", {}),

        ("/learning_resources", {}),
        ("/learning_resources", {"format":"json"}),
        ("/learning_resources", {"format":"json","sort":True}),
        ("/learning_resources", {"format":"xml"}),
        ("/learning_resources", {"format":"xml","sort":True}),
        ("/learning_resources", {"format":"johnxml"}),
        ("/learning_resources", {"format":"johnxml","sort":True}),
        ("/learning_resources", {"format":"oldxml"}),
        ("/learning_resources", {"format":"oldxml","sort":True}),
        ("", {}),

        ("/learning_resources", {"competency":"uri://ccss/standard/4.SL.5"}),
        ("/learning_resources", {"competency":"uri://ccss/standard/4.SL.5","format":"json"}),
        ("/learning_resources", {"competency":"uri://ccss/standard/4.SL.5","format":"json","sort":True}),
        ("/learning_resources", {"competency":"uri://ccss/standard/4.SL.5","format":"xml"}),
        ("/learning_resources", {"competency":"uri://ccss/standard/4.SL.5","format":"xml","sort":True}),
        ("/learning_resources", {"competency":"uri://ccss/standard/4.SL.5","format":"johnxml"}),
        ("/learning_resources", {"competency":"uri://ccss/standard/4.SL.5","format":"johnxml","sort":True}),
        ("/learning_resources", {"competency":"uri://ccss/standard/4.SL.5","format":"oldxml"}),
        ("/learning_resources", {"competency":"uri://ccss/standard/4.SL.5","format":"oldxml","sort":True}),
        ("", {})
        ]

    for query, opts in queriesOpts:
        if len(query) == 0:
            output.append("\n")

            LOG.write("\n")
            continue
        try:
            LOG.write("%s : %r" % (query, opts))
            results = testGet(query, opts)
        except TypeError, e:
            # TypeError can come from ccss.py
            output.append("%s: status: FAIL: TypeError: %r" % (query, opts))
            continue
        except AttributeError, e:
            # AttributeRrror can come from ccss.py
            output.append("%s: status: FAIL: AttributeError: %r" % (query, opts))
            continue

        try:
            resultsDict = json.loads(results)
            output.append("%s: status: %s: %r" % (query, str(resultsDict["status"]), opts))
        except ValueError, e:
            # json.loads throws ValueError if format=xml
            if DEBUG is True:
                LOG.write(results)

            if opts["format"] in ["xml", "johnxml", "oldxml"]:
                xml = saxutils.unescape(results)
                soup = BeautifulSoup.BeautifulSoup(xml)
                status = ""

                # xml
                if opts["format"] == "xml":
                    if DEBUG is True:
                        LOG.write("%s\n" % opts["format"])

                    pairTags = soup.findAll("pair")
                    tags = {}
                    for pair in pairTags:
                        key = pair.find("key")
                        if key is not None:
                            keyText = key.getText()
                            val = pair.find("value")
                            if val is not None:
                                valText = val.getText()
                                tags[keyText] = valText
                    status = tags["status"]
                    output.append("%s: status: %s: %r" % (query, str(status), opts))
                    pass

                # johnxml
                elif opts["format"] == "johnxml":
                    if DEBUG is True:
                        LOG.write("%s\n" % opts["format"])

                    status = soup.find(key="status").getText()
                    output.append("%s: status: %s: %r" % (query, str(status), opts))
                    pass

                # oldxml
                elif opts["format"] == "oldxml":
                    if DEBUG is True:
                        LOG.write("%s\n" % opts["format"])

                    status = soup.find("status").getText()
                    output.append("%s: status: %s: %r" % (query, str(status), opts))
                    pass

    headers = [
        ('X-Powered-By', 'Python'),
        ('Content-Type', 'application/json'),
        ('Access-Control-Allow-Origin', '*')
        ]

    start_response("200 OK", headers)

    if DEBUG is True:
        LOG.write("\n\n\n OUTPUT \n")
        LOG.writelines(output)
        LOG.write("\n /OUTPUT \n\n\n")

    if DEBUG is True:
        LOG.write("\n\n\n JOINING OUTPUT \n")
    try:
        outputString = "\n".join(output)
        if DEBUG is True:
            LOG.write(outputString)
    except TypeError, e:
        if DEBUG is True:
            LOG.write("\n !!!!! ERROR JOINING OUTPUT !!!!! \n")
    if DEBUG is True:
        LOG.write("\n JOINED OUTPUT \n\n\n")

    if DEBUG is True:
        LOG.write("\n\n\n RETURNING \n")

    return [outputString]

def testGet(pathInfo, opts={}):
    """Tests ccss get"""

    query = ccss.QueryFactory().CreateQuery(pathInfo, opts)
    runner = ccss.QueryRunner(query.getUrl())
    results = runner.runQuery()
    if not isinstance(results, ccss.QueryResult):
        raise ccss.WrongTypeError("runQuery returned wrong type")

    if opts.has_key("sort") and opts["sort"] == True:
        sorter = ccss.SorterFactory().CreateSorter(pathInfo, results)
        results = sorter.sort()

    toFormat = "json"
    if opts.has_key("format"):
        toFormat = opts["format"]
    formatter = ccss.FormatterFactory().CreateFormatter(results.get(), toFormat)
    formatted = formatter.format()

    return formatted
