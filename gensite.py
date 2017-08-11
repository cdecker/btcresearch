from staticjinja import make_site
from glob2 import glob
import json
import os
import codecs

entries = {}

def main():
    global entries

    s = make_site(
        contexts=[
            ('.*.json', load_publication),
            ('index.html', load_entries),
            ('cabra.bib', load_entries),
        ],
        rules=[
            ('.*.json', render_publication),
        ],
        outpath='output',
        staticpaths=('static/',)
    )
    s.render()

def load_entries(template):
    # Load JSON files
    entries = []
    ids = []
    for fname in glob("publications/**/*.json"):
        entry = json.loads(open(fname, 'r').read())
        if entry['id'] in ids:
            raise ValueError('ID collision with %s' % (entry['id']))
        ids.append(entry['id'])
        entries.append(entry)

    from collections import OrderedDict
    groups = OrderedDict()
    for year in sorted(set([e['year'] for e in entries]))[::-1]:
        groups[year] = []

    for e in entries:
        groups[e['year']].append(e)

    return {'entry_groups': groups}

def load_publication(template):
    with codecs.open(template.filename, encoding='utf-8') as f:
        entry = json.loads(f.read())
        f = template.filename.split('/')
        entry['filename'] = '/'.join(f[f.index('templates') + 1:])
        if 'peer-reviewed' in entry:
            entry['pr'] = entry['peer-reviewed']
        return entry

def render_publication(env, template, **entry):
    """Render a template as a publication."""
    post_template = env.get_template("_publication.html")
    out = "%s/%d/%s.html" % (env.outpath, entry['year'], entry['id'])
    path = os.path.dirname(out)
    if not os.path.exists(path):
        os.makedirs(path)
    post_template.stream(**entry).dump(out)

if __name__ == "__main__":
    if not os.path.exists('output'):
        os.makedirs('output')
    main()
