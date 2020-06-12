# MissingItems
Program to cross-reference with a floor plan with a spreadsheet to check what items are missing in specified regions.

MissingItems is a Python script that analyzes a PDF floor plan, determines what items exist in a set of regions, cross-references the items found with a spreadsheet, and lists the discrepancies between the spreadsheet and the floor plan.

## Dependencies
Pandas - Used for spreadsheet reading (.xlsx)
PyPDF2 - Used for gathering PDF details (e.g. width/height) and PDF generation
pdfminer - Used for extracting locations of items from within a PDF

## How it Works
1. The user specifies an input floor plan PDF, a spreadsheet, and the regions that contain the associated items they want to check for. Regions consist of a unique name (to be identified by humans for readability), a room code (to know which region to check the items for in the spreadsheet), the page number of the floor plan PDF the region is in, and the coordinates for the bottom left and upper right corners of the region.
2. Upon running the script, pdfminer acquires every string in the PDF along with the associated X and Y position of it.
3. We check every string's coordinates against our list of regions to see if is contained within them. If it is, we check the spreadsheet to see if it should be within the region. If we find that it is either not supposed to be in the region, that we find too many of a given item in a region, or we find we don't have enough of an item in a region, we output that information to the user in a report.
4. [TO BE IMPLEMENTED] Any regions where there is a mismatch in the expected items from the spreadsheet and the actual items found on the floor plan are sent to an output PDF to make it easy to check those specific regions and either debug or identify discrepancies.
