import my_package  # Replace with your package name

def main():
    # Step 1: Inspect the package to gather data
    inspector = PackageInspector(my_package)
    package_data = inspector.inspect()

    # Step 2: Generate the Word document using the gathered package data
    doc_generator = HelpDocumentGenerator(output_file="my_package_reference.docx")
    doc_generator.generate_document(package_data)

if __name__ == "__main__":
    main()
