from django.db import models
from django.contrib.auth.models import User


class Instructor(models.Model):
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField(default=0)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Learner(models.Model):
    occupation = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Course(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='course_images/')
    description = models.TextField()
    pub_date = models.DateField()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    content = models.TextField()
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )

    def __str__(self):
        return self.title


# -------------------------
# Assessment Models
# -------------------------

class Question(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE
    )
    question_text = models.CharField(
        max_length=500
    )
    grade = models.IntegerField(
        default=1
    )

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    choice_text = models.CharField(
        max_length=200
    )
    is_correct = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    learner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    choices = models.ManyToManyField(
        Choice
    )

    def __str__(self):
        return str(self.id)
