import pkgutil
import importlib
import inspect

class PackageInspector:
    """
    A class to inspect a Python package and list its modules, classes, functions, and subpackages.
    """

    def __init__(self, package, subpackages=None):
        """
        Initialize the inspector with a package and create containers for storing results.
        
        :param package: The root package to inspect (e.g., `my_package`).
        :param subpackages: List of subpackages to include. If None, inspect all subpackages.
        """
        self.package = package
        self.subpackages_filter = subpackages or []  # List of subpackages to inspect (empty means all)
        self.data = {
            'modules': [],
            'classes': [],
            'functions': [],
            'subpackages': []
        }

    def inspect(self):
        """
        Main method to inspect the package and gather its modules, classes, functions, and subpackages.
        """
        for importer, modname, ispkg in pkgutil.walk_packages(self.package.__path__, self.package.__name__ + "."):
            # Only process if it’s in the list of allowed subpackages, or no filter is applied
            if not self.subpackages_filter or any(modname.startswith(sub) for sub in self.subpackages_filter):
                self._process_module(modname, ispkg)

        return self.data

    def _process_module(self, modname, ispkg):
        """
        Process each module or subpackage found in the package.
        
        :param modname: Name of the module or subpackage.
        :param ispkg: Boolean indicating if it's a package (True) or a module (False).
        """
        try:
            # Dynamically import the module or package
            module = importlib.import_module(modname)

            if ispkg:
                self.data['subpackages'].append(modname)
            else:
                self.data['modules'].append(modname)

            self._extract_members(module, modname)

        except ImportError as e:
            print(f"Error importing {modname}: {e}")

    def _extract_members(self, module, modname):
        """
        Extract classes and functions from the module and store them.
        
        :param module: The module object to inspect.
        :param modname: The module name for filtering its members.
        """
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and obj.__module__ == modname:
                self.data['classes'].append(f"{modname}.{name}")
            elif inspect.isfunction(obj) and obj.__module__ == modname:
                self.data['functions'].append(f"{modname}.{name}")
