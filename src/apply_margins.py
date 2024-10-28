import argparse, os
from pypdf import PaperSize, PdfReader, PdfWriter, Transformation
from common_utils import (
	MARGIN_IN,
	MARGIN_OUT
)

def create_parser():
	parser = argparse.ArgumentParser(description="Command line epub to pdf converter to get print ready pdf with custom font and inside margins being mindful of binding space. Outputs the converted pdf file in same directory as input file with name same as input file but with '--applied-margins' appended to it.")
	parser.add_argument("-i", "--input", required=True, metavar="PDF_FILE", help="path to input epub file")
	return parser

def get_ouput_pdf_path(curr_pdf_path):
	basename = os.path.basename(curr_pdf_path)
	str_to_replace = 'no-final-margins'
	if str_to_replace in basename:
		replaced_basename = basename.replace('no-final-margins','margins-applied')
		parent_dir_path = os.path.dirname(curr_pdf_path)
		return os.path.join(parent_dir_path, replaced_basename)
	else:
		root, ext = os.path.splitext(curr_pdf_path)
		if root.endswith('--') or root.endswith('-'):
			return '{}margins_applied{}'.format(root, ext)
		return '{}--margins_applied{}'.format(root, ext)

def main():
	parser = create_parser()
	args = parser.parse_args()
	book = None
	# shift distance should have only +ve real no as value.
	# shift distance = avg_hori_margin - MARGIN_OUT = (MARGIN_IN - MARGIN_OUT)/2

	shift_distance_mm = (MARGIN_IN - MARGIN_OUT) / 2

	# pypdf assumes A5 paper (w, h) = (420, 595) in px @ 72 ppi
	# we know A5 paper (w, h) = (148, 210) in mm
	# so, formula - 
	# for width, px = mm * 420 / 148
	# for height, px = mm * 595 / 210

	shift_distance_px = shift_distance_mm * 420 / 148

	pg_width = PaperSize.A5.width
	pg_height = PaperSize.A5.height

	if os.path.exists(args.input):
		pdf_path = args.input
		reader = PdfReader(pdf_path)

		writer = PdfWriter()

		# insert front cover
		writer.insert_page(reader.pages[0], 0)

		page_count = reader.get_num_pages()

		print('--- transforming pages')
		for page_num in range(1,  page_count - 1):
			sourcepage = reader.pages[page_num]
			# page num starts from 1. and 1st page will more left margin. so shift content right.
			# for every odd page shift content right
			if page_num % 2 == 0:
				sourcepage.add_transformation(Transformation().translate(-shift_distance_px, 0)) 

			else:
				sourcepage.add_transformation(Transformation().translate(shift_distance_px, 0)) 

			writer.insert_page(sourcepage, page_num)

		# inserting back cover 
		writer.insert_page(reader.pages[page_count - 1], page_count - 1)

		print('--- writing final file')
		with open(get_ouput_pdf_path(pdf_path), 'wb') as fp:
			writer.write(fp)

		print('--- done')

	else:
		print("Oops! input file does not exist. Please check the entered input path and try again.")

if __name__ == '__main__':
	main()