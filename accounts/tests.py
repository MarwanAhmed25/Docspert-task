from django.test import TestCase
from django.urls import reverse
from .models import Account, Transaction
from .forms import TransactionForm

class TransactionCreateViewTests(TestCase):
    def setUp(self):
        # Create test accounts
        self.sender = Account.objects.create(name="Sender", balance=100)
        self.receiver = Account.objects.create(name="Receiver", balance=200)

    def test_valid_transaction(self):
        form_data = {
            'sender': self.sender.id,
            'receiver': self.receiver.id,
            'amount': 50,
        }
        response = self.client.post(reverse('accounts:transaction_create', args=[self.sender.id]), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful transaction
        self.sender.refresh_from_db()
        self.receiver.refresh_from_db()
        self.assertEqual(self.sender.balance, 50)
        self.assertEqual(self.receiver.balance, 250)

    def test_invalid_transaction(self):
        form_data = {
            'sender': self.sender.id,
            'receiver': self.receiver.id,
            'amount': 200,
        }
        response = self.client.post(reverse('accounts:transaction_create', args=[self.sender.id]), data=form_data)
        self.assertEqual(response.status_code, 302)  # Form validation failed
        self.assertEqual(response.url, '/' + str(self.sender.id) + '/transactions/create')  # after failed it will redirect to create page


class AccountCreateViewTest(TestCase):
    def test_successful_form_submission(self):
        # Simulate a valid form submission
        response = self.client.post(reverse('accounts:account_create'), data={'name': 'Test Account'})
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse('accounts:account_list'))
        self.assertEqual(Account.objects.count(), 1)  # Verify account creation

    def test_invalid_form_submission(self):
        # Simulate an invalid form submission
        response = self.client.post(reverse('accounts:account_create'), data={})
        self.assertEqual(response.status_code, 200)  # Form not valid
        self.assertTemplateUsed(response, 'accounts/create_account.html')
        self.assertIn('form', response.context)

    def test_get_request(self):
        # Test GET request to the view
        response = self.client.get(reverse('accounts:account_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/create_account.html')
        self.assertIn('form', response.context)


