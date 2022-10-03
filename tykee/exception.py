from tykee import logger


class TykeeError(Exception):
    """Base class for exceptions."""

    def __init__(self, message):
        super().__init__(message)

    @staticmethod
    def value_error(func_name, value, values):
        msg = f"{func_name}: Value '{value}' is not in {values}"
        logger.error(msg)
        return ValueError(msg)

    @staticmethod
    def mt_init_error(name, mt_error):
        """Error for MetaTrader5 initialization fail."""
        msg = f"MT5.initialize() failed, error code = {mt_error}"
        logger.error(msg)
        return TykeeError(f"{name}: {msg}")
