from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Course, Submission, Choice


def submit(request, course_id):

    course = get_object_or_404(Course, pk=course_id)

    selected_choices = []

    for key in request.POST:
        if key.startswith('choice'):
            selected_choices.append(int(request.POST[key]))

    submission = Submission.objects.create(
        learner=request.user
    )

    submission.choices.set(selected_choices)

    return HttpResponseRedirect(
        reverse(
            'onlinecourse:show_exam_result',
            args=(course.id, submission.id)
        )
    )


def show_exam_result(request, course_id, submission_id):

    course = get_object_or_404(Course, pk=course_id)

    submission = get_object_or_404(
        Submission,
        pk=submission_id
    )

    choices = submission.choices.all()

    total_score = 0
    earned_score = 0

    for lesson in course.lessons.all():

        questions = lesson.question_set.all()

        for question in questions:

            total_score += question.grade

            correct_choices = set(
                question.choice_set.filter(
                    is_correct=True
                ).values_list(
                    'id',
                    flat=True
                )
            )

            selected_choices = set(
                choices.filter(
                    question=question
                ).values_list(
                    'id',
                    flat=True
                )
            )

            if correct_choices == selected_choices:
                earned_score += question.grade

    grade = 0

    if total_score > 0:
        grade = round(
            earned_score / total_score * 100,
            2
        )

    context = {
        'course': course,
        'submission': submission,
        'grade': grade,
        'earned_score': earned_score,
        'total_score': total_score,
    }

    return render(
        request,
        'onlinecourse/exam_result_bootstrap.html',
        context
    )
