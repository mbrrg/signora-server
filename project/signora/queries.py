import logging
from datetime import datetime

def get_current_device_content(device):
    """ retrieves the currently scheduled content given a device """
    now = datetime.now()

    logger = logging.getLogger(__name__)
    logger.debug('now.time = ' + now.time().isoformat())
    logger.debug('now.isoweekday = ' + str(now.isoweekday()))

    result = device.schedule_set.filter(valid_days__iso_weekday__in=[now.isoweekday()],
                                        start__lte=now.time(), end__gte=now.time())

    if result:
        result = result[0].content
        logger.debug('returning url ' + result.static_url)

    return result
