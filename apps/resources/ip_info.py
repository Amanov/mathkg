"""Country and robot hints for the IP addresses in the admin logs.

The country comes from the offline database bundled with ``geoip2fast``,
so nothing is sent to an outside service. It is a hint, not proof: a
VPN or a cloud server shows the country the server stands in.
"""

import ipaddress
import logging
import re
from functools import lru_cache

logger = logging.getLogger(__name__)

# Country names the admin sees most often, in Kyrgyz. Others stay in English.
COUNTRY_NAMES = {
    'KG': 'Кыргызстан', 'KZ': 'Казакстан', 'UZ': 'Өзбекстан', 'TJ': 'Тажикстан',
    'RU': 'Россия', 'TR': 'Түркия', 'CN': 'Кытай', 'US': 'АКШ', 'DE': 'Германия',
    'GB': 'Улуу Британия', 'KR': 'Түштүк Корея', 'JP': 'Япония', 'SG': 'Сингапур',
    'AE': 'БАЭ', 'NL': 'Нидерланд', 'FR': 'Франция', 'IN': 'Индия',
}

# Address blocks of the search engines' crawlers (published by Google and Microsoft).
CRAWLER_NETWORKS = [ipaddress.ip_network(net) for net in (
    '66.249.64.0/19',     # Googlebot
    '64.233.160.0/19',    # Google
    '72.14.192.0/18',     # Google
    '74.125.0.0/16',      # Google
    '40.77.167.0/24',     # Bingbot
    '157.55.39.0/24',     # Bingbot
    '207.46.13.0/24',     # Bingbot
    '52.167.144.0/24',    # Bingbot
    '5.255.231.0/24',     # YandexBot
    '213.180.203.0/24',   # YandexBot
    '87.250.224.0/19',    # Yandex
)]

ROBOT_AGENT = re.compile(
    r'bot|crawl|spider|slurp|preview|scan|fetch|python-|curl|wget|httpclient|headless|okhttp|go-http|java/',
    re.IGNORECASE,
)


@lru_cache(maxsize=1)
def _geo():
    try:
        from geoip2fast import GeoIP2Fast
        return GeoIP2Fast()
    except Exception:  # The admin must still open if the database cannot load.
        logger.exception('Could not load the country database')
        return None


@lru_cache(maxsize=4096)
def country(ip):
    """``('KG', 'Кыргызстан')`` for an address, or ``('', '')`` when unknown."""
    if not ip:
        return '', ''
    geo = _geo()
    if geo is None:
        return '', ''
    try:
        result = geo.lookup(str(ip))
    except Exception:
        return '', ''
    code = (getattr(result, 'country_code', '') or '').strip()
    if not code or code.startswith('--') or len(code) != 2:
        return '', ''
    return code, COUNTRY_NAMES.get(code, getattr(result, 'country_name', '') or code)


def country_label(ip):
    code, name = country(ip)
    return f'{code} · {name}' if code else '-'


def is_robot(ip, user_agent=''):
    """True for a known search-engine crawler address or a robot user agent."""
    if user_agent and ROBOT_AGENT.search(user_agent):
        return True
    if not ip:
        return False
    try:
        address = ipaddress.ip_address(str(ip))
    except ValueError:
        return False
    return any(address in net for net in CRAWLER_NETWORKS)
