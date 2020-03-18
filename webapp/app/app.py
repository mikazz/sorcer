__author__ = "mikazz"
__version__ = "1.0"

from rq import Queue, Connection
from flask import Flask, request, jsonify, abort, send_file
from redis import Redis
from redis import Connection as BasicConnection
from webapp.app.jobs import get_text_job, get_images_job, url_to_page_name, long_job

import zipfile
import io
import pathlib
import rq_dashboard

app = Flask(__name__)

# RQ Dashboard configuration
app.config.from_object(rq_dashboard.default_settings)
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")

HOST = "127.0.0.1"
PORT = 5000
DEBUG = True


@app.route('/')
def home():
    """
        Home
    """
    try:
        basic_connection = BasicConnection()
        basic_connection.connect()

    except Exception as e:
        response_object = {"status": "failed",
                           "data": {
                               "connection": "failed",
                               "details": str(e)
                           }
                           }
    else:
        response_object = {"status": "success",
                           "data": {
                               "connection": "ok",
                           }
                           }

    return jsonify(response_object)


@app.route('/job', methods=['POST'])
def run_job():
    """
        curl -X POST -F "page_url=https://www.google.com/" -F "function=get_text" http://127.0.0.1:5000/job
    """

    page_url = str(request.form['page_url'])
    function_name = str(request.form['function'])

    if function_name == "get_text":
        job_func_name = get_text_job

    elif function_name == "get_images":
        job_func_name = get_images_job
    else:
        abort(400)

    with Connection(connection=Redis()):
        q = Queue()
        job = q.enqueue(job_func_name, page_url=page_url, job_timeout=60)

    response_object = {
        'status': 'success',
        'data': {
            'job_id': job.get_id(),
            'job_func_name': job.func_name,
            'job_args': job.args,
            'job_kwargs': job.kwargs,
            'job_status_url': f"http://{HOST}:{PORT}/jobs/{job.get_id()}",
            'job_download_url': f"http://{HOST}:{PORT}/jobs/{job.get_id()}/download",
            'job_is_queued': job.is_queued,
            'job_enqueued_at': job.enqueued_at,
        }
    }
    return jsonify(response_object), 202  # ACCEPTED


@app.route('/jobs/<job_id>', methods=['GET'])
def get_job(job_id):
    """
        Get single job status
        curl -X GET http://localhost:5000/jobs/7758ecb7-59db-40b0-8336-8a38e087e5b6
    """
    with Connection(connection=Redis()):
        q = Queue()
        job = q.fetch_job(job_id)
    if job:
        response_object = {
            'data': {
                'job_id': job.get_id(),
                'job_status': job.get_status(),
                'job_result': job.result,
                'job_is_started': job.is_started,
                'job_started_at': job.started_at,
                'job_is_queued': job.is_queued,
                'job_timeout': job.timeout,
                'job_enqueued_at': job.enqueued_at,
                'job_ended_at': job.ended_at,
                'job_exc_info': job.exc_info,
                'job_dependent_ids': job.dependent_ids,
                'job_meta': job.meta,
                'job_status_url': f"http://{HOST}:{PORT}/jobs/{job.get_id()}",
                'job_download_url': f"http://{HOST}:{PORT}/jobs/{job.get_id()}/download",
                'job_func_name': job.func_name,
                'job_args': job.args,
                'job_kwargs': job.kwargs,
            }
        }

        if job.is_failed:
            response_object = {
                'status': 'failed',
                'data': {
                    'job_id': job.get_id(),
                    'job_status': job.get_status(),
                    'job_result': job.result,
                    'message': job.exc_info.strip().split('\n')[-1]
                }
             }
    else:
        response_object = {
            'status': 'ERROR: Unable to fetch the job from RQ'
        }
    return jsonify(response_object)


@app.route('/jobs/<job_id>/download', methods=['GET'])
def get_job_download(job_id):

    with Connection(connection=Redis()):
        q = Queue()
        job = q.fetch_job(job_id)

    if not job.get_status() == "finished":
        abort(404)

    directory_name = job.kwargs.get("page_url")
    directory_name = url_to_page_name(directory_name)

    # if dir there is none so what?

    base_path = pathlib.Path(directory_name)
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        for f_name in base_path.iterdir():
            z.write(f_name)
    data.seek(0)
    return send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename=f'{directory_name}.zip'
    )


@app.route('/jobs', methods=['GET'])
def get_jobs():
    """
        curl -X GET http://localhost:5000/jobs
    """
    with Connection(connection=Redis()):
        q = Queue()
        jobs = q.get_jobs()

    if jobs:
        response_object = {
            'status': 'success',
            'in_queue_jobs_number': str(len(q)),
            'jobs': str(jobs)
        }

    else:
        response_object = {
            'status': 'success',
            'queue_size': f'{len(q)}'
        }
    return jsonify(response_object)


@app.route('/long_job', methods=['POST'])
def run_long_job():
    """
        curl -X POST -F "duration=3" http://127.0.0.1:5000/long_job
    """

    job_duration = int(request.form['duration'])
    with Connection(connection=Redis()):
        q = Queue()
        job = q.enqueue(long_job, job_duration, job_timeout=60)

    response_object = {
        'data': {
            'job_id': job.get_id(),
            'job_status': job.get_status(),
            'job_result': job.result,
            'job_timeout': job.timeout,
            'job_is_started': job.is_started,
            'job_started_at': job.started_at,
            'job_is_queued': job.is_queued,
            'job_enqueued_at': job.enqueued_at,
            'job_ended_at': job.ended_at,
            'job_page_url': f"http://{HOST}:{PORT}/jobs/{job.get_id()}",
        }
    }
    return jsonify(response_object), 202


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
