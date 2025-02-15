from flask import Flask, request, jsonify, Response
from openai import OpenAI
from typing import Union, Any
from workspace.src.utils import initialize_client
from workspace.src.detect_prescription_anomalies import detect_prescription_anomalies
from workspace.src.extract_ordonnance_data import extract_ordonnance_data, summarize_ordonnances
from workspace.src.gather_medical_knowledge_tool import search_medical_articles, fetch_article_abstract, generate_search_summary
from workspace.src.generate_follow_up_questions import generate_follow_up_questions
from workspace.src.generate_pertinent_points import extract_pertinent_medical_points
from workspace.src.hello import hello_function
from workspace.src.propose_medical_queries import generate_search_propositions
from workspace.src.report_generation import generate_report
from workspace.src.utils import generate_prompt
from workspace.src.prompts import (
    detect_medical_prescription_anomaly_prompt_template,
    extract_ordonnance_data_prompt_template,
    summarize_ordonnances_prompt_template,
    follow_up_questions_prompt_template,
    extract_medical_points_prompt_template,
    search_proposition_prompt_template,
    report_generation_template,
    summarize_search_prompt_template,
)

app = Flask(__name__)
client = initialize_client()

@app.route('/hello', methods=['GET'])
def hello() -> Response:
    hello_function()
    return jsonify({"message": "Hello World!"})

@app.route('/detect-prescription-anomalies', methods=['POST'])
def detect_anomalies() -> Union[Response, tuple[Response, int]]:
    data = request.get_json()
    if not data or 'doctor_prescription' not in data or 'patient_medication_history' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    prompt = generate_prompt(
        detect_medical_prescription_anomaly_prompt_template,
        doctor_prescription=data['doctor_prescription'],
        patient_medication_history=data['patient_medication_history']
    )
    response = detect_prescription_anomalies(client, prompt)
    return jsonify(response)

@app.route('/extract-ordonnance', methods=['POST'])
def extract_ordonnance() -> Union[Response, tuple[Response, int]]:
    data = request.get_json()
    if not data or 'doctor_prescription' not in data:
        return jsonify({"error": "Missing doctor_prescription"}), 400
    
    prompt = generate_prompt(
        extract_ordonnance_data_prompt_template,
        doctor_prescription=data['doctor_prescription']
    )
    response = extract_ordonnance_data(client, prompt)
    return jsonify({"extracted_data": response})

@app.route('/summarize-ordonnances', methods=['POST'])
def summarize() -> Union[Response, tuple[Response, int]]:
    data = request.get_json()
    if not data or 'doctor_prescriptions' not in data:
        return jsonify({"error": "Missing doctor_prescriptions"}), 400
    
    prompt = generate_prompt(
        summarize_ordonnances_prompt_template,
        doctor_prescriptions=data['doctor_prescriptions']
    )
    response = summarize_ordonnances(client, prompt)
    return jsonify({"summary": response})

@app.route('/search-medical-articles', methods=['GET'])
def search_articles() -> Union[Response, tuple[Response, int]]:
    query = request.args.get('query')
    retmax = request.args.get('retmax', default=5, type=int)
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400
    
    response = search_medical_articles(query, retmax)
    return jsonify(response)

@app.route('/fetch-article-abstract/<pmid>', methods=['GET'])
def get_article_abstract(pmid: str) -> Union[Response, tuple[Response, int]]:
    if not pmid:
        return jsonify({"error": "Missing PMID"}), 400
    
    abstract = fetch_article_abstract(pmid)
    return jsonify({"abstract": abstract})

@app.route('/generate-search-summary', methods=['POST'])
def search_summary() -> Union[Response, tuple[Response, int]]:
    data = request.get_json()
    if not data or 'patient_condition' not in data or 'medical_articles' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    prompt = generate_prompt(
        summarize_search_prompt_template,
        patient_condition=data['patient_condition'],
        medical_articles=data['medical_articles']
    )
    response = generate_search_summary(client, prompt)
    return jsonify(response)

@app.route('/generate-follow-up-questions', methods=['POST'])
def follow_up_questions() -> Union[Response, tuple[Response, int]]:
    data = request.get_json()
    if not data or 'conversation' not in data:
        return jsonify({"error": "Missing conversation"}), 400
    
    prompt = generate_prompt(
        follow_up_questions_prompt_template,
        conversation=data['conversation']
    )
    response = generate_follow_up_questions(client, prompt)
    return jsonify(response)

@app.route('/extract-pertinent-points', methods=['POST'])
def pertinent_points() -> Union[Response, tuple[Response, int]]:
    data = request.get_json()
    if not data or 'conversation' not in data or 'previous_medical_history' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    prompt = generate_prompt(
        extract_medical_points_prompt_template,
        conversation=data['conversation'],
        previous_medical_history=data['previous_medical_history']
    )
    response = extract_pertinent_medical_points(client, prompt)
    return jsonify(response)

@app.route('/generate-search-propositions', methods=['POST'])
def search_propositions() -> Union[Response, tuple[Response, int]]:
    data = request.get_json()
    if not data or 'conversation' not in data or 'search_history' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    prompt = generate_prompt(
        search_proposition_prompt_template,
        conversation=data['conversation'],
        search_history=data['search_history']
    )
    response = generate_search_propositions(client, prompt)
    return jsonify(response)

@app.route('/generate-report', methods=['POST'])
def generate_medical_report() -> Union[Response, tuple[Response, int]]:
    data = request.get_json()
    required_fields = [
        'conversation',
        'patient_information',
        'medical_history',
        'additional_notes',
        'additional_medical_information'
    ]
    
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    prompt = generate_prompt(
        report_generation_template,
        conversation=data['conversation'],
        patient_information=data['patient_information'],
        medical_history=data['medical_history'],
        additional_notes=data['additional_notes'],
        additional_medical_information=data['additional_medical_information']
    )
    response = generate_report(client, prompt)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)