from django.test import TestCase
from django.urls import reverse

from apps.account.models import Account

from .models import Exam, ExamQuestion, Question


class ExamFlowTests(TestCase):
    def setUp(self):
        self.teacher = Account.objects.create_user(
            email='teacher@example.com', username='teacher', password='SuperSecret123!'
        )
        self.teacher.is_active = True
        self.teacher.save(update_fields=['is_active'])
        self.client.login(email='teacher@example.com', password='SuperSecret123!')

        self.mcq = Question.objects.create(
            created_by=self.teacher,
            question_type='mcq',
            text='2 + 2 канча?',
            choice_a='3', choice_b='4', choice_c='5', choice_d='6',
            correct_choice='b',
            marks=2,
        )
        self.exam = Exam.objects.create(title='Сынак тест', created_by=self.teacher)
        ExamQuestion.objects.create(exam=self.exam, question=self.mcq, order=1)
        self.exam.is_published = True
        self.exam.save(update_fields=['is_published'])

    def test_question_requires_correct_choice_for_mcq(self):
        bad = Question(
            created_by=self.teacher, question_type='mcq', text='Жооп жок суроо',
            choice_a='1', choice_b='2',
        )
        with self.assertRaises(Exception):
            bad.full_clean()

    def test_unpublished_exam_is_not_takeable(self):
        self.exam.is_published = False
        self.exam.save(update_fields=['is_published'])
        resp = self.client.get(reverse('exam_take', args=[self.exam.access_code]))
        self.assertEqual(resp.status_code, 404)

    def test_published_exam_take_page_loads(self):
        resp = self.client.get(reverse('exam_take', args=[self.exam.access_code]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '2 + 2 канча?')

    def test_correct_answer_scores_full_marks(self):
        resp = self.client.post(reverse('exam_submit', args=[self.exam.access_code]), {
            'student_name': 'Айгерим',
            f'question_{self.mcq.id}': 'b',
        })
        attempt = self.exam.attempts.get(student_name='Айгерим')
        self.assertEqual(attempt.score, 2)
        self.assertRedirects(resp, reverse('exam_result', args=[self.exam.access_code, attempt.pk]))

    def test_wrong_answer_scores_zero(self):
        self.client.post(reverse('exam_submit', args=[self.exam.access_code]), {
            'student_name': 'Нурбек',
            f'question_{self.mcq.id}': 'a',
        })
        attempt = self.exam.attempts.get(student_name='Нурбек')
        self.assertEqual(attempt.score, 0)

    def test_teacher_can_create_exam_and_add_question(self):
        resp = self.client.post(reverse('exam_create'), {'title': 'Экинчи тест'})
        new_exam = Exam.objects.get(title='Экинчи тест')
        self.assertRedirects(resp, reverse('exam_detail', args=[new_exam.pk]))

        self.client.post(reverse('exam_detail', args=[new_exam.pk]), {
            'action': 'add_question', 'question_id': self.mcq.id,
        })
        self.assertTrue(
            ExamQuestion.objects.filter(exam=new_exam, question=self.mcq).exists()
        )

    def test_exam_detail_is_only_visible_to_its_owner(self):
        other = Account.objects.create_user(
            email='other@example.com', username='other', password='SuperSecret123!'
        )
        other.is_active = True
        other.save(update_fields=['is_active'])
        self.client.logout()
        self.client.login(email='other@example.com', password='SuperSecret123!')

        resp = self.client.get(reverse('exam_detail', args=[self.exam.pk]))
        self.assertEqual(resp.status_code, 404)
