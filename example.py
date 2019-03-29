from v_log import VLogger

log = VLogger()

log.critical("critical")
log.error("error")
log.warning("warning")
log.info("info")
log.debug("debug")


# Show time
log.info("Test time", time=10)

# Show error
try:
    1 / 0
except Exception as e:
    log.error("Try errors", error=e)
    log.error("Try errors %s", "full", time=10, error=e)
