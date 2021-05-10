import sys
import os
import json
import logging.config

def setup_logging():
        """Setup logging configuration
        """
    
        default_path='logging.json'
        default_level=logging.INFO
        env_key='LOG_CFG'

        path = default_path
        value = os.getenv(env_key, None)
        if value:
            path = value
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = json.load(f)
                logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)
