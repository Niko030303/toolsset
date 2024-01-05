from pdf2docx import Converter

def convert_pdf_to_word(pdf_path):
    word_path = pdf_path.replace('.pdf', '.docx')

    cv = Converter(pdf_path)
    cv.convert(word_path, start=0, end=None)
    cv.close()

    return word_path