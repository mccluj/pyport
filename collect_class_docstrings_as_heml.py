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

def format_to_html(docstrings):
    """
    Formats the collected docstrings into an HTML document.

    Args:
        docstrings (dict): A dictionary containing class and method docstrings.

    Returns:
        str: A string containing the HTML-formatted reference guide.
    """
    output = []
    output.append("<html>")
    output.append("<head><title>API Reference Guide</title></head>")
    output.append("<body>")
    output.append("<h1>API Reference Guide</h1>")

    for class_name, class_info in docstrings.items():
        output.append(f"<h2>Class: {class_name}</h2>")
        
        if class_info['class_doc']:
            output.append(f"<p><strong>Class docstring:</strong><br>{class_info['class_doc']}</p>")
        else:
            output.append("<p><strong>Class docstring:</strong><br>(No docstring provided)</p>")
        
        output.append("<h3>Methods:</h3>")
        for method_name, method_doc in class_info['methods_doc'].items():
            output.append(f"<h4>{method_name}()</h4>")
            if method_doc:
                output.append(f"<p>{method_doc}</p>")
            else:
                output.append("<p>(No docstring provided)</p>")
    
    output.append("</body></html>")
    
    return "\n".join(output)

def save_html_file(html_content, file_name="reference_guide.html"):
    """
    Saves the formatted HTML content to an .html file.

    Args:
        html_content (str): The HTML content to write.
        file_name (str): The name of the output file (default is 'reference_guide.html').
    """
    with open(file_name, "w") as file:
        file.write(html_content)
    print(f"HTML file has been generated and saved as '{file_name}'.")

# Example usage:
module_name = "your_asset_pricing_library"  # Replace with your actual module name
docstrings = collect_class_docstrings(module_name)
html_content = format_to_html(docstrings)
save_html_file(html_content, "api_reference_guide.html")
