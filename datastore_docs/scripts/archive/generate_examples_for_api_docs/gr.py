# gr.py <urls-file> <request base url> <print base url> <oauth token>
# demo e88cb6d1-771d-46ac-a207-2e58d7f12196
# linda.kim 4cf7a5d4-37a1-ca19-8b13-b5f95131ac85

# python gr.py urls-nocustom http://local.slidev.org:8080/api/rest/v1/ https://localhost/api/rest/v1/ 4cf7a5d4-37a1-ca19-8b13-b5f95131ac85

import sys
import json
import requests
import re

if len(sys.argv) == 5:
    urlfile = open(sys.argv[1])
    base_url = sys.argv[2]
    final_base_url = sys.argv[3]
    token = sys.argv[4]
else:
    exit(0)

headers = {'content-type': 'application/json', 'accept' : 'application/json', 'Authorization' : 'bearer %s' % token}
params = {'limit': '1'}
regex_uuid = re.compile(r'[\w]{8}(-[\w]{4}){3}-[\w]{12}')
crnt_entity_id_default = '{placeholder_id}'

template = """<simplesect xml:id="ex-%s">
    <title>Example request/response for <varname>/%s</varname>
    </title>
    <para>
        Request:
    </para>
    <programlisting>
        <![CDATA[%s]]>
    </programlisting>
    <para>
        Response:
    </para>
    <programlisting language="json">
        <![CDATA[%s]]>
    </programlisting>
</simplesect>"""
#template = """<section xml:id="ex-%s">
#    <title>Example request/response for <varname>/%s</varname>
#    </title>
#    <para>
#        Request:
#    </para>
#    <programlisting><![CDATA[%s]]></programlisting>
#    <para>
#        Response:
#    </para>
#    <programlisting language="json"><![CDATA[%s]]></programlisting>
#</section>"""
##    <para>
#        Optional fields: FIXME... comma-separated list of optional fields (we'll do more with these later)
#    </para>

def print_response(url, req_url, res):
    # generate an xml:id
    url_id = url.replace('{', '').replace('}', '').replace('/', '-')

    # replace the request url with the print url
    req_url = req_url.replace(base_url, final_base_url)
    res = res.replace(base_url, final_base_url)

    # replace UUIDs with generic string <UUID>
    req_url = regex_uuid.sub('<UUID>', req_url)
    res = regex_uuid.sub('<UUID>', res)

    print template % (url_id, url, "GET %s" % req_url, res)

req_good = 0;
req_failed = 0
req_ex_not_available = 0

crnt_entity_id = crnt_entity_id_default
urls = urlfile.read().splitlines()
for url in urls:
    brace_regex = re.compile("\((.)\)")
    r_url = re.sub(r'\([^)]*\)', crnt_entity_id, url.replace('}', ')').replace('{', '('))
    req_url = base_url + r_url

    r = requests.get(req_url, headers=headers, params=params)
    status = r.status_code
    response = r.text

    if status == 404:
        print_response(url, req_url, "Example response not available at this time.")
        req_ex_not_available += 1
        continue
    elif status == 403:
        print_response(url, req_url, "Example response not available at this time.")
        req_failed += 1
        continue
    elif status != 200:
        print_response(url, req_url, "FIIXME error from REST call. (%s)" % status)
        req_failed += 1
        continue

    json_object = json.loads(response)
    response = json.dumps(json_object, sort_keys=True, indent=4)

    if url != "home" and url.find('/') == -1:
        if len(json_object) > 0:
            if len(json_object) > 0 and 'id' in json_object[0]:
                crnt_entity_id = json_object[0]['id']
            req_good += 1
            print_response(url, req_url, response)
        else:
            crnt_entity_id = crnt_entity_id_default
            req_ex_not_available += 1
#            print template % (url_id, url, "GET %s" % req_url, " FIIXME empty response from REST call (1).\n\n%s" % response)
            print_response(url, req_url, "Example response not available at this time.")
    else:
        if 'id' in json_object or len(json_object) > 0:
            req_good += 1
            print_response(url, req_url, response)
        elif len(json_object) == 0:
            req_ex_not_available += 1
#            print template % (url_id, url, "GET %s" % req_url, " FIIXME empty response from REST call(2).\n\n %s" % response)
            print_response(url, req_url, "Example response not available at this time.")
        else:
            req_failed += 1
            print_response(url, req_url, "FIIXME object with no ID returned.")

print "\n\n"
print "succeeded=%d" % req_good
print "not available=%d" % req_ex_not_available
print "failed=%d" % req_failed
