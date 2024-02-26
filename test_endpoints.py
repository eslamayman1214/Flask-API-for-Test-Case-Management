import unittest
from app import app

class TestEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_create_test_case(self):
        data = {'name': 'Test Case 1', 'description': 'Description for Test Case 1'}
        response = self.app.post('/testcases', json=data)
        self.assertEqual(response.status_code, 201)

    def test_get_all_test_cases(self):
        response = self.app.get('/testcases')
        self.assertEqual(response.status_code, 200)

    def test_get_test_case_by_id(self):
        response = self.app.get('/testcases/1')
        self.assertEqual(response.status_code, 200)

    def test_update_test_case(self):
        data = {'name': 'Updated Test Case 1', 'description': 'Updated description for Test Case 1'}
        response = self.app.put('/testcases/1', json=data)
        self.assertEqual(response.status_code, 200)

    def test_delete_test_case(self):
        response = self.app.delete('/testcases/1')
        self.assertEqual(response.status_code, 200)

    def test_record_execution_result(self):
        data = {'test_case_id': 1, 'test_asset': 'Asset 1', 'result': 'Pass'}
        response = self.app.post('/executionresults', json=data)
        self.assertEqual(response.status_code, 201)

    def test_get_execution_results_by_test_asset(self):
        response = self.app.get('/executionresults/Asset 1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()