import json
import os
import sys
import urllib
import web

import httpconfig

"""uWSGI / web.py test app"""

urls = ( "/test/", "index")

class index:
    def GET(self):
        httpConfig = httpconfig.HttpConfig(web.ctx.env["DOCUMENT_ROOT"])
        url = 'http://%s:%d/entity/search?q={"uri://lri/property_type/types":"uri://lri/object_type/subject"}&opts={"use_cached":false}' % (httpConfig.config["serverhost"], httpConfig.config["serverport"])

        fh = urllib.urlopen(url)
        code = fh.code
        json = fh.read()
        headers = fh.headers

        result = ["\nurl: %s" % url]
        result.append("\nenv: ")
        env = web.ctx.env
        for key in sorted(env.keys()):
            result.append("\t%s: %s" % (key, env[key]))

        result.append("\nheaders: ")
        for h in headers:
            result.append("\t%s: %s" % (h, fh.headers.getheader(h)))
        fh.close()

        result.append("\nquery: ")
        result.append(json)
        result.append("\n")

        headers = [
            ('X-Powered-By', 'Python'),
            ('Content-Type', 'application/json'),
            ('Access-Control-Allow-Origin', '*')
            ]
        return "\n".join(result)


app = web.application(urls, globals())
application = app.wsgifunc()

if __name__ == '__main__':
    app.run()
