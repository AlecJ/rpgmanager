import os
import sys
import requests
from svc import app
from util import loggingFactory


_getLogger = loggingFactory('index')
logger = _getLogger('__main__')
logger.info('running environment: {}'.format(os.environ.get('ENV', '')))

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    debug = os.environ.get('ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug) # Run the app
