import enum


class ColumnNames(enum.Enum):
    item_code = "ITEM CODE   (PER SPEC DOC)"
    item_qty_per_room = "QTY/ROOM"
    space_number = "SPACE #"


# Defines a square region on the PDF, classified by a name, page number, and bottom left/upper right corner
class Region:
    def __init__(self, unique_name, names, page, x1, y1, x2, y2):
        self.unique_name = unique_name
        self.names = names
        self.page = page
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


regions = [
    Region("1415-K013", ["K013"], 2, 2194, 800, 2320, 640),
    Region("1417-K013", ["K013"], 2, 2318, 800, 2440, 640),
    Region("1100-C1b/C9/C10", ["C001B", "C009", "C010"], 2, 2010, 2900, 2320, 2355),
]
spreadsheet_input_filepath = "./input/spreadsheet.xlsx"
pdf_input_filepath = "./input/floorplan.pdf"
pdf_output_filepath = "./output/"
pdf_output_name = "results"
text_output_filepath = "./output/output.txt"

# TODO: Automate this in main.py
document_pixel_width = 4680
document_pixel_height = 3311
