# EPUB to PDF with book margins

## Overview 

Command Line programs for converting epub book to pdf using pdfkit (i.e. wkhtmltopdf). And applying inside margins on pdf so that when it is printed as a book it will have text a little away from binding region increasing readabiliy.

## Prequisites for running

1. Install Python version >= 3.11.5. As programs were tested on this version only, but it should work fine in older versions as well. Don't forget to add python to the path environment variable, although in windows, python installer itself does it by giving you option to tick checkbox `add to path`.

1. Install **wkhtmltopdf** from [here](https://wkhtmltopdf.org/downloads.html) if you haven't already. Add wkhtmltopdf's bin folder to path environment variable.

1. Make sure you have "Georgia" or "Bookman Old Style" font installed in your system. Check font settings in window settings to find out. If no such font is installed, install from [here](https://www.cufonfonts.com/font/georgia-2)

## Running 

### Setup project folder

1. Clone project folder using -
	```powershell
	git clone https://github.com/sorbx64/epub-to-pdf-custom-margins.git
	```

### Setup python virtual environment (venv)

1. Open this project folder in cmd. And run -
	```powershell
	python -m venv .venv 
	```
	it creates python virual environment in .venv folder

2. Now, To activate the python virtual environment. Run -
	 ```powershell
	 .venv\Scripts\activate
	 ```
	 prompt will have (.venv) in from now, indicating virtual env is active.

3. Installing dependencies from requirements.txt
	```powershell
	pip install -r requirements.txt
	```
	wait till it installs the dependencies and setup is complete.

### Making pdf from epub

1. Run -
	```powershell
	python src\convert.py -i EPUB_FILE_PATH
	```
	Note: enclose the path in double quotes if it has space in folder or filename.
	- `convert.py` - converts given epub file into pdf with font "Georgia" and base font size 11px. If "Georgia" font is not available it will use "Bookman Old Style" font. If this is not available on system as well then it will use sans-serif.
	- If `convert.py` fails to make pdf from epub file. Or even if it creates pdf whose look is not upto mark. Do the following. You will notice it has created a folder with same name as epub file in same location as epub file. You can make changes to css files inside of this folder to get the desired appearance in pdf. After you have made changes follow next step.

1. Run -
	```powershell
	python src\convert_unzipped.py -i UNZIPPED_FOLDER_PATH
	```
	- `convert_unzipped.py` - converts html, xhtml in given directory to pdfs and then combines to form final pdf.

### Editing pdfs

- Use online tools line pdf2go and smallpdf to Remove unnecessary or blank pages from pdf. 
- These tools can also be use to give front and back cover to pdf. it it already doesnt have it. just add a cover image at start of pdf. Make sure it has same aspect ratio as A5 page. Add a colored page at end of pdf pages that you want to use as back cover.
- download the final pdf from these tools

### Apply alternate margins to pdf

1. Run following command on edited pdf -
	```powershell
	python src\apply_margins.py -i EDITED_PDF_PATH
	```
- `apply_margins.py` - It translates content of pages towards left or right, alternating over all the pages, except for 1st and last page of pdf i.e. front cover and back cover.
- It saves modified pdf as a separate file with '--margins-applied' text at end of filename.
- Increases readibility of content after book is printed, as no text is lost in binding area.