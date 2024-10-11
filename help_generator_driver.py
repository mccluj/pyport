import my_package  # Replace with your actual package

def main():
    # Step 1: Inspect only specified subpackages within the package
    subpackages_to_inspect = ["my_package.subpackage1", "my_package.subpackage2"]
    inspector = PackageInspector(my_package, subpackages=subpackages_to_inspect)
    package_data = inspector.inspect()

    # Step 2: Generate the Word document with TOC
    doc_generator = HelpDocumentGenerator(output_file="my_package_reference.docx")
    doc_generator.generate_document(package_data)

if __name__ == "__main__":
    main()
