import anydbm
from datetime import datetime
from bz2 import BZ2File


def index(redirects, index_map, k):
    """Find the index of an article name after redirect resolution"""
    k = redirects.get(k, k)
    return index_map.setdefault(k, len(index_map))


DBPEDIA_RESOURCE_PREFIX_LEN = len("http://dbpedia.org/resource/")
SHORTNAME_SLICE = slice(DBPEDIA_RESOURCE_PREFIX_LEN + 1, -1)


def short_name(nt_uri):
    """Remove the < and > URI markers and the common URI prefix"""
    return nt_uri[SHORTNAME_SLICE]

def get_redirects(redirects_filename):
    """Parse the redirections and build a transitively closed map out of it"""

    redirects = {}
    print "Parsing the NT redirect file"
    for l, line in enumerate(BZ2File(redirects_filename)):
        split = line.split()
        if len(split) != 4:
            print "ignoring malformed line: " + line
            continue
        redirects[short_name(split[0])] = short_name(split[2])
        if l % 1000000 == 0:
            print "[%s] line: %08d" % (datetime.now().isoformat(), l)

    # compute the transitive closure
    print "Computing the transitive closure of the redirect relation"
    for l, source in enumerate(redirects.keys()):
        transitive_target = None
        target = redirects[source]
        seen = set([source])
        while True:
            transitive_target = target
            target = redirects.get(target)
            if target is None or target in seen:
                break
            seen.add(target)
        redirects[source] = transitive_target
        if l % 1000000 == 0:
            print "[%s] line: %08d" % (datetime.now().isoformat(), l)

    return redirects


def get_links(db, redirects_filename, page_links_filename, limit=None):

    print "Computing the redirect map"
    redirects = get_redirects(redirects_filename)

    print "Computing the integer index map"
    index_map = dict()
    for l, line in enumerate(BZ2File(page_links_filename)):
        split = line.split()
        if len(split) != 4:
            print "ignoring malformed line: " + line
            continue
        u = short_name(split[0])
        v = short_name(split[2])
        if ':' in u or ':' in v:
            continue
        i = index(redirects, index_map, u)
        j = index(redirects, index_map, v)

        # No self loops
        if i == j:
            continue

        db['{0} {1}'.format(i, j)] = '1'

        if l % 1000000 == 0:
            print "[%s] line: %08d" % (datetime.now().isoformat(), l)

        if limit is not None and l >= limit - 1:
            break

    return index_map


def main(args):
    db = anydbm.open('/Users/scott/wikipedia.db', 'n')
    index_map = get_links(db, args.redirects_filename, args.links_filename)
    names = dict((i, name) for name, i in index_map.iteritems())

    with open('datasets/names.map', 'w') as fh:
        for k, v in sorted(names.items()):
            fh.write('{0} {1}\n'.format(k, v))

    with open('/Users/scott/wikipedia.abc', 'w') as fh:
        for k in db:
            u, v = k.split()
            fh.write('{0} {1}\n'.format(u, v))

    db.close()



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Generate ABC link format for wikipedia')
    parser.add_argument('--links-filename', action="store", required=True)
    parser.add_argument('--redirects-filename', action="store", required=True)

    main(parser.parse_args())

