"""
    Flask Web scrapping App with REST Api
"""

__author__ = "mikazz"

# Basic
import datetime
import uuid
import threading
import zipfile
import io
import pathlib
from urllib.parse import urlparse

from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import send_file

from utils import SavePage

HOST = "127.0.0.1"
PORT = 5000

app = Flask(__name__)

workers = []  # list of threads (Task)

@app.errorhandler(404)
def not_found(error):
    """Much more API friendly error response:"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/sorcer/api/tasks', methods=['GET'])
def get_tasks():
    """Get details about all tasks"""
    return jsonify({'tasks': make_workers_dict(workers)})


@app.route('/scrapper/api/tasks/<string:task_id>', methods=['GET'])
def get_task(task_id):
    """Get details about single task"""
    task = [task for task in make_workers_dict(workers) if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


@app.route('/scrapper/api/tasks/<string:task_id>/download', methods=['GET'])
def get_task_download(task_id):
    """Download task (zip directory with results)"""
    if task_id not in [w.id for w in workers]:
        abort(404)

    for w in workers:
        if str(w.id) == str(task_id):
            task = w

    if task.is_alive():  # you can't download active task
        abort(404)

    base_path = pathlib.Path(task.directory_name)
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        for f_name in base_path.iterdir():
            z.write(f_name)
    data.seek(0)
    return send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename=f'{task.directory_name}.zip'
    )


@app.route('/scrapper/api/tasks', methods=['POST'])
def create_task():
    """POST method, which we will use to insert a new item in our task list"""
    if not request.json or 'page' not in request.json:
        abort(400)

    task_name = request.json['page']

    if request.json['tag'] == "get_text":
        param = "get_text"
    elif request.json['tag'] == "get_images":
        param = "get_images"
    else:
        param = None

    new_task = Task(page_url=task_name, param=param)
    new_task.start()
    workers.append(new_task)
    return jsonify({'task_id': str(new_task.id),
                    "page": new_task.page_url,
                    'download_page': f"{HOST}:{PORT}/scrapper/api/tasks/{new_task.id}/download"
                    })


if __name__ == '__main__':
    print("\n", f"http://{HOST}:{PORT}/scrapper/api/tasks", "\n")
    app.run(host=HOST, port=PORT, debug=True)