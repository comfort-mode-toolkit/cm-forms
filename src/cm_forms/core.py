import os
import shutil

from bs4 import BeautifulSoup
from cm_forms.fixers.label_fixer import LabelFixer
from cm_forms.fixers.aria_required_fixer import AriaRequiredFixer
from cm_forms.fixers.ambiguous_button_fixer import AmbiguousButtonFixer

def process_file(filepath, dryrun=False):
    """
    Process a single HTML file to apply accessibility fixes.
    
    Args:
        filepath (str): Path to the input HTML file.
        dryrun (bool): If True, do not write changes to disk.
        
    Returns:
        dict: A report containing 'output_path', 'changes', and 'warnings'.
    """
    filename, ext = os.path.splitext(filepath)
    output_path = f"{filename}_cm{ext}"
    
    changes = []
    warnings = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    # Register fixers
    fixers = [
        LabelFixer(soup),
        AriaRequiredFixer(soup),
        AmbiguousButtonFixer(soup),
    ]
    
    for fixer in fixers:
        fixer.apply()
        changes.extend(fixer.changes)
        warnings.extend(fixer.warnings)
    
    if not dryrun:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))

    return {
        "output_path": output_path if not dryrun else f"{output_path} (preview)",
        "changes": changes,
        "warnings": warnings
    }
