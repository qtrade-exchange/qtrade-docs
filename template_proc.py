import json
import jinja2
import yaml
import pprint

data = yaml.load(open('endpoints.yml'))
env_raw = json.load(open('postman_environment.json'))
env_dict = {val['key']: val['value'] for val in env_raw['values']}


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


def json_to_php_array(value):
    value = json.loads(value)
    php_str = "array(\n"
    for k, v in value.items():
        v_str = str(v) if type(v) is int else "\"" + str(v) + "\""
        php_str += "    \"" + str(k) + "\" => " + v_str + ",\n"
    php_str += ")"
    return php_str


env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('.'),
    autoescape=jinja2.select_autoescape(['html', 'xml']),
    trim_blocks=True,
    lstrip_blocks=True
)
env.filters['apply_env'] = apply_env
env.filters['to_pretty_json'] = to_pretty_json
env.filters['json_to_python_dict'] = json_to_python_dict
env.filters['json_to_php_array'] = json_to_php_array

public = [item for item in data['endpoints'] if "user" not in item['request']['url']['path']]
private = [item for item in data['endpoints'] if "user" in item['request']['url']['path']]

template = env.get_template('template.md')
print(template.render(public=public, private=private, env=env_dict, load_snippet=load_snippet))
