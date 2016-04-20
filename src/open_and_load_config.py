import os
import yaml
import test_attributes_factory

def open_and_load_yaml_file():
    config_dir = os.path.dirname(__file__)
    rel_path = 'config.yml'
    abs_file_path = os.path.join(config_dir, rel_path)

    with open(abs_file_path, 'r') as _ymlfile:
        cfg = yaml.safe_load(_ymlfile)

    return cfg

def get_host_name(cfg):
    configs = [x for x in cfg if x.get('config') != None]
    return configs[0].get('config')[0].get('hostname')

def get_headers(cfg):
    configs = [x for x in cfg if x.get('common') != None]
    return configs[0].get('common')[0].get('headers')

def get_test_attributes(cfg):
    configs = (x for x in cfg if x.get('tests') != None)
    test_list = configs.next()
    test_values = test_list['tests']

    return (test_attributes_factory.build_test_attributes(test) for test in (individual_test.get('test') for
                                                                 individual_test in test_values))

def get_includes(cfg):
    configs = [x for x in cfg if x.get('includes') != None]
    #print(configs[0].get('includes'))
    for c in configs[0].get('includes'):
        print(c)

def generate_url(hostname, attributes):
    url = 'https://{}{}'
    return url.format(hostname, attributes.url)
