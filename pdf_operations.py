from datetime import datetime
import PyPDF2 as PyPDF2
import user_input
import math


# ======================
# COORDINATE CONVERSIONS
# ======================

# Converts pixel coordinates in region to PDF units
def convert_region_coords(selected_region):
    selected_region.x1 = math.floor(selected_region.x1 * width_scaling_factor)
    selected_region.y1 = math.floor(document_pdf_height - selected_region.y1 * height_scaling_factor)
    selected_region.x2 = math.ceil(selected_region.x2 * width_scaling_factor)
    selected_region.y2 = math.ceil(document_pdf_height - selected_region.y2 * height_scaling_factor)


def get_pdf_heights_and_widths(pdf_filepath):
    with open(pdf_filepath, 'rb') as infp:
        reader = PyPDF2.PdfFileReader(infp)
        page = reader.getPage(0)

        pdf_width = page.mediaBox.upperRight[0]
        pdf_height = page.mediaBox.upperRight[1]

        return [pdf_width, pdf_height]


def generate_pdf_pages_for_regions(in_file, out_file_dir, out_file_name, regions):
    now = datetime.now()
    output_file_name = out_file_dir + out_file_name + "-" + str(now.strftime("%m-%d-%y_%H-%M-%S")) + ".pdf"

    with open(in_file, 'rb') as infp:
        writer = PyPDF2.PdfFileWriter()
        for region in regions:
            reader = PyPDF2.PdfFileReader(infp)
            page = reader.getPage(region.page - 1)

            # Crop regions to specified selections
            page.mediaBox.lowerLeft = [region.x1, region.y1]
            page.mediaBox.upperRight = [region.x2, region.y2]

            # Add page to output PDF
            writer.addPage(page)
        with open(output_file_name, 'wb') as output_file:
            writer.write(output_file)
            output_file.close()


# Get document dimensions and scaling to convert pixel coordinates to PDF coordinates
document_pdf_width_and_height = get_pdf_heights_and_widths(user_input.pdf_input_filepath)
document_pdf_width = document_pdf_width_and_height[0]
document_pdf_height = document_pdf_width_and_height[1]
width_scaling_factor = document_pdf_width / user_input.document_pixel_width
height_scaling_factor = document_pdf_height / user_input.document_pixel_height
