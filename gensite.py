from staticjinja import make_site
from glob2 import glob
import json
import os
import codecs
import cgi

entries = {}

def main():
    global entries
    
    # Load JSON files
    for fname in glob("publications/**/*.json"):
        entry = json.loads(open(fname, 'r').read())
        entries[entry['id'] + ".json"] = entry

    s = make_site(
        contexts=[
            ('.*.json', load_publication),
            ('index.html', lambda **kwargs: {'entries': entries.values()})
        ],
        rules=[
            ('.*.json', render_publication),
        ],
        outpath='output',
    )
    s.render()

def load_publication(template):
    with codecs.open(template.filename, encoding='utf-8') as f:
        return json.loads(f.read())

def render_publication(env, template, **entry):
    """Render a template as a publication."""
    for i in xrange(len(entry['authors'])):
        entry['authors'][i]['name'] = entry['authors'][i]['name'].encode('utf-8')
    post_template = env.get_template("_post.html")
    out = "%s/%d/%s.html" % (env.outpath, entry['year'], entry['id'])
    path = os.path.dirname(out)
    if not os.path.exists(path):
        os.makedirs(path)
    post_template.stream(**entry).dump(out)

if __name__ == "__main__":
    if not os.path.exists('output'):
        os.makedirs('output')
    main()
