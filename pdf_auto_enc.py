import argparse
import csv
import os
import secrets
import string

import PyPDF2

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PDF Auto Encrypter')
    parser.add_argument('in_f', help='Folder path to input PDF files')
    parser.add_argument('out_f', help='Folder path to output PDF files')
    parser.add_argument('pwd', help='File to store the password')
    parser.add_argument('pwd_len', type=int, help='Length of the password')
    args = parser.parse_args()
    
    if not os.path.exists(args.in_f):
        print('Folder path to input PDF files does not exist')
        exit(1)
    
    if not os.path.exists(args.out_f):
        os.makedirs(args.out_f)
    
    with open(args.pwd, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'password'])
        for file in os.listdir(args.in_f):
            if file.endswith('.pdf'):
                pdf = PyPDF2.PdfReader(os.path.join(args.in_f, file))
                password = ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(args.pwd_len))
                writer.writerow([os.path.splitext(file)[0], password])
                pdf_writer = PyPDF2.PdfWriter()
                for page_num in range(len(pdf.pages)):
                    pdf_writer.add_page(pdf.pages[page_num])
                pdf_writer.encrypt(password)
                with open(os.path.join(args.out_f, file), 'wb') as out:
                    pdf_writer.write(out)
        
    