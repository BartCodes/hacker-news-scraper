class ScraperError(Exception):
    pass

class RobotsTxtError(ScraperError):
    pass

class FetchError(ScraperError):
    pass

class PermissionError(ScraperError):
    pass
    
class ParseError(ScraperError):
    pass

class SaveCsvError(ScraperError):
    pass

class DataExtractionError(ParseError):
    pass 