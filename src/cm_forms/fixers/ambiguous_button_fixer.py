from .base import BaseFixer

class AmbiguousButtonFixer(BaseFixer):
    """
    Fixer to detect ambiguous button values/text (e.g. "Submit", "OK", "Button").
    """
    AMBIGUOUS_TEXTS = ["submit", "ok", "button", "click here", "go"]

    def apply(self):
        # Check <button> elements
        for button in self.soup.find_all('button'):
            text = button.get_text(strip=True).lower()
            if text in self.AMBIGUOUS_TEXTS:
                self.add_warning(f"<button> label \"{button.get_text(strip=True)}\" is ambiguous, developer review needed")

        # Check <input type="submit"> and <input type="button">
        for input_tag in self.soup.find_all('input', attrs={'type': ['submit', 'button', 'reset']}):
            value = input_tag.get('value', '').strip().lower()
            if value in self.AMBIGUOUS_TEXTS:
                self.add_warning(f"<input type=\"{input_tag['type']}\"> value \"{input_tag.get('value')}\" is ambiguous, developer review needed")
