import logging
log = logging.getLogger('MyModule')

def doIT():
    log.debug("Doing stuff")
    raise TypeError


