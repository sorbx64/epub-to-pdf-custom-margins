import os, pdfkit
from PyPDF2 import PdfMerger

CSS_CONTENT = '\n * { font-family: "Georgia", "Bookman Old Style", sans-serif !important; } \n html { font-size: 11px !important; }\n'

# margins in mm
MARGIN_IN = 25.4  
MARGIN_OUT = 5
MARGIN_TOP = 5
MARGIN_BOTTOM = 5

def is_doc(filename):
	exts = ['.xht', '.xhtml', '.htm', '.html', '.mht', '.mhtml']
	for ext in exts:
		if filename.endswith(ext):
			return True
	return False

def is_css_file(filename):
	exts = ['.css']
	for ext in exts:
		if filename.endswith(ext):
			return True
	return False

def get_doc_files(dir_path):
	files = []
	for root, dirnames, filenames in os.walk(dir_path):
		for filename in filenames:
			if is_doc(filename):
				files.append(os.path.join(root, filename))
	return files

def get_css_files(dir_path):
	files = []
	for root, dirnames, filenames in os.walk(dir_path):
		for filename in filenames:
			if is_css_file(filename):
				files.append(os.path.join(root, filename))
	return files

def create_pdf(doc_path):
	margin_right = ( MARGIN_IN + MARGIN_OUT ) / 2
	margin_left = margin_right
	options = {
		'page-size': 'A5', 
		'margin-top': f'{MARGIN_TOP:.2f}mm', 
		'margin-right': f'{margin_right:.2f}mm', 
		'margin-bottom': f'{MARGIN_BOTTOM:.2f}mm', 
		'margin-left': f'{margin_left:.2f}mm',
		'encoding': 'UTF-8',
		'dpi': '300',
		'enable-local-file-access': '',
		'disable-smart-shrinking': ''
	}
	path_without_ext, ext = os.path.splitext(doc_path)
	print(f"Printing: {doc_path}")
	pdfkit.from_file(doc_path, "{}.pdf".format(path_without_ext), options=options)

def combine_pdfs(pdf_list, output_pdf_path):
	
	merger = PdfMerger()
	for pdf in pdf_list:
		merger.append(pdf, import_outline=False)
	merger.write(output_pdf_path)
	print(f"Success! All pdf combined to form one pdf at {output_pdf_path}")
