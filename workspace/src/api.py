from flask import Flask, request, jsonify, Response
from typing import Union
from workspace.src.celery_app import celery
from workspace.src.utils import initialize_client
from workspace.src.tasks import (
    detect_anomalies_task,
    extract_ordonnance_task,
    summarize_ordonnances_task,
    search_articles_task,
    generate_search_summary_task,
    generate_report_task,
)

app = Flask(__name__)
client = initialize_client()

@app.route("/task/<task_id>", methods=["GET"])
def get_task_status(task_id: str) -> Union[Response, tuple[Response, int]]:
    """Get the status of a task by its ID."""
    task = celery.AsyncResult(task_id)
    if task.ready():
        if task.successful():
            return jsonify({
                "status": "completed",
                "result": task.get()
            })
        return jsonify({
            "status": "failed",
            "error": str(task.result)
        }), 500
    return jsonify({
        "status": "processing",
        "task_id": task_id
    })

@app.route("/hello", methods=["GET"])
def hello() -> Response:
    return jsonify({"message": "Hello World!"})

@app.route("/detect-prescription-anomalies", methods=["POST"])
def detect_anomalies() -> Union[Response, tuple[Response, int]]:
    data = request.get_json()
    if (
        not data
        or "doctor_prescription" not in data
        or "patient_medication_history" not in data
    ):
        return jsonify({"error": "Missing required fields"}), 400

    task = detect_anomalies_task.delay(
        data["doctor_prescription"],
        data["patient_medication_history"]
    )
    return jsonify({
        "status": "processing",
        "task_id": task.id
    }), 202

@app.route("/extract-ordonnance", methods=["POST"])
def extract_ordonnance() -> Union[Response, tuple[Response, int]]:
    data = request.get_json()
    if not data or "doctor_prescription" not in data:
        return jsonify({"error": "Missing doctor_prescription"}), 400

    task = extract_ordonnance_task.delay(
        data["doctor_prescription"]
    )
    return jsonify({
        "status": "processing",
        "task_id": task.id
    }), 202

@app.route("/summarize-ordonnances", methods=["POST"])
def summarize() -> Union[Response, tuple[Response, int]]:
    data = request.get_json()
    if not data or "doctor_prescriptions" not in data:
        return jsonify({"error": "Missing doctor_prescriptions"}), 400

    task = summarize_ordonnances_task.delay(
        data["doctor_prescriptions"]
    )
    return jsonify({
        "status": "processing",
        "task_id": task.id
    }), 202

@app.route("/search-medical-articles", methods=["GET"])
def search_articles() -> Union[Response, tuple[Response, int]]:
    query = request.args.get("query")
    retmax = request.args.get("retmax", default=5, type=int)
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400

    task = search_articles_task.delay(query, retmax)
    return jsonify({
        "status": "processing",
        "task_id": task.id
    }), 202

@app.route("/generate-search-summary", methods=["POST"])
def search_summary() -> Union[Response, tuple[Response, int]]:
    data = request.get_json()
    if not data or "patient_condition" not in data or "medical_articles" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    task = generate_search_summary_task.delay(
        data["patient_condition"],
        data["medical_articles"]
    )
    return jsonify({
        "status": "processing",
        "task_id": task.id
    }), 202

@app.route("/generate-report", methods=["POST"])
def generate_medical_report() -> Union[Response, tuple[Response, int]]:
    data = request.get_json()
    required_fields = [
        "conversation",
        "patient_information",
        "medical_history",
        "additional_notes",
        "additional_medical_information",
    ]

    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    task = generate_report_task.delay(
        data["conversation"],
        data["patient_information"],
        data["medical_history"],
        data["additional_notes"],
        data["additional_medical_information"]
    )
    return jsonify({
        "status": "processing",
        "task_id": task.id
    }), 202

if __name__ == "__main__":
    app.run(debug=True, port=5000)
