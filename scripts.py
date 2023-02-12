import random
from datacenter.models import Schoolkid, Mark, Lesson
from datacenter.models import Chastisement, Commendation
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

PRAISES = ['Молодец!', 'Хвалю!',
           'Ты меня приятно удивил!',
           'Ты растешь над собой!', 'Так держать!']


def get_pupil(pupil_name):
    try:
        return Schoolkid.objects.get(full_name__contains=pupil_name)
    except MultipleObjectsReturned:
        print ('Найдено несколько учеников с таким именем. Уточните запрос')
    except ObjectDoesNotExist:
        print ('Ученик не найден. Уточните запрос')


def get_lesson(lesson_subject, pupil):
    lesson = Lesson.objects.filter(
            year_of_study=pupil.year_of_study,
            group_letter=pupil.group_letter,
            subject__title__contains=lesson_subject
            ).order_by('-date').first()
    if lesson:
        return lesson
    else: raise ObjectDoesNotExist ('Предмет не найден')


def fix_marks(pupil_name, grade):
    pupil = get_pupil(pupil_name)
    pupil_marks = Mark.objects.filter(schoolkid=pupil,
                                      points__lte=3)
    pupil_marks.update(points=grade)
    print('Оценки исправлены')
    

def remove_chastisements(pupil_name):
    pupil = get_pupil(pupil_name)
    chastisement = Chastisement.objects.filter(schoolkid=pupil)
    chastisement.delete()
    print('Замечания удалены')


def create_commendation(pupil_name, lesson_subject):
    pupil = get_pupil(pupil_name)
    lesson = get_lesson(lesson_subject, get_pupil(pupil_name))       
    Commendation.objects.create(teacher=lesson.teacher,
                                    created=lesson.date,
                                    subject=lesson.subject,
                                    text=random.choice(PRAISES),
                                    schoolkid=pupil)
    print('Создан положительный отзыв учителя')

