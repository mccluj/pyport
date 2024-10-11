import pkgutil
import inspect
import importlib

def list_package_objects(package):
    """
    Generate a list of objects (classes, functions, and subpackages) from a package.

    :param package: The root package to inspect.
    :return: A dictionary containing the package's modules, classes, functions, and subpackages.
    """
    package_objects = {
        'modules': [],
        'classes': [],
        'functions': [],
        'subpackages': [],
    }

    # Process the root package
    for importer, modname, ispkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        try:
            # Dynamically import the module
            module = importlib.import_module(modname)

            if ispkg:
                # If it's a package, add to the subpackages list
                package_objects['subpackages'].append(modname)
            else:
                # Otherwise, add to the modules list
                package_objects['modules'].append(modname)

            # Get all classes and functions from the module
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and obj.__module__ == modname:
                    package_objects['classes'].append(f"{modname}.{name}")
                elif inspect.isfunction(obj) and obj.__module__ == modname:
                    package_objects['functions'].append(f"{modname}.{name}")

        except ImportError:
            print(f"Could not import module: {modname}")
    
    return package_objects


# Example usage with a package
# Assume you have a package named 'my_package' in your Python environment
import my_package  # Replace with your actual package

package_content = list_package_objects(my_package)

# Output the content for inspection
print("Modules:")
for module in package_content['modules']:
    print(module)

print("\nClasses:")
for cls in package_content['classes']:
    print(cls)

print("\nFunctions:")
for func in package_content['functions']:
    print(func)

print("\nSubpackages:")
for subpackage in package_content['subpackages']:
    print(subpackage)
