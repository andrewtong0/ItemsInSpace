from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.layout import LTTextBoxHorizontal, LTTextBoxVertical, LTTextBox, LTTextLine, LTTextGroup, LTFigure, LTTextContainer, LTText, LTTextLineHorizontal, LTTextLineVertical, LTTextGroupLRTB, LTTextGroupTBRL
from pdfminer.converter import PDFPageAggregator
import pdfminer


valid_text_objects = [LTTextBoxHorizontal, LTTextBoxVertical, LTTextLine, LTTextBox, LTTextContainer, LTText, LTTextLineHorizontal, LTTextLineVertical]


# Helper function to get all strings and their coordinate positions
def get_strings_on_page(lt_objs, strings_found_in_region):
    # Iterate through all objects
    for obj in lt_objs:
        # If valid text object is found, add it to the found strings
        if type(obj) in valid_text_objects:
            strings_found_in_region.append({
                "x_pos": obj.bbox[0],
                "y_pos": obj.bbox[1],
                "string": obj.get_text().replace('\n', '_')
            })
        # If object is a container, recurse
        elif isinstance(obj, pdfminer.layout.LTFigure):
            get_strings_on_page(obj._objs, strings_found_in_region)

    return strings_found_in_region


def get_strings_in_document(input_file_directory):
    fp = open(input_file_directory, 'rb')

    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fp)
    document = PDFDocument(parser)

    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    # Instantiate pdfminer variables
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Loops through all pages in document
    strings_dictionary = {}
    page_number = 1
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()

        # Extract text for each page
        strings_dictionary[str(page_number)] = get_strings_on_page(layout._objs, [])
        page_number += 1

    return strings_dictionary


strings_dict = get_strings_in_document("./pdfs/floorplan.pdf")
print(strings_dict)