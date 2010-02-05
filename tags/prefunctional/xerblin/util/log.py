import logging


logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s %(asctime)s %(name)s :: %(message)s',
    filename='/tmp/xerblin.log',
    )


log = logging.getLogger('xerblin')
