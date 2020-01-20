from celery import shared_task
from django.contrib.auth.models import Group
from django.db import IntegrityError

from accounts.models import User
from accounts.task import user_send_mail
from schools.models import SchoolStudent


@shared_task
def register_students(user, students):
    # school = School.objects.get(user_id=school_id)
    if len(students) > 1:
        print("AAAAAAA")
        for student in students:
            if len(student) > 0:
                print("BBBBB")
                if student[0] != "No":
                    print("CCCCCC")
                    if len(student) < 4:
                        print("DDDDDD")
                        i = len(student)
                        while i < 4:
                            student.append("")
                            i += 1
                    print("EEEEE")
                    try:
                        print("FFFFFF")
                        s, _ = User.objects.get_or_create(username=student[1],
                                                          first_name=student[2],
                                                          last_name=student[3],
                                                          email=student[4],
                                                          phone=student[5])

                        s.account_type = 'student'
                        Group.objects.get_or_create(name="Students")
                        user_group = Group.objects.get(name='Students')
                        password = User.objects.make_random_password()
                        s.set_password(password)
                        print(password)
                        file = open('student.txt', 'a')
                        file.write("{:<20}{:>10}\n".format(s.username, password))
                        file.close()
                        user_send_mail.delay(user=s, password=password, host=user.email)
                        # send_mail('Account Password', 'UserName: {}\n'
                        #                               'First Name: {}\n'
                        #                               'Last Name: {}\n'
                        #                               'Password for your account is {}'
                        #                               ''.format(s.username, s.first_name, s.last_name,
                        #                                         password),
                        #           request.user.email,
                        #           [s.email])
                        s.save()
                        user_group.user_set.add(s)
                        SchoolStudent.objects.get_or_create(user=s, school=user.school_profile)
                    except IntegrityError:
                        pass

#
# @shared_task
# def register_teachers(user, teachers):
#     if len(teachers) > 1:
#         print("AAAAAAA")
#         for teacher in teachers:
#             if len(teacher) > 0:
#                 print("BBBBB")
#                 if teacher[0] != "No":
#                     print("CCCCCC")
#                     if len(teacher) < 4:
#                         print("DDDDDD")
#                         i = len(teacher)
#                         while i < 4:
#                             teacher.append("")
#                             i += 1
#                     print("EEEEE")
#                     try:
#                         print("FFFFFF")
#                         s, _ = User.objects.get_or_create(username=teacher[1],
#                                                      first_name=teacher[2],
#                                                      last_name=teacher[3],
#                                                      email=teacher[4],
#                                                      phone=teacher[5])
#
#                         s.account_type = 'student'
#                         Group.objects.get_or_create(name="Students")
#                         user_group = Group.objects.get(name='Students')
#                         password = User.objects.make_random_password()
#                         s.set_password(password)
#                         print(password)
#                         file = open('student.txt', 'a')
#                         file.write("{:<20}{:>10}\n".format(s.username, password))
#                         file.close()
#                         user_send_mail.delay(user=s, password=password, host=user.email)
#                         # send_mail('Account Password', 'UserName: {}\n'
#                         #                               'First Name: {}\n'
#                         #                               'Last Name: {}\n'
#                         #                               'Password for your account is {}'
#                         #                               ''.format(s.username, s.first_name, s.last_name,
#                         #                                         password),
#                         #           request.user.email,
#                         #           [s.email])
#                         s.save()
#                         user_group.user_set.add(s)
#                         Teacher.objects.get_or_create(user=s, school=user.school_profile, grade=teacher[6])
#                     except IntegrityError:
#                         pass
#
