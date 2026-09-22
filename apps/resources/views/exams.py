from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from ..models import Exam, ExamAnswer, ExamAttempt, ExamQuestion, Question, Topic, Subtopic, SubSubtopic


@login_required
def question_bank_view(request):
    questions = Question.objects.filter(created_by=request.user).select_related(
        'topic', 'subtopic', 'subsubtopic',
    )
    return render(request, 'exams/question_bank.html', {'questions': questions})


@login_required
def question_create_view(request):
    topics = Topic.objects.all()

    if request.method == 'POST':
        question = Question(
            created_by=request.user,
            question_type=request.POST.get('question_type', 'mcq'),
            text=request.POST.get('text', '').strip(),
            choice_a=request.POST.get('choice_a', '').strip(),
            choice_b=request.POST.get('choice_b', '').strip(),
            choice_c=request.POST.get('choice_c', '').strip(),
            choice_d=request.POST.get('choice_d', '').strip(),
            correct_choice=request.POST.get('correct_choice', ''),
            correct_answer_text=request.POST.get('correct_answer_text', '').strip(),
            marks=int(request.POST.get('marks') or 1),
            topic_id=request.POST.get('topic') or None,
            subtopic_id=request.POST.get('subtopic') or None,
            subsubtopic_id=request.POST.get('subsubtopic') or None,
        )
        try:
            question.full_clean()
        except ValidationError as e:
            return render(request, 'exams/question_create.html', {
                'topics': topics, 'errors': e.messages, 'posted': request.POST,
            })
        question.save()
        return redirect('question_bank')

    return render(request, 'exams/question_create.html', {'topics': topics})


@login_required
def exam_list_view(request):
    exams = Exam.objects.filter(created_by=request.user)
    return render(request, 'exams/exam_list.html', {'exams': exams})


@login_required
def exam_create_view(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if title:
            exam = Exam.objects.create(title=title, created_by=request.user)
            return redirect('exam_detail', pk=exam.pk)
    return render(request, 'exams/exam_create.html')


@login_required
def exam_detail_view(request, pk):
    exam = get_object_or_404(Exam, pk=pk, created_by=request.user)
    own_questions = Question.objects.filter(created_by=request.user).exclude(
        id__in=exam.questions.values_list('id', flat=True)
    )

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_question':
            question_id = request.POST.get('question_id')
            next_order = exam.examquestion_set.count() + 1
            ExamQuestion.objects.get_or_create(
                exam=exam, question_id=question_id, defaults={'order': next_order},
            )
        elif action == 'remove_question':
            question_id = request.POST.get('question_id')
            ExamQuestion.objects.filter(exam=exam, question_id=question_id).delete()
        elif action == 'publish':
            exam.is_published = True
            exam.save(update_fields=['is_published'])
        return redirect('exam_detail', pk=exam.pk)

    exam_questions = exam.examquestion_set.select_related('question').all()
    attempts = exam.attempts.all()

    return render(request, 'exams/exam_detail.html', {
        'exam': exam,
        'exam_questions': exam_questions,
        'own_questions': own_questions,
        'attempts': attempts,
        'total_marks': exam.total_marks(),
    })


def exam_take_view(request, access_code):
    exam = get_object_or_404(Exam, access_code=access_code, is_published=True)
    exam_questions = exam.examquestion_set.select_related('question').all()
    return render(request, 'exams/exam_take.html', {
        'exam': exam,
        'exam_questions': exam_questions,
    })


def exam_submit_view(request, access_code):
    exam = get_object_or_404(Exam, access_code=access_code, is_published=True)

    if request.method != 'POST':
        return redirect('exam_take', access_code=access_code)

    student_name = request.POST.get('student_name', '').strip() or 'Аноним'
    attempt = ExamAttempt.objects.create(exam=exam, student_name=student_name)

    score = 0
    for exam_question in exam.examquestion_set.select_related('question'):
        question = exam_question.question
        field_name = f'question_{question.id}'

        if question.question_type == 'mcq':
            selected = request.POST.get(field_name, '')
            is_correct = bool(selected) and selected == question.correct_choice
            if is_correct:
                score += question.marks
            ExamAnswer.objects.create(
                attempt=attempt, question=question,
                selected_choice=selected, is_correct=is_correct,
            )
        else:
            answer_text = request.POST.get(field_name, '').strip()
            ExamAnswer.objects.create(
                attempt=attempt, question=question,
                answer_text=answer_text, is_correct=None,
            )

    attempt.score = score
    attempt.submitted_at = timezone.now()
    attempt.save(update_fields=['score', 'submitted_at'])

    return redirect('exam_result', access_code=access_code, attempt_id=attempt.pk)


def exam_result_view(request, access_code, attempt_id):
    exam = get_object_or_404(Exam, access_code=access_code)
    attempt = get_object_or_404(ExamAttempt, pk=attempt_id, exam=exam)
    return render(request, 'exams/exam_result.html', {
        'exam': exam,
        'attempt': attempt,
        'total_marks': exam.total_marks(),
    })
