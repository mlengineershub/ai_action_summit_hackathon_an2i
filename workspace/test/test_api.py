import unittest
from typing import Any
import json
from flask.testing import FlaskClient
from workspace.src.api import app

class TestAPI(unittest.TestCase):
    app_client: FlaskClient

    def setUp(self) -> None:
        self.app_client = app.test_client()

    def test_hello_endpoint(self) -> None:
        response = self.app_client.get('/hello')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Hello World!')

    def test_detect_prescription_anomalies_missing_data(self) -> None:
        response = self.app_client.post('/detect-prescription-anomalies', 
                               json={})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_extract_ordonnance_missing_data(self) -> None:
        response = self.app_client.post('/extract-ordonnance', 
                               json={})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_search_medical_articles_missing_query(self) -> None:
        response = self.app_client.get('/search-medical-articles')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_fetch_article_abstract_missing_pmid(self) -> None:
        response = self.app_client.get('/fetch-article-abstract/')
        self.assertEqual(response.status_code, 404)

    def test_generate_search_summary_missing_data(self) -> None:
        response = self.app_client.post('/generate-search-summary',
                               json={})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_generate_follow_up_questions_missing_data(self) -> None:
        response = self.app_client.post('/generate-follow-up-questions',
                               json={})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_extract_pertinent_points_missing_data(self) -> None:
        response = self.app_client.post('/extract-pertinent-points',
                               json={})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_generate_search_propositions_missing_data(self) -> None:
        response = self.app_client.post('/generate-search-propositions',
                               json={})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_generate_report_missing_data(self) -> None:
        response = self.app_client.post('/generate-report',
                               json={})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()