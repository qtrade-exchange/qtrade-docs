import json
import jinja2
import pprint

data = json.load(open('postman.json'))
extra = json.load(open('extra.json'))
env_raw = json.load(open('postman_environment.json'))
env_dict = {val['key']: val['value'] for val in env_raw['values']}

for item in data['item']:
    if item['name'] in extra:
        item['extra'] = extra[item['name']]
    else:
        item['extra'] = {}

def apply_env(tmpl):
    template = jinja2.Template(tmpl)
    return template.render(**env_dict)

def load_snippet(name):
    return apply_env(open('snippets/' + name).read())

def to_pretty_json(value):
    value = json.loads(value)
    return json.dumps(value, sort_keys=True, indent=4, separators=(',', ': '))

def json_to_python_dict(value):
    value = json.loads(value)
    return pprint.pformat(value, indent=2)

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('.'),
    autoescape=jinja2.select_autoescape(['html', 'xml']),
    trim_blocks=True,
    lstrip_blocks=True
)
env.filters['apply_env'] = apply_env
env.filters['to_pretty_json'] = to_pretty_json
env.filters['json_to_python_dict'] = json_to_python_dict

public = [item for item in data['item'] if item['request']['url']['path'][1] != "user"]
private = [item for item in data['item'] if item['request']['url']['path'][1] == "user"]

template = env.get_template('template.md')
print(template.render(public=public, private=private, env=env_dict, load_snippet=load_snippet))
