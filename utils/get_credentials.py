import configparser
import pathlib
from utils.logging import get_log_object
import sys

log = get_log_object()


def get_api_news_credential(ini_file_credentials: str = 'news_api_credential.ini',
                            path_to_credentials_ini_file='credentials/') -> str:

    full_path = path_to_credentials_ini_file + ini_file_credentials
    if not pathlib.Path(full_path).exists():
        log.error('Missing %s configurations file, create one and place it at %s ',
                  ini_file_credentials, path_to_credentials_ini_file)
        log.error('The app will stop now...')
        sys.exit()

    # get api key
    config = configparser.ConfigParser()
    config.read(full_path)
    apiNews_string = config['NEWSAPI']['api_key_aux']

    return apiNews_string
