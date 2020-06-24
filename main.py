import pdf_operations
import user_input
import pandas as pd
import pdf_extract_strings
import data
import re


# =========================
# LOCATE STRINGS IN REGIONS
# =========================

# Takes strings and coordinates found and output regions with mismatches
def find_items_in_each_region(strings_and_coords, regions):
    results = {}
    for region in regions:
        pdf_operations.convert_region_coords(region)
        results[region.unique_name] = find_strings_in_region(strings_and_coords, region)
    return results


# Finds which strings exist within region
def find_strings_in_region(strings_and_coords, region):
    strings_in_region = ""
    page = region.page
    strings_on_page = strings_and_coords[str(page)]
    for string_and_coords in strings_on_page:
        if is_string_in_region_bounds(string_and_coords, region.x1, region.y1, region.x2, region.y2):
            text = string_and_coords["string"]
            strings_in_region += text
    print(strings_in_region)
    return strings_in_region


def is_string_in_region_bounds(string_and_coords, x1, y1, x2, y2):
    string_x = string_and_coords["x_pos"]
    string_y = string_and_coords["y_pos"]
    x_valid = x1 <= string_x <= x2
    y_valid = y2 >= string_y >= y1
    return x_valid and y_valid


# ===============================
# SPREADSHEET INFORMATION GETTERS
# ===============================

# Gets the spreadsheet dataframe given the number for the space
def items_and_quantities_in_space(space_numbers):
    queried_df = dataframe.loc[dataframe[user_input.ColumnNames.space_number.value].isin(space_numbers),
                               [user_input.ColumnNames.item_code.value, user_input.ColumnNames.item_qty_per_room.value]]
    return queried_df


# Constructs expected items and quantities array given a region dataframe
def construct_item_array_from_df(region_dataframe):
    output_array = []
    for index, row in region_dataframe.iterrows():
        item_code = row[user_input.ColumnNames.item_code.value]
        item_qty = row[user_input.ColumnNames.item_qty_per_room.value]
        output_array.append({
            "code": item_code,
            "qty": item_qty
        })
    return output_array


# =============================================
# CROSS REFERENCING BETWEEN EXPECTED AND ACTUAL
# =============================================

def items_not_found(expected_items_array, actual_items_string, region):
    failed_to_find = []
    for index in range(len(expected_items_array)):
        item_and_qty = expected_items_array[index]
        item_code = item_and_qty["code"]
        item_qty = item_and_qty["qty"]
        actual_item_qty = return_num_items_found(actual_items_string, item_code)
        if actual_item_qty != item_qty:
            failed_to_find.append({
                "code": item_code,
                "expected_count": item_qty,
                "actual_count": actual_item_qty
            })
    return {"region": region.unique_name, "missing_items": failed_to_find}


def return_num_items_found(item_string, item_to_find):
    matches = re.findall(item_to_find + "[^a-zA-Z0-9]{1}", item_string)
    return len(matches)


# ==================
# MAIN FUNCTIONALITY
# ==================

# 1. Generate rotated PDFs
pdf_operations.generate_rotated_pdfs_for_angles(user_input.pdf_input_filepath, user_input.rotation_angles)

# 2. Get all strings and associated coordinates for each string
# document_strings_and_coords = data.strings_and_coords
# document_strings_and_coords = pdf_extract_strings.get_strings_in_document(user_input.pdf_input_filepath)
items_in_regions = find_items_in_each_region(document_strings_and_coords, user_input.regions)


# 3. Import spreadsheet dataframe
spreadsheet = pd.read_excel(user_input.spreadsheet_input_filepath)
dataframe = pd.DataFrame(spreadsheet, columns=[
    user_input.ColumnNames.item_code.value,
    user_input.ColumnNames.item_qty_per_room.value,
    user_input.ColumnNames.space_number.value
])


# 4. For each region, get the dataframe of expected items
missing_items = []
regions_to_add_to_pdf = []
for region in user_input.regions:
    region_names = region.names
    region_df = items_and_quantities_in_space(region_names)
    expected_region_items = construct_item_array_from_df(region_df)
    region_missing_items = items_not_found(expected_region_items, items_in_regions[region.unique_name], region)

    if len(region_missing_items["missing_items"]) > 0:
        regions_to_add_to_pdf.append(region)
        missing_items.append(region_missing_items)


pdf_operations.generate_pdf_pages_for_regions(
    user_input.pdf_input_filepath,
    user_input.pdf_output_filepath,
    user_input.pdf_output_name,
    regions_to_add_to_pdf
)


print(missing_items)


# 5. Write results to file
file = open(user_input.text_output_filepath, "r+")
file.write(str(missing_items))
file.close()
