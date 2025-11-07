from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Book, Loan

User = get_user_model()


class LoanModelTests(TestCase):
    """Testes para o modelo Loan."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.book = Book.objects.create(
            title='Livro Teste',
            author='Autor Teste',
            isbn='1234567890123',
            copies_total=1
        )

    def test_overdue_logic(self):
        """Testa se empréstimo atrasado é detectado corretamente."""
        # Criar inicialmente com due_date futuro para satisfazer a constraint
        past_borrowed = timezone.now() - timedelta(days=2)
        desired_due = timezone.localdate() - timedelta(days=1)

        temp_due = timezone.localdate() + timedelta(days=2)
        loan = Loan.objects.create(
            book=self.book,
            user=self.user,
            due_date=temp_due,
        )

        # Atualiza diretamente no banco para definir borrowed_at no passado e due_date no passado
        Loan.objects.filter(pk=loan.pk).update(borrowed_at=past_borrowed, due_date=desired_due)
        loan.refresh_from_db()

        self.assertTrue(loan.is_overdue)
        self.assertTrue(loan.is_active)

    def test_mark_returned_sets_timestamp(self):
        loan = Loan.objects.create(
            book=self.book,
            user=self.user,
            due_date=timezone.localdate() + timedelta(days=7)
        )
        
        self.assertIsNone(loan.returned_at)
        loan.mark_returned()
        self.assertIsNotNone(loan.returned_at)
        self.assertFalse(loan.is_active)

    def test_copies_available_counts_active_loans(self):
        self.assertEqual(self.book.copies_available, 1)
        
        Loan.objects.create(
            book=self.book,
            user=self.user,
            due_date=timezone.localdate() + timedelta(days=7)
        )
        
        self.assertEqual(self.book.copies_available, 0)


class AuthViewsTests(TestCase):

    def test_logout_requires_post_and_redirects(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 405)
