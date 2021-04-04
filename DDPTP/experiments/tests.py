from django.test import TestCase
from django.test import Client
from .models import Adult_original, Adult_test, Statlog

class Database_test(TestCase):
    def setUp(self):
        Adult_original.objects.create(age=20, workclass="Private", fnlwgt=12345, education="Bachelors", education_num=10, marital_status="Divorced", 
                                      occupation="Tech-support", relationship="Wife", race="White", sex="Female", capital_gain=10000, capital_loss=2345,
                                      hours_per_week=40, native_country="United-States")
        Adult_original.objects.create(age=25, workclass="Private", fnlwgt=12233, education="Bachelors", education_num=10, marital_status="Divorced", 
                                      occupation="Tech-support", relationship="Wife", race="White", sex="Female", capital_gain=10000, capital_loss=2345,
                                      hours_per_week=40, native_country="United-States")
        Adult_test.objects.create(age=30, workclass="Private", fnlwgt=23456, education="Doctorate", education_num=15, marital_status="Married-civ-spouse", 
                                  occupation="Sales", relationship="Husband", race="White", sex="Male", capital_gain=9000, capital_loss=3456,
                                  hours_per_week=28, native_country="United-States")
        Statlog.objects.create(account_status="A11", duration=20, credit_history="A31", purpose="A41", credit_amount=1000, savings_account="A61", 
                               present_employment_since="A71", installment_rate_in_income=40, personal_status_and_sex="A91", guarantors="A101",
                               present_residence_since=10, property="A121", age=31, other_installment_plans="A141", housing="A151", existing_credits=12345,
                               job="A171", maintenance_provider_number=2, telephone="A192", foreign_worker="A201", result=2)

    def test_get_objects(self):
        adult_original_objects = Adult_original.objects.values_list()
        self.assertEqual(len(adult_original_objects), 2)
        adult_test_object = Adult_original.objects.first()
        self.assertEqual(adult_test_object.native_country, "United-States")
        Statlog_object = Statlog.objects.first()
        self.assertEqual(Statlog_object.result, 2)

class Experiment_page_test(TestCase):
    def test_url(self):
        c = Client()
        response = c.get('/experiments/')
        self.assertEqual(response.status_code, 200)

    def test_run_experiments(self):
        c = Client()
        e2_t2_c1_response = c.post('/experiments/run', {'action': 'run_e2_t2_c1'})
        self.assertEqual(e2_t2_c1_response.status_code, 200)
        e2_t2_c2_response = c.post('/experiments/run', {'action': 'run_e2_t2_c2'})
        self.assertEqual(e2_t2_c2_response.status_code, 200)
        e2_t2_customize_response = c.post('/experiments/run', {'action': 'run_e2_t2_customize', 'epsilon': 2})
        self.assertEqual(e2_t2_customize_response.status_code, 200)
