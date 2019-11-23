import json
import yaml
import textwrap

data = json.load(open('postman.json'))


def str_presenter(dumper, data):
    if len(data.splitlines()) > 1:  # check for multiline string
        # if data.startswith("Returns OHLCV"):
        #     print(data)
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    if len(data) > 80:
        return dumper.represent_scalar('tag:yaml.org,2002:str', "\n".join(textwrap.wrap(data, 80)), style='|')
    if " " in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


yaml.add_representer(str, str_presenter)


def proc_url(url, example_path=True, template_path=True):
    variables = {v['key']: v for v in url.get('variable', [])}
    if example_path:
        url['path'] = "/" + "/".join([
            variables[k[1:]]['value'] if k.startswith(":") else k
            for k in url['path']
        ])
    if template_path:
        url['path'] = "/" + "/".join(url['path'])
    url.pop('raw')
    url.pop('host')
    return url


def proc_original_request(req):
    req['url'] = proc_url(req['url'], template_path=False)
    req.pop('header')
    req.pop('method')
    if 'body' in req:
        req['body'] = req['body']['raw']
    return req


def proc_items(items):
    new_items = []
    for item in items:
        t = {}
        t.update(item)
        req = item['request']
        req['url'] = proc_url(req['url'], example_path=False)
        req.pop('auth', None)
        req.pop('header', None)
        if 'body' in req and req['body'].get('mode') == "formdata":
            req['body'].pop('mode')
            req['body']['params'] = req['body']['formdata']
            req['body'].pop('formdata')

        t['response'] = []
        for resp in item['response']:
            body = json.dumps(json.loads(resp['body']),
                              sort_keys=True,
                              indent=4, separators=(',', ': '))
            t['response'].append({
                "body": body,
                "name": resp['name'],
                "code": resp['code'],
                "request": proc_original_request(resp['originalRequest']),
            })

        new_items.append(t)
    return new_items


print(yaml.dump({
    "endpoints": proc_items(data['item']),
}, default_flow_style=False))
