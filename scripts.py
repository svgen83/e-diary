import random
from datacenter.models import Schoolkid, Mark, Lesson
from datacenter.models import Chastisement, Commendation
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def fix_marks(pupil_name, grade):
    try:
        pupil = Schoolkid.objects.get(full_name__contains=pupil_name)
        pupil_marks = Mark.objects.filter(schoolkid=pupil,
                                          points__lte=3)
        pupil_marks.update(points=grade)
        print('Оценки исправлены')
    except MultipleObjectsReturned:
        print('Найдено несколько учеников с таким именем. Уточните запрос')
    except ObjectDoesNotExist:
        print('Ученик не найден. Уточните запрос')


def remove_chastisements(pupil_name):
    try:
        pupil = Schoolkid.objects.get(full_name__contains=pupil_name)
        chastisement = Chastisement.objects.filter(schoolkid=pupil)
        chastisement.delete()
        print('Замечания удалены')
    except MultipleObjectsReturned:
        print('Найдено несколько учеников с таким именем. Уточните запрос')
    except ObjectDoesNotExist:
        print('Ученик не найден. Уточните запрос')


def create_commendation(pupil_name, lesson_subject):
    try:
        pupil = Schoolkid.objects.get(full_name__contains=pupil_name)
        lesson = Lesson.objects.filter(
            year_of_study=pupil.year_of_study,
            group_letter=pupil.group_letter,
            subject__title__contains=lesson_subject
            ).order_by('-date').last()
        prases = ['Молодец!', 'Хвалю!',
                  'Ты меня приятно удивил!',
                  'Ты растешь над собой!', 'Так держать!']
        Commendation.objects.create(teacher=lesson.teacher,
                                    created=lesson.date,
                                    subject=lesson.subject,
                                    text=random.choice(prases),
                                    schoolkid=pupil)
        print('Создан положительный отзыв учителя')
    except MultipleObjectsReturned:
        print('Найдено несколько учеников с таким именем. Уточните запрос')
    except ObjectDoesNotExist:
        print('Ученик не найден. Уточните запрос')
