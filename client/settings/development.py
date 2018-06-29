import os

from pathlib import Path


ROOT_DIR = Path('/var', 'DevTesting')
TESTS_DIR = ROOT_DIR / 'Tests'
TOOLS_DIR = ROOT_DIR / 'Tools'

PROJECT_DIR = Path(__file__).parents[1]
UTILS_DIR = Path(PROJECT_DIR, 'utils')
WEBIZ_SCRIPTS_DIR = Path(UTILS_DIR, 'tv', 'nonsoap_commands', 'webiz_scripts')

LOGS_DIR = Path('/usr', 'share', 'client', 'logs')
UTIL_LOGS_DIR = LOGS_DIR / 'utils'

CAM_LOG_FILE = Path('/tmp/cam_log')

TV_FIRMWARE_URI = os.environ.get('TV_FIRMWARE_URI', 
                   'http://172.31.14.147:8044/tvfirmware/')


HOSTNAME = os.environ.get('HOSTNAME', 'dev')
