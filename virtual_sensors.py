# -*- coding: utf-8 -*-

import time
from src.memory_usage import log_mu
from src.outdoor import log_outdoor

import config as cfg


n = 0  # min count
while True:
    try:
        if n == 60:
            n = 0
        
        # Logging
        log_outdoor()

        if not n % cfg.MU_SAVEEVERY:
            log_mu()

        # Sleep for 1 min
        time.sleep(60)

        n += 1
    except KeyboardInterrupt:
        break
    except:
        continue