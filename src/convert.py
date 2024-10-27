import argparse, ebooklib, os
import zipfile
from ebooklib import epub
from common_utils import ( 
	is_doc, 
	is_css_file, 
	get_doc_files, 
	get_css_files, 
	create_pdf, 
	combine_pdfs,
	CSS_CONTENT
)

'''
1. read epub file
2. generate new content files in diff folder with same name as epub 
3. edit the css
4. give each html/xhtml file to pdf printer which will output pdf(s) with same name as html/xhtml
5. combine all generated pdfs into final one. name it same as epub file. give it '--combined' at end of filename.
'''

def create_parser():
	parser = argparse.ArgumentParser(description="Command line epub to pdf converter to get print ready pdf with custom font and inside margins being mindful of binding space. Outputs the converted pdf file in same directory as input file with name same as input file but with '--no-final-margins' appended to it.")
	parser.add_argument("-i", "--input", required=True, metavar="EPUB_FILE", help="path to input epub file")
	return parser

def main():
	parser = create_parser()
	args = parser.parse_args()
	book = None
	if os.path.exists(args.input):
		input_path = args.input
		extraction_dir, ext = os.path.splitext(input_path)
		zip_path = "{}.zip".format(extraction_dir)
		
		os.rename(input_path, zip_path);
		
		# extract zipfile to folder
		with zipfile.ZipFile(zip_path) as zf:
			zf.extractall(extraction_dir)

		# rename the zip file back to epub
		os.rename(zip_path, input_path)

		# doc files = html + xml files in extracted dir tree
		doc_files = get_doc_files(extraction_dir)

		opf_docnames = []
		epub_book = epub.read_epub(input_path)
		for item in epub_book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
			opf_docnames.append(os.path.normpath(item.get_name()))

		css_files = get_css_files(extraction_dir)
		# inject css in css files
		for css_file in css_files:
			with open(css_file, 'a') as f:
				f.write(CSS_CONTENT)

		# print('--- PRINTING doc_files elements ---')
		# for item in doc_files:
		# 	print(item)

		# print('--- PRINTING opf_docnames list ---')
		# for item in opf_docnames:
		# 	print(item)

		pdf_list = []
		for docname in opf_docnames:
			for doc_path in doc_files:
				if doc_path.endswith(docname):
					# print(f"create_pdf func called with variables - path: {path}, docname: {docname}")
					
					# append css in style tag of that doc if available. and if not available inject style tags wih css.
					# with open(doc_path) as f_xml:
					# 	soup = BeautifulSoup(f_xml, 'html.parser')
					# 	CSS_CONTENT = 'font-family: "Bookman Old Style"; font-size: 11px;'
					# 	if 'style' in soup.html.attrs:
					# 		soup.html['style'] = '{} {}'.format(soup.html['style'], CSS_CONTENT)
					# 	else:
					# 		soup.html['style'] = CSS_CONTENT
					# --- css inject end ---

					pdf_path = "{}.pdf".format(os.path.splitext(doc_path)[0])
					pdf_list.append(pdf_path)
					create_pdf(doc_path)
					break
		
		combine_pdfs(pdf_list, "{}--no-final-margins.pdf".format(extraction_dir))
		print("now you can make any changes to this combined pdf like add or delete pages if needed. use online pdf editing tools for this. for instance - smallpdf.com, pdf2go.com")
		print("combined pdf generated currently has no alternate margins on pages for printing. To apply alternate margins. Run command -")
		print("py apply_margins.py -i PDF_FILE_PATH")

		# works! TODO: append custom css (for font size and family targetting html element with use of !important as necessary) in style tags. if no style tag exist make style tag and then insert css into it. use bs4 or anything as convenient.


	else:
		print("Oops! input file does not exist. Please check the entered input path and try again.")

if __name__ == '__main__':
	main()