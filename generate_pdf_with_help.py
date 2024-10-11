import io
import reportlab
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from contextlib import redirect_stdout


def get_help_text(obj):
    """Capture the help() output for a given object as a string."""
    help_text_io = io.StringIO()
    with redirect_stdout(help_text_io):
        help(obj)
    return help_text_io.getvalue()


def add_help_to_pdf(c, title, help_text):
    """Add a title and the help text to the PDF, and move to a new page."""
    text = c.beginText(40, 800)  # Start at (40, 800) on each page
    text.setFont("Helvetica", 12)
    text.textLine(title)
    
    text.setFont("Helvetica", 10)
    
    # Split help_text into lines and add to the PDF
    for line in help_text.splitlines():
        text.textLine(line)
    
    c.drawText(text)
    c.showPage()  # Start a new page for the next class/module


def generate_pdf_with_help(objects, output_pdf="help_reference_manual.pdf"):
    """Generate a PDF with help output for the given objects."""
    # Set up PDF canvas
    c = canvas.Canvas(output_pdf, pagesize=A4)
    
    for obj in objects:
        title = f"Help for {obj.__name__}"  # Add a title for the class/module
        help_text = get_help_text(obj)
        add_help_to_pdf(c, title, help_text)

    # Save the PDF
    c.save()

    print(f"PDF generated: {output_pdf}")


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


# Generate PDF for the list of classes
asset_classes = [AssetClass1, AssetClass2]
generate_pdf_with_help(asset_classes)
