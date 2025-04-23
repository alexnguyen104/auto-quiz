from flask import Flask, render_template, request, session
import os, shutil
from werkzeug.utils import secure_filename
from src.document_processor import process_document
from src.rag_chain_chromadb import create_rag_chain
from src.create_question_file import export_to_pdf

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def clear_session():
    session.clear()

    folders = ['static/uploads/','static/result/']
    for folder in folders:
        try:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    print("cleared old session.")


def ai_process(language, mode, num_questions, file_name, file_paths):
    user_info = {
        "lang": language
    }
    chunks = process_document(source=file_paths, mode=mode, doc_num=len(file_paths))
    print("File processed completely!")

    questions = create_rag_chain(chunks, user_info).invoke(num_questions)
    print("Loading...")

    output_filepath = export_to_pdf(questions, file_name)
    print("Quiz created successfully!")

    return output_filepath

@app.route('/')
def home():
    return render_template('index_image.html', active_page='home')

@app.route('/pdf')
def home_pdf():
    return render_template('index_pdf.html')

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('file')
    n = 0
    for file in files:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        n += 1
        session["filepath_" + str(n)] = filepath

    session["num_doc"] = n
    return {"signal": "upload successfully"}

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.route('/get_form_data', methods=['POST'])
def get_form_data():
    file_name = request.form.get('file_name')
    language = request.form.get('language')
    mode = request.form.get('detail')
    num_questions = request.form.get('num_questions')
    num_doc = session["num_doc"]
    file_paths = []

    for i in range(num_doc):
        file_path = session["filepath_" + str(i + 1)]
        file_paths.append(file_path)

    output_filepath = ai_process(language, mode, num_questions, file_name, file_paths)

    # pass to /result page
    session["output_filepath"] = output_filepath

    # Process the data
    return {"signal": "success"}

@app.route('/result', methods=['GET'])
def result():
    output_filepath = session["output_filepath"]
    return render_template('result.html', output_filepath=output_filepath)

@app.route('/clear_old_session', methods=['POST'])
def clear_old_session():
    clear_session()
    return "success"

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
