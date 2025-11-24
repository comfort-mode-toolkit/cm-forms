from .base import BaseFixer

class AriaRequiredFixer(BaseFixer):
    """
    Fixer to ensure 'required' fields also have 'aria-required="true"'.
    """
    def apply(self):
        # Find all elements with 'required' attribute
        for tag in self.soup.find_all(attrs={"required": True}):
            # Check if aria-required is already present
            if not tag.get('aria-required'):
                tag['aria-required'] = "true"
                self.add_comment(tag, "added-aria-required")
                self.add_change(f"Added aria-required=\"true\" to <{tag.name} id=\"{tag.get('id', 'unknown')}\">")
