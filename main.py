from cgi import print_arguments
from collections import namedtuple
import io
import json
import os

import camelot
from flask import Flask, jsonify, make_response, request, render_template, flash, send_file
from numpy import column_stack
from werkzeug.utils import redirect, secure_filename
import cached_property
from PDFRecord import JsonData, PDFRecord
import pandas as pd
from io import BytesIO


from singlefileupload import allowed_file
from templates.column_config import Column_config

app = Flask(__name__)
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/hello', methods=['GET'])
def helloworld():
    if request.method == 'GET':
        # dfd.to_dict(orient='records')
        table = camelot.read_pdf('D:\\sumit\\projects\\statement_reader\\camelot-py-pdf-reader\\pnb.pdf', pages='1')
        print(table[0].data)
        table.export('bar.json', f='json')
        return jsonify(table[0].data) 


@app.route('/upload', methods=['POST'])
def upload_file():
    result_json = [];
    pages_to_parse = request.form.get('pages')
    config_data = request.form.get('config')
    print(pages_to_parse)
    print(config_data)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # dfd.to_dict(orient='records')
            table = camelot.read_pdf(os.path.join(app.config['UPLOAD_FOLDER'], filename), pages=pages_to_parse)
            #print(table[0].data)
            #flash('File successfully uploaded')
            #return jsonify(table[0].data)
            print (len(table))
            #config = json.loads(config_data, object_hook = lambda d : namedtuple('X', d.keys()) (*d.values()))
            config = JsonData(config_data)
            print(config.date)
            for x in table:
                print('====================PAGE1===========')
                
                #print(x.data) 
                for y in x.data:
                    pdfRecord = PDFRecord(y[config.date],y[config.particular],y[config.details],y[config.withdrawal],y[config.deposit],y[config.balance])
                    result_json.append(pdfRecord)
                    #print(result_json)
            print(result_json)
            #export_data = pd.DataFrame(result_json)
            #excel_filename = 'exported.xlsx'
            #export_data.to_excel(excel_filename)
            df = pd.read_json(str(result_json))
           # df.to_excel(excel_filename, index=False)


            # Creating output and writer (pandas excel writer)
            out = io.BytesIO()
            writer = pd.ExcelWriter(out, engine='xlsxwriter')

        
            # Export data frame to excel
            df.to_excel(excel_writer=writer, index=False, sheet_name='Sheet1')
            writer.save()
            writer.close()

        
            # Flask create response 
            r = make_response(out.getvalue())

            
            # Defining correct excel headers
            r.headers["Content-Disposition"] = "attachment; filename=export.xlsx"
            r.headers["Content-type"] = "application/x-xls"

            
            # Finally return response
            return r        

            #return redirect('/')
            #return jsonify(result_json)
            #return json.dumps(result_json)
            
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
