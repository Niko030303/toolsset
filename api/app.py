import atexit
import shutil
from flask import Flask, render_template, request, send_file, abort
import os
from pdf_to_word_converter import convert_pdf_to_word
import threading

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

app.config['DOWNLOAD_FOLDER'] = 'downloads'
if not os.path.exists(app.config['DOWNLOAD_FOLDER']):
    os.makedirs(app.config['DOWNLOAD_FOLDER'])

MAX_THREADS = 4  # 最大线程数


def process_file(pdf_file):
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
    pdf_file.save(pdf_path)

    # pdf转换为word
    word_path = convert_pdf_to_word(pdf_path)

    # 构建目标文件路径
    dest_filename = pdf_file.filename.replace('.pdf', '.docx')
    dest_path = os.path.join(app.config['DOWNLOAD_FOLDER'], dest_filename)

    # 将转换后的文件移动到 DOWNLOAD_FOLDER 目录
    shutil.move(word_path, dest_path)

    return dest_path


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('pdf_file')

        # 限制最大线程数
        num_threads = min(len(files), MAX_THREADS)
        threads = []

        converted_files = []  # 转换后的文件路径列表

        for i in range(num_threads):
            thread = threading.Thread(target=process_file, args=(files[i],))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        for file in files:
            word_path = os.path.join(app.config['DOWNLOAD_FOLDER'], file.filename.replace('.pdf', '.docx'))
            converted_files.append(word_path)

        return render_template('upload.html', files=converted_files)

    return render_template('upload.html')


@app.route("/downloads/<filename>")
def download_file(filename):
    # 处理下载请求的逻辑
    # 根据 filename 找到对应的文件，并返回给用户下载

    # 示例代码：
    # 构建文件的绝对路径
    file_path = os.path.join(app.config["DOWNLOAD_FOLDER"], filename)

    # 检查文件是否存在
    if os.path.isfile(file_path):
        # 如果文件存在，返回文件给用户下载
        return send_file(file_path, as_attachment=True)
    else:
        # 如果文件不存在，返回 404 错误
        return abort(404)


@atexit.register
def cleanup_folders():
    # 清空 uploads 文件夹
    shutil.rmtree(app.config['UPLOAD_FOLDER'])

    # 清空 downloads 文件夹
    shutil.rmtree(app.config['DOWNLOAD_FOLDER'])

if __name__ == '__main__':
    app.run(debug=True)