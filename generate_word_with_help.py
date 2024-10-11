import io
from docx import Document
from contextlib import redirect_stdout

def get_help_text(obj):
    """Capture the help() output for a given object as a string."""
    help_text_io = io.StringIO()
    with redirect_stdout(help_text_io):
        help(obj)
    return help_text_io.getvalue()

def add_help_to_word(doc, title, help_text):
    """Add a title and help text to the Word document, starting each on a new page."""
    # Add a page break to start the section on a new page
    doc.add_page_break()
    
    # Add the title for the section
    doc.add_heading(title, level=1)
    
    # Add the help text as a paragraph
    doc.add_paragraph(help_text)

def generate_word_with_help(objects, output_file="help_reference_manual.docx"):
    """Generate a Word document with help output for the given objects."""
    # Create a new Word document
    doc = Document()
    
    # For each object, generate help and add it to the document
    for obj in objects:
        title = f"Help for {obj.__name__}"  # Title of the section
        help_text = get_help_text(obj)
        add_help_to_word(doc, title, help_text)

    # Save the Word document
    doc.save(output_file)
    print(f"Word document generated: {output_file}")

# Example classes to generate help from
class AssetClass1:
    """
    AssetClass1 manages some asset operations.
    
    Example:
    >>> ac = AssetClass1()
    >>> ac.method1(10)
    """

    def method1(self, x):
        """
        Multiplies input by 2.
        
        Example:
        >>> AssetClass1().method1(5)
        10
        """
        return x * 2

class AssetClass2:
    """
    AssetClass2 deals with another type of asset.
    
    Example:
    >>> ac = AssetClass2()
    >>> ac.method2(20)
    """

    def method2(self, y):
        """
        Adds 20 to the input.
        
        Example:
        >>> AssetClass2().method2(10)
        30
        """
        return y + 20

# Generate Word document for the list of classes
asset_classes = [AssetClass1, AssetClass2]
generate_word_with_help(asset_classes)
