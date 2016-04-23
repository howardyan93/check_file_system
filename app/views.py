__author__ = 'li'
# -*- coding: gb2312 -*-


from flask import request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os, file_sim_hash, codecs
from app import app

# �ϴ��ļ�����Ŀ¼
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# �����ļ��ϴ��ĸ�ʽ
app.config['ALLOWED_EXTENSIONS'] = set(['txt'])
# �����ļ��ϴ�������С
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# �ж�һ���ļ��Ƿ������ϴ�
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename):
            fname = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            minfilepath, sourcefile, min_distance, sim_percent = file_sim_hash.get_simlar_file(
                os.path.join(app.config['UPLOAD_FOLDER'], fname))
            print(sim_percent)
            if (min_distance > 6):
                return render_template('results.html', sim_percent=sim_percent, result=u'���ظ��ļ�',
                                       sourcefilecontent=sourcefile)
            simfile = codecs.open(minfilepath, 'r', 'gb2312', errors='ignore')
            filecontent = simfile.read()
            print filecontent
            print sourcefile
            simfile.close()
            return render_template('results.html', sim_percent=sim_percent, result=filecontent,
                                   sourcefilecontent=sourcefile)


@app.route('/')
def index():
    return redirect(url_for('upload'), 302)
