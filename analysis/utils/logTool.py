import logging

logger = logging.getLogger(__name__)


def addLogSectionMark(msg):
    logger.info("======{0}======".format(msg))
    return
