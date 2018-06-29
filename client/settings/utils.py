import os


def get_settings():
    configs = {
        'BROKER_URL': 'amqp://',
        'RESULT_BACKEND': 'amqp://',
    }
    parsed_configs = {
        'user': None,
        'password': None,
        'vhost': None,
        'host': None,
    }

    fname = None
    configsdir = os.path.dirname(__file__)
    configfname = os.path.join(configsdir, 'configure.ini')

    try:
        with open(configfname, 'r') as conf:
            fname = os.path.join(configsdir, conf.readline().strip())
    except:
        return configs

    if os.path.isfile(fname):
        with open(fname, 'r') as conf:
            for line in conf:
                parameter, value = line.strip().split('=')
                if parameter in parsed_configs:
                    parsed_configs[parameter] = value
    else:
        return configs

    # https://www.rabbitmq.com/uri-spec.html
    # amqp_URI       = "amqp://" amqp_authority [ "/" vhost ] [ "?" query ]
    # amqp_authority = [ amqp_userinfo "@" ] host [ ":" port ]
    # amqp_userinfo  = username [ ":" password ]
    amqp_URI = "amqp://"

    amqp_userinfo = ''
    if parsed_configs['user']:
        amqp_userinfo = parsed_configs['user']
        password = parsed_configs['password']
        if password:
            amqp_userinfo += ':{}'.format(password)

    amqp_authority = parsed_configs.get('host') or ''

    if amqp_authority and amqp_userinfo:
        amqp_authority = '{}@{}'.format(amqp_userinfo, amqp_authority)

    if amqp_authority:
        amqp_URI += amqp_authority

    if parsed_configs['vhost']:
        amqp_URI += '/{}'.format(parsed_configs['vhost'])

    configs['RESULT_BACKEND'] = configs['BROKER_URL'] = amqp_URI
    return configs
