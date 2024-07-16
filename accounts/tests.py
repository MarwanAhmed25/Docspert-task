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


class AccountDetailViewTest(TestCase):
    def setUp(self):
        # Create test data (adjust as needed)
        self.sender = Account.objects.create(name='sender Account', balance=200)
        self.receiver = Account.objects.create(name='receiver Account', balance=200)
        self.transaction1 = Transaction.objects.create(sender=self.sender, receiver=self.receiver, amount=100)
        self.transaction2 = Transaction.objects.create(receiver=self.sender, sender=self.receiver, amount=50)

    def test_account_detail_with_search_query(self):
        response = self.client.get(reverse('accounts:account_detail', args=[self.sender.pk]), {'search': 'receiver'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/detail.html')
        self.assertIn('account', response.context)
        self.assertIn('transactions', response.context)

    def test_account_detail_without_search_query(self):
        response = self.client.get(reverse('accounts:account_detail', args=[self.sender.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/detail.html')
        self.assertIn('account', response.context)
        self.assertIn('transactions', response.context)


class AccountListViewTest(TestCase):
    def test_account_list_with_search_query(self):
        # Create test accounts (adjust as needed)
        Account.objects.create(name='Test Account 1')
        Account.objects.create(name='Another Test Account')

        response = self.client.get(reverse('accounts:account_list'), {'search': 'Another'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['accounts']), 1)
        self.assertTemplateUsed(response, 'accounts/list.html')
        self.assertIn('accounts', response.context)


    def test_account_list_without_search_query(self):
        # Create test accounts (adjust as needed)
        Account.objects.create(name='Test Account 1')
        Account.objects.create(name='Another Test Account')

        response = self.client.get(reverse('accounts:account_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/list.html')
        self.assertIn('accounts', response.context)
        self.assertEqual(len(response.context['accounts']), 2)


    def test_rendering_template(self):
        response = self.client.get(reverse('accounts:account_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/list.html')
        self.assertIn('accounts', response.context)
        self.assertIn('form', response.context)



