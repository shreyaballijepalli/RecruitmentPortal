# import sys
# import os
# import comtypes.client

# wdFormatPDF = 17


# # out_file = os.path.abspath(sys.argv[2])

# word = comtypes.client.CreateObject('Word.Application')
# doc = word.Documents.Open("demo1.docx")
# doc.SaveAs("demo1.pdf", FileFormat=wdFormatPDF)
# doc.Close()
# word.Quit()

# import subprocess
# def conversiontopdf():
# 	print("starting conversion to pdf")
# 	import subprocess
# 	output = subprocess.check_output(['libreoffice', '--convert-to', 'pdf' ,'demo.docx'])
# 	print output
# conversiontopdf()

import sys
import subprocess
import re


def convert_to(folder, source, timeout=None):
    args = [libreoffice_exec(), '--headless', '--convert-to', 'pdf', '--outdir', folder, source]

    process = subprocess.check_output(args)


def libreoffice_exec():
    # TODO: Provide support for more platforms
    if sys.platform == 'darwin':
        return '/Applications/LibreOffice.app/Contents/MacOS/soffice'
    return 'libreoffice'


class LibreOfficeError(Exception):
    def __init__(self, output):
        self.output = output


# if __name__ == '__main__':
#    convert_to('/home/elizabeth/Desktop', '/home/elizabeth/Desktop/demo1.docx')

