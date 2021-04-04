from django.test import TestCase
from django.test import Client
from .forms import Statlog_submission_form

class Pages_test(TestCase):
    def test_url(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        response = c.get('/demo/index')
        self.assertEqual(response.status_code, 200)
        response = c.get('/demo/contract')
        self.assertEqual(response.status_code, 200)
        response = c.get('/demo/statlog_contract')
        self.assertEqual(response.status_code, 200)
        response = c.get('/demo/submission')
        self.assertEqual(response.status_code, 200)
        response = c.get('/demo/api')
        self.assertEqual(response.status_code, 200)
        response = c.get('/demo/verification')
        self.assertEqual(response.status_code, 200)


class Form_test(TestCase):
    def test_submission_form_invalid_data(self):
        form = Statlog_submission_form(data={
            'account_status': "A11",
            'duration': 11,
            'credit_history': "A31",
            'purpose': "A41",
            'credit_amount': "1000",
            'savings_account': "A61",
            'present_employment_since': "A71",
            'installment_rate_in_income': 20,
            'personal_status_and_sex': "A91",
            'guarantors': "A101",
            'present_residence_since': 15,
            'property': "A121",
            'age': 25
        })
        self.assertFalse(form.is_valid())

class API_test(TestCase):
    def test_api_valid_query(self):
        c = Client()
        response = c.get('/demo/api/result?query=SELECT+AVG%28age%29+FROM+experiments_statlog')
        self.assertEqual(response.status_code, 200)
    
    def test_api_invalid_query(self):
        c = Client()
        response = c.get('/demo/api/result?query=SELECT+AVG%28age%29+FROM+experiments')
        self.assertEqual(response.content, b'"Invalid query! Please refer to the rules of making queries."')