from flask import Flask
from flask import render_template, request, url_for, redirect, session
from client import Client
from process import parse_answer
from pathlib import Path
import time
import uuid
import shutil
from threading import Thread
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
if not Path('uploads').exists():
    Path('uploads').mkdir()
app.config['UPLOAD_FOLDER'] = Path('uploads')

client = Client()

tasks = {}

def generate_answer(message, task_id):
    try:
        answer = client.chat(message)
        tasks[task_id]['answer'] = answer
    except Exception as e:
        print(f"An error occurred: {e}")
        tasks[task_id]['answer'] = "Error"
        tasks[task_id]['error'] = e
    finally:
        if tasks[task_id]['answer'] == "Error":
            print(f"Task {task_id} did not complete successfully.")

@app.route('/')
def start():  # put application's code here
    return render_template('index.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        task_id = str(uuid.uuid4())
        tasks[task_id] = {}
        session['task_id'] = task_id
        session['start_time'] = time.time()

        unique_folder = app.config['UPLOAD_FOLDER'] / task_id
        unique_folder.mkdir(parents=True, exist_ok=True)
        uploaded_files = request.files.getlist('file[]')
        file_names = []
        for file in uploaded_files:
            if file.filename != '':
                file_path = unique_folder / file.filename
                file.save(file_path)
                file_names.append(file.filename)

        if file_names:
            message = request.form['idea'] + "\n" + client.files2text(unique_folder)
            time.sleep(1)
        else:
            message = request.form['idea']
        shutil.rmtree(unique_folder)

        session['message'] = message
        Thread(target=generate_answer, args=(message,task_id)).start()
        return redirect(url_for('loading'))

    return render_template('generate.html')

@app.route('/loading')
def loading():
    start_time = session.get('start_time', time.time())
    elapsed_time = round(time.time() - start_time, 2)
    return render_template('loading.html', start_time=start_time,elapsed_time=elapsed_time)

@app.route('/check_status')
def check_status():
    task_id = session.get('task_id')
    if not task_id or (task_id in tasks and 'answer' in tasks[task_id]):
        return {'result_ready': True}
    else:
        return {'result_ready': False}

@app.route('/result')
def result():
    if task_id := session.get('task_id'):
        task = tasks[task_id]
    else:
        return render_template('index.html')
    if 'answer' in task:
        answer = task['answer']
        if answer == "Error":
            print(tasks)
            tasks.pop(task_id)
            session.pop('task_id')
            return render_template("error.html", error_message=task['error'])
        answer = parse_answer(answer)
        return render_template('bmc.html',
                               key_partners=answer['key_partners'],
                               key_activities=answer['key_activities'],
                               key_resources=answer['key_resources'],
                               value_proposition=answer['value_propositions'],
                               customer_relationship=answer['customer_relationships'],
                               channels=answer['channels'],
                               customer_segments=answer['customer_segments'],
                               cost_structure=answer['cost_structure'],
                               revenue_streams=answer['revenue_streams'],
                               response_time=round(time.time() - session['start_time'], 2))
    else:
        return redirect(url_for('loading'))

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        q1 = request.form['question1']
        q2 = request.form['question2']
        q3 = request.form['question3']
        q4 = request.form['question4']
        q5 = request.form['question5']
        q6 = request.form['question6']
        q7 = request.form['question7']
        q8 = request.form['question8']
        q9 = request.form['question9']
        # TODO: construct a message to send to the chatbot
        message = (f"Construct a Business Canvas Model according to the question-answer pairs: "
                   f"What specific customer problem does your product or service solve, and how does it differentiate from competitors? {q1};"
                   f"Who are your primary target customers, and what are their key characteristics and needs that your offering addresses? {q2};"
                   f"Which primary channel will you use to reach your target customers, are there any alternatives and why is this the most effective method? {q3};"
                   f"What type of relationship will you establish with your customers, and what strategies will you use to maintain and enhance these relationships? {q4};"
                   f"What is your main revenue model, and why is it appropriate for your target market and value proposition? {q5};"
                   f"Identify the essential resources needed to deliver your value proposition. How do you plan to secure and manage these resources? {q6};"
                   f"Who are your indispensable partners or suppliers, what will they provide, and how are these partnerships structured to support your business objectives? {q7};"
                   f"What are the critical activities necessary to support your business model? How do you plan to excel at these activities? {q8};"
                   f"What are your significant expected costs, and how do you plan to manage efficiency while maintaining quality? {q9}.")
        task_id = str(uuid.uuid4())
        tasks[task_id] = {}
        session['task_id'] = task_id
        session['start_time'] = time.time()
        session['message'] = message
        Thread(target=generate_answer, args=(message,task_id)).start()
        return redirect(url_for('loading'))

    return render_template('question.html')


if __name__ == '__main__':
    app.run()
