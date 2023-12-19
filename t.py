import weakref

class Document:
    def __init__(self, content):
        self.content = content
        print(f"Document created with content: {self.content}")

class Printer:
    def __init__(self):
        self.documents = {}

    def add_document(self, document):
        # Store a weak reference to the document
        self.documents[document] = weakref.ref(document)
        # Attach a finalizer to the document for cleanup
        weakref.finalize(document, self.cleanup, document)

    def cleanup(self, document):
        if document in self.documents:
            print(f"Cleaning up and releasing resources for document: {document.content}")
            del self.documents[document]

    def print_document(self, document):
        print(f"Printing: {document.content}")

# Create a Printer instance
printer = Printer()

# Create a Document instance
doc1 = Document("Hello, World!")

# Add the document to the printer
printer.add_document(doc1)

# Print the document
printer.print_document(doc1)

# Delete the document
del doc1

# The finalizer attached to doc1 should automatically clean up resources
