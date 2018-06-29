import re
from urllib.parse import urlparse

from client.utils.osutils import network


LOCATION_REX = re.compile(r'.*LOCATION: (.*)/happy.*')


def __get_tv_urls_gen(upnp_results):
    for result in upnp_results:
        match = LOCATION_REX.search(result)
        if match:
            yield match.group(1)


def get_tv_upnp_list():
    byte_res = network.send_upnp_request()

    str_res_gen = (res.decode() for res in byte_res)
    tv_urls_gen = __get_tv_urls_gen(str_res_gen)
    parsed_urls = (urlparse(url) for url in tv_urls_gen)

    ips_set = set(urlobj.hostname for urlobj in parsed_urls)

    return tuple(ips_set)
