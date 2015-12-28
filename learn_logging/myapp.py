import mymodule,logging

logging.basicConfig()


log=logging.getLogger("MyApp")
print log.level
log.setLevel(10)
print log.level
#print logging.getLevelName('DEBUG')
logging.addLevelName(15,'some_level')
#print logging.getLevelName('some_level')

print log.isEnabledFor(15)
#print log.manager.disable

log.info("Starting my app")

try:
    mymodule.doIT()
except Exception, e:
    log.exception("There was a problem.")

log.info("Ending my app")
