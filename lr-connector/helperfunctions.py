import urlparse


def scrubUrl(url):
    up = urlparse.urlparse(url)
    return urlparse.urlunparse((up[0].lower(), up[1].lower(), up[2], up[3], up[4], up[5]))


def readFile(path):
    contents = None;
    try:
        f = open(path, "r")
        try:
            contents = f.read()
        finally:
            f.close()
    except IOError:
        pass
    return contents


def appendToFile(path, line):
    try:
        f = open(path, "a")
        try:
            f.writeline(line)
        finally:
            f.close()
    except IOError:
        pass


def writeFile(path, contents):
    try:
        f = open(path, "w")
        try:
            f.write(contents)
        finally:
            f.close()
    except IOError:
        pass
