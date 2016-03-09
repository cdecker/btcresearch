from staticjinja import make_site
from glob2 import glob
import json
import os
import codecs
import cgi

entries = {}

def main():
    global entries
    
    s = make_site(
        contexts=[
            ('.*.json', load_publication),
            ('index.html', load_entries)
        ],
        rules=[
            ('.*.json', render_publication),
        ],
        outpath='output',
        staticpaths=('static/',)
    )
    s.render(use_reloader=True)

def load_entries(template):
    # Load JSON files
    entries = []
    for fname in glob("publications/**/*.json"):
        entry = json.loads(open(fname, 'r').read())
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
        return json.loads(f.read())

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
