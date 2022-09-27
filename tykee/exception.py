from tykee import logger


class TykeeError(Exception):
    """Base class for exceptions."""

    def __init__(self, message):
        super().__init__(message)

    @staticmethod
    def mt_init_failed(name, mt_error):
        """Error for MetaTrader5 initialization fail."""
        msg = f"MT5.initialize() failed, error code = {mt_error}"
        logger.error(msg)
        return TykeeError(f"{name}: {msg}")
