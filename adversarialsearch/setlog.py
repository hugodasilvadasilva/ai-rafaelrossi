import logging

"""
Description
---------
Set log configuration at formmat `dd/mm/aaaa hh:mn:ss am/pm message`.
The log level must be informe at `level` variable.

Levels
----------
Define log level by setting `level` variable with some of the followings
values:
- logging.DEBUG,
- logging.INFO,
- logging.WARNING,
- logging.ERROR,
- logging.CRITICAL.

"""

def set_log(level: logging):
    
    logging.basicConfig(format="%(asctime)s # At %(funcName)s # Line %(lineno)d # %(message)s", level=level, datefmt='%d/%m/%Y %I:%M:%S %p')

    logging.debug("Log de debug registrado")
    logging.info("Log de info registrado")
    logging.warning("Log de warning registrado")
    logging.error("Log de error registrado")
    logging.critical("Log crítico registrado")