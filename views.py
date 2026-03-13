from django.shortcuts import render, get_object_or_404
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

def submit(request, exam_id):
    course = get_object_or_404(Course, pk=exam_id)

    selected_choices = request.POST.getlist('choice')

    enrollment = Enrollment.objects.first()

    submission = Submission.objects.create(enrollment=enrollment)

    for choice_id in selected_choices:
        choice = Choice.objects.get(id=choice_id)
        submission.choices.add(choice)

    return show_exam_result(request, submission.id)


def show_exam_result(request, submission_id):
    submission = Submission.objects.get(id=submission_id)

    choices = submission.choices.all()

    score = 0
    total = 0

    for choice in choices:
        if choice.is_correct:
            score += choice.question.grade
        total += choice.question.grade

    context = {
        'score': score,
        'total': total,
        'choices': choices
    }

    return render(request, 'onlinecourse/exam_result.html', context)
