import inspect
import doctest
import markdown

def extract_class_docstring(cls):
    """Extract class-level docstring and method docstrings."""
    doc = f"## Class: {cls.__name__}\n\n"
    class_docstring = inspect.getdoc(cls)
    if class_docstring:
        doc += f"**Description:**\n{class_docstring}\n\n"
    return doc

def extract_method_docstrings(cls):
    """Extract method-level docstrings."""
    doc = ""
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        docstring = inspect.getdoc(method)
        if docstring:
            doc += f"### Method: {name}\n\n"
            doc += f"**Docstring:**\n{docstring}\n\n"
    return doc

def extract_doctests(cls):
    """Extract doctests from the class."""
    doc = ""
    finder = doctest.DocTestFinder()
    tests = finder.find(cls)
    for test in tests:
        doc += f"### Doctest for {test.name}:\n\n"
        for example in test.examples:
            doc += f"```python\n{example.source.strip()}\n```\n\n"
            if example.want:
                doc += f"**Expected Output:**\n```\n{example.want.strip()}\n```\n\n"
    return doc

def generate_reference_manual(classes, output_file="reference_manual.md"):
    """Generate a reference manual from the given classes."""
    manual_content = "# Asset Class Reference Manual\n\n"
    
    for cls in classes:
        manual_content += extract_class_docstring(cls)
        manual_content += extract_method_docstrings(cls)
        manual_content += extract_doctests(cls)
        manual_content += "\n\n"

    with open(output_file, "w") as file:
        file.write(manual_content)

    print(f"Reference manual generated: {output_file}")

# Example usage with asset classes
class AssetClass1:
    """
    AssetClass1 handles asset management.
    
    Example:
    >>> ac1 = AssetClass1()
    >>> ac1.method1(10)
    20
    """
    def method1(self, x):
        """
        Multiplies the input by 2.
        
        Example:
        >>> AssetClass1().method1(5)
        10
        """
        return x * 2

class AssetClass2:
    """
    AssetClass2 manages different types of assets.
    
    Example:
    >>> ac2 = AssetClass2()
    >>> ac2.method2(10)
    30
    """
    def method2(self, y):
        """
        Adds 20 to the input.
        
        Example:
        >>> AssetClass2().method2(10)
        30
        """
        return y + 20

# List of asset classes
asset_classes = [AssetClass1, AssetClass2]

# Generate the reference manual
generate_reference_manual(asset_classes)
