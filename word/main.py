"""docstring"""

from spire.doc import *
from spire.doc.common import *

# Create a Document object
doc = Document()

# Add a section
section = doc.AddSection()

# Set the page margins
section.PageSetup.Margins.All = 40

# Add a title
titleParagraph = section.AddParagraph()
titleParagraph.AppendText("Introduction of Spire.Doc for Python")

# Add two paragraphs
bodyParagraph_1 = section.AddParagraph()
bodyParagraph_1.AppendText(
    "Spire.Doc for Python is a professional Python library designed for developers to "
    + "create, read, write, convert, compare and print Word documents in any Python application "
    + "with fast and high-quality performance."
)

bodyParagraph_2 = section.AddParagraph()
bodyParagraph_2.AppendText(
    "As an independent Word Python API, Spire.Doc for Python doesn't need Microsoft Word to "
    + "be installed on neither the development nor target systems. However, it can incorporate Microsoft Word "
    + "document creation capabilities into any developers' Python applications."
)

# Apply heading1 to the title
titleParagraph.ApplyStyle(BuiltinStyle.Heading1)

# Create a style for the paragraphs
style2 = ParagraphStyle(doc)
style2.Name = "paraStyle"
style2.CharacterFormat.FontName = "Arial"
style2.CharacterFormat.FontSize = 13
doc.Styles.Add(style2)
bodyParagraph_1.ApplyStyle("paraStyle")
bodyParagraph_2.ApplyStyle("paraStyle")

# Set the horizontal alignment of the paragraphs
titleParagraph.Format.HorizontalAlignment = HorizontalAlignment.Center
bodyParagraph_1.Format.HorizontalAlignment = HorizontalAlignment.Left
bodyParagraph_2.Format.HorizontalAlignment = HorizontalAlignment.Left

# Set the after spacing
titleParagraph.Format.AfterSpacing = 10
bodyParagraph_1.Format.AfterSpacing = 10

# Save to file
doc.SaveToFile("output/WordDocument.docx", FileFormat.Docx2019)
