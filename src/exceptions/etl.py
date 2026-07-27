class ETLException(Exception):
    """Base exception for ETL pipeline errors."""


class ConfigurationError(ETLException):
    """Raised when application configuration is invalid."""


class ExtractionError(ETLException):
    """Raised when data extraction fails."""


class TransformationError(ETLException):
    """Raised when data transformation fails."""


class StorageError(ETLException):
    """Raised when data storage fails."""