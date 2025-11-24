from abc import ABC, abstractmethod
from bs4 import BeautifulSoup, Tag, Comment

class BaseFixer(ABC):
    """
    Abstract base class for all accessibility fixers.
    """
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup
        self.changes = []
        self.warnings = []

    @abstractmethod
    def apply(self):
        """
        Apply the fix to the soup.
        Should populate self.changes and self.warnings.
        """
        pass

    def add_change(self, message: str):
        self.changes.append(message)

    def add_warning(self, message: str):
        self.warnings.append(message)
    
    def add_comment(self, tag: Tag, message: str, position="before"):
        """
        Add a comment to the HTML.
        """
        comment = Comment(f" cm-forms: {message} ")
        if position == "before":
            tag.insert_before(comment)
        else:
            tag.insert_after(comment)
