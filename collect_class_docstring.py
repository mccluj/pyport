import inspect
import importlib

def collect_class_docstrings(module_name):
    """
    Collects class and method docstrings from a specified module.

    Args:
        module_name (str): The name of the module to inspect.

    Returns:
        dict: A dictionary with class names as keys and a sub-dictionary of method docstrings.
    """
    docstrings = {}
    
    # Dynamically import the module
    module = importlib.import_module(module_name)

    # Iterate through members of the module
    for name, obj in inspect.getmembers(module, inspect.isclass):
        # Get the class docstring
        class_doc = inspect.getdoc(obj)
        methods_doc = {}
        
        # Iterate through methods of the class
        for method_name, method_obj in inspect.getmembers(obj, inspect.isfunction):
            # Get the method docstring
            method_doc = inspect.getdoc(method_obj)
            methods_doc[method_name] = method_doc
        
        # Store the class and method docstrings
        docstrings[name] = {
            'class_doc': class_doc,
            'methods_doc': methods_doc
        }
    
    return docstrings


def format_docstrings(docstrings, output_format='markdown'):
    """
    Formats the collected docstrings into a specified format (e.g., Markdown).

    Args:
        docstrings (dict): A dictionary containing class and method docstrings.
        output_format (str): The format for output ('markdown' or 'rst').

    Returns:
        str: A formatted string containing the reference guide.
    """
    output = []
    
    if output_format == 'markdown':
        for class_name, class_info in docstrings.items():
            output.append(f"# Class `{class_name}`\n")
            if class_info['class_doc']:
                output.append(f"**Class docstring:**\n{class_info['class_doc']}\n")

            if class_info['methods_doc']:
                output.append(f"## Methods:\n")
                for method_name, method_doc in class_info['methods_doc'].items():
                    output.append(f"### `{method_name}`\n")
                    if method_doc:
                        output.append(f"{method_doc}\n")
                    else:
                        output.append("*(No docstring provided)*\n")
            output.append("\n")
    
    # Other formats can be added here (e.g., reStructuredText)
    
    return "\n".join(output)


# Example usage:
module_name = "your_asset_pricing_library"  # Replace with your actual module name
docstrings = collect_class_docstrings(module_name)
formatted_docstrings = format_docstrings(docstrings, output_format='markdown')

# Save to a file (optional)
with open("reference_guide.md", "w") as file:
    file.write(formatted_docstrings)

# Print or use the formatted docstrings
print(formatted_docstrings)
