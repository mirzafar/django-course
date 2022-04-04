from django.shortcuts import render
from main.models import *
import random
import requests
from django.shortcuts import redirect
import re
from hashlib import md5
from datetime import datetime
import os, uuid
from smsc.settings import BASE_DIR
from django.http.response import JsonResponse
import  base64
from django.core.files.base import ContentFile

email_regex = re.compile(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')
phone_regexp = re.compile(r'^77[0-9]{9}$')
iin_regexp = re.compile(r'[0-9]{12}$')


def get_random_number(random_len):
    random_len = int(random_len)
    a = pow(10, random_len)
    b = pow(10, random_len-1)
    n = random.randint(b, a)
    return n


def send_message(phone, sms):
    sms_domain = 'https://smsc.kz/sys/send.php'
    sms_params = {
        'login': 'sanzharirissaliyev',
        'psw': '$anko.Sanko',
        'mes': sms,
        'fmt': 3,
        'phones': phone,
    }
    r = requests.post(sms_domain, data=sms_params)
    print(r.status_code)
    print(r.json())
    print(phone)
    print(sms)


def mainHandler(request):
    user_id = request.session.get('user_id', None)
    active_user = None
    if user_id:
        active_user = Siteuser.objects.get(id=int(user_id))

    courses = Course.objects.all()[:9]
    course_count = Course.objects.count()

    new_list = News.objects.all().order_by('-create_datetime')[:3]

    popular_new_list = News.objects.all().order_by('-views_count')[:3]

    return render(request, 'index.html', {'user_id': user_id,
                                          'active_user': active_user,
                                          'courses': courses,
                                          'course_count': course_count,
                                          'new_list': new_list,
                                          'popular_new_list': popular_new_list,
                                          })


def courseHandler(request):
    user_id = request.session.get('user_id', None)
    active_user = None
    if user_id:
        active_user = Siteuser.objects.get(id=int(user_id))


    all_courses = Course.objects.all()
    all_categories = CourseCategory.objects.all()

    return render(request, 'course.html', {'user_id': user_id,
                                           'active_user': active_user,
                                           'all_courses': all_courses,
                                           'all_categories': all_categories
                                           })


def courseItemHandler(request, course_id):
    active_lesson_number = int(request.GET.get('lesson', 1))
    active_lesson_number_index = active_lesson_number - 1
    user_id = request.session.get('user_id', None)
    active_user = None
    user_have_course =False




    if user_id:
        active_user = Siteuser.objects.get(id=int(user_id))

        all_user_courses = SiteuserCourse.objects.filter(course__id = course_id).filter(site_user__id = active_user.id)
        if all_user_courses:
            user_have_course = True

        if request.POST:
            action = request.POST.get('action', '')
            if action == 'start_course':
                user_courses = SiteuserCourse.objects.filter(course__id = course_id).filter(site_user__id = active_user.id)
                print(user_courses)
                if user_courses:
                    pass
                else:
                    new_site_user_course = SiteuserCourse()
                    new_site_user_course.start_datetime = datetime.now()
                    new_site_user_course.stop_datetime = datetime.now()
                    new_site_user_course.site_user = Siteuser.objects.get(id=int(user_id))
                    new_site_user_course.course = Course.objects.get(id=course_id)
                    new_site_user_course.save()
                    user_have_course = True





    course = Course.objects.get(id=course_id)
    course_lesson_count = CourseItem.objects.filter(course__id = course_id).count()
    lesson_counts = range(1, course_lesson_count + 1)
    course_items = CourseItem.objects.filter(course__id = course_id)
    first_course_item = None
    paragraphs = []
    if course_items:
        if len(course_items) > active_lesson_number_index:
            first_course_item = course_items[active_lesson_number_index]
            paragraphs = CourseItemParagraph.objects.filter(course_item__id=first_course_item.id)

    return render(request, 'course_item.php', {'user_id': user_id,
                                                'active_user': active_user,
                                                'course': course,
                                                'course_lesson_count': course_lesson_count,
                                                'first_course_item': first_course_item,
                                                'paragraphs': paragraphs,
                                                'lesson_counts': lesson_counts,
                                                'active_lesson_number': active_lesson_number,
                                                'user_have_course': user_have_course,

                                                })



def loginHandler(request):
    post_error = ''
    if request.POST:
        login = request.POST.get('login', '')
        password = request.POST.get('password', '')
        if login and password:

            temp_hash = md5()
            temp_hash.update(password.encode())
            password_hash = temp_hash.hexdigest()

            site_user = Siteuser.objects.filter(phone=login).filter(password=password_hash)
            if not site_user:
                site_user = Siteuser.objects.filter(email=login).filter(password=password_hash)
            if site_user:
                site_user = site_user[0]
                request.session['user_id'] = site_user.id
                return redirect('/')
            else:
                post_error = 'USER_NOT_FOUND'
        else:
            post_error = 'ERROR_ARGUMENTS'

    return render(request, 'login.html', {'post_error': post_error})



def logoutHandler(request):
    request.session['user_id'] = None
    return redirect('/')

    return render(request, 'logout.html', {})


def registerHandler(request):
    if request.POST:
        phone = request.POST.get('phone', '')
        if phone:
            if len(phone) == 11:
               site_user = Siteuser.objects.filter(phone=phone)
               if site_user:
                   new_site_user = site_user[0]
                   old_password = str(get_random_number(4))
                   print(old_password)
                   password_hash = md5()
                   password_hash.update(old_password.encode())
                   new_passwoord = password_hash.hexdigest()

                   new_site_user.password = new_passwoord
                   new_site_user.save()
                   message = 'Kod dlya registrasiya ' + str(old_password)
                   send_message(phone, message)
                   return redirect('/login/')
               else:
                   new_site_user = Siteuser()
                   new_site_user.phone = phone

                   old_password = str(get_random_number(4))
                   print(old_password)
                   password_hash = md5()
                   password_hash.update(old_password.encode())
                   new_passwoord = password_hash.hexdigest()

                   new_site_user.password = new_passwoord
                   new_site_user.save()
                   message = 'Kod dlya registrasiya ' + str(old_password)
                   send_message(phone, message)

                   return redirect('/login/')
            else:
                print('FORMAT ErROR')
        else:
            print('NO ARGUMRNT')
    return render(request, 'register.html', {})


def editHandler(request):
    user_id = request.session.get('user_id', None)
    active_user = None
    post_errors = []

    if user_id:
        active_user = Siteuser.objects.get(id=int(user_id))
        if request.POST:
            last_name = request.POST.get('last_name', '')
            first_name = request.POST.get('first_name', '')
            middle_name = request.POST.get('middle_name', '')
            iin = request.POST.get('iin', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            active_password = request.POST.get('active_password', '')
            new_password = request.POST.get('new_password', '')
            new_password_repeat = request.POST.get('new_password_repeat', '')

            active_user.last_name = last_name
            active_user.first_name = first_name
            active_user.middle_name = middle_name
            if iin:
                if iin_regexp.match(iin):
                    active_user.iin = iin
                else:
                    post_errors.append('IIN_FORMAT_ERROR')
            if email:
                if email_regex.match(email):
                    email_users = Siteuser.objects.filter(email=email)
                    if email_users:
                        email_user = email_users[0]
                        if email_user.id == active_user.id:
                            pass
                        else:
                            post_errors.append('EMAIL_REGISTERED')
                    else:
                        active_user.email = email
                else:
                    post_errors.append('EMAIL_FORMAT_ERROR')

            if phone:
                if phone_regexp.match(phone):
                    email_users = Siteuser.objects.filter(phone=phone)
                    if email_users:
                        email_user = email_users[0]
                        if email_user.id == active_user.id:
                            pass
                        else:
                            post_errors.append('PHONE_REGISTERED')
                    else:
                        active_user.phone = phone
                else:
                    post_errors.append('PHONE_FORMAT_ERROR')


            if active_password and new_password and new_password_repeat:
                temp_hash = md5()
                temp_hash.update(active_password.encode())
                active_password_hash = temp_hash.hexdigest()
                if active_user.password == active_password_hash:
                    if new_password == new_password_repeat:
                        new_temp_hash =md5()
                        new_temp_hash.update(new_password.encode())
                        new_password_hash = new_temp_hash.hexdigest()
                        active_user.password = new_password_hash
                    else:
                        post_errors.append('NEW_PASSWORD_INCORRECT')
                else:
                    post_errors.append('ACTIVE_PASSWORD_INCORRECT')

            active_user.save()
    return render(request, 'profile/edit.html', {'user_id': user_id,
                                         'active_user': active_user,
                                         'post_errors': post_errors})



def profileCoursesHandler(request):
    user_id = request.session.get('user_id', None)
    active_user = None
    my_courses = []
    if user_id:
        active_user = Siteuser.objects.get(id=int(user_id))
        my_courses = SiteuserCourse.objects.filter(site_user__id = active_user.id)
        course_count = len(SiteuserCourse.objects.filter(site_user__id = active_user.id))

    return render(request, 'profile/courses.html', {'user_id': user_id,
                                          'active_user': active_user,
                                          'my_courses': my_courses,
                                          'course_count': course_count
                                          })


def apiHandler(request):

    return render(request, 'api/index.html', {})


def apiCourseCategoriesHandler(request):
    if request.POST:
        action = request.POST.get('action', '')
        id = int(request.POST.get('id', 0))
        if action == 'delete':
            cc = CourseCategory.objects.get(id=id)
            cc.delete()

    items = CourseCategory.objects.all()

    return render(request, 'api/course_categories.html', {'items': items})


def apiCourseCategoriesAddHandler(request):
    if request.POST:
        action = request.POST.get('action', '')
        title = request.POST.get('title', '')
        status = int(request.POST.get('status', 0))
        if action == 'add':
            cc = CourseCategory()
            cc.title = title
            cc.status = status
            cc.save()

    return render(request, 'api/course_categories_item.html', {})


def apiCourseCategoriesEditHandler(request, item_id):
    if request.POST:
        action = request.POST.get('action', '')
        title = request.POST.get('title', '')
        status = int(request.POST.get('status', 0))
        if action == 'edit':
            cc = CourseCategory.objects.get(id = int(item_id))
            cc.title = title
            cc.status = status
            cc.save()

    item = CourseCategory.objects.get(id=int(item_id))

    return render(request, 'api/course_categories_item_edit.html', {'item': item})


def apiCoursesHandler(request):
    if request.POST:
        action = request.POST.get('action', '')
        id = int(request.POST.get('id', 0))
        if action == 'delete':
            cc = Course.objects.get(id=id)
            cc.delete()

    items = Course.objects.all()

    return render(request, 'api/courses.html', {'items': items})


def apiCoursesAddHandler(request):
    if request.POST:
        action = request.POST.get('action', '')
        title = request.POST.get('title', '')
        category_id = int(request.POST.get('category_id', 0))
        lessons_count = int(request.POST.get('lessons_count', 0))
        description = request.POST.get('description', '')
        info1 = request.POST.get('info1', '')
        info1_text = request.POST.get('info1_text', '')
        status = int(request.POST.get('status', 0))
        logo = request.POST.get('logo', '')
        is_free = request.POST.get('is_free', '')
        if action == 'add':
            cc = Course()
            cc.title = title
            # cc.category_id = category_id
            cc.category = CourseCategory.objects.get(id=category_id)
            cc.status = status
            cc.lessons_count = lessons_count
            cc.description = description
            cc.info1 = info1
            cc.logo = logo
            cc.info1_text = info1_text
            if is_free:
                cc.is_free = True
            else:
                cc.is_free = False
            cc.save()

    categories = CourseCategory.objects.all()

    return render(request, 'api/courses_item.html', {'categories': categories})


def apiCoursesEditHandler(request, item_id):
    if request.POST:
        action = request.POST.get('action', '')
        title = request.POST.get('title', '')
        category_id = int(request.POST.get('category_id', 0))
        lessons_count = int(request.POST.get('lessons_count', 0))
        description = request.POST.get('description', '')
        info1 = request.POST.get('info1', '')
        info1_text = request.POST.get('info1_text', '')
        status = int(request.POST.get('status', 0))
        is_free = request.POST.get('is_free', '')
        logo = request.POST.get('logo','')
        if action == 'edit':
            cc = Course.objects.get(id = int(item_id))
            cc.title = title
            cc.category = CourseCategory.objects.get(id=category_id)
            cc.lessons_count = lessons_count
            cc.description = description
            cc.info1 = info1
            cc.logo = logo
            cc.info1_text = info1_text
            cc.status = status
            if is_free:
                cc.is_free = True
            else:
                cc.is_free = False
            cc.save()
    categories = CourseCategory.objects.all()
    item = Course.objects.get(id=int(item_id))

    return render(request, 'api/courses_edit.html', {'item': item, 'categories': categories})


def apiUploadHandler(request):
    file_name = ''

    if request.POST:
        fileinfo = request.FILES.get('file')
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) +extn
            FILE_DIR = os.path.join(BASE_DIR, 'media', 'upload/')
            fh = open(FILE_DIR + cname, 'wb')
            print('file size is -> ', fileinfo.size)
            fh.write(fileinfo.read())
            fh.close()
            file_name = cname
        image_base = request.POST.get('image_base', None)
        if image_base:
            image_data = image_base
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            cname = str(uuid.uuid4()) + '.' + ext
            FILE_DIR = os.path.join(BASE_DIR, 'media', 'upload/')
            fh = open(FILE_DIR + cname, 'wb')
            fh.write(base64.b64decode((imgstr)))
            fh.close()
            file_name = cname

    response = JsonResponse({'success': True, 'file_name': file_name})
    response.status_code = 200
    return response


def newfileHandler(request):
    return render(request, 'newfile.html', {})