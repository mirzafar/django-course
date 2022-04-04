from django.db import models

class Siteuser(models.Model):
    last_name = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=200, blank=True)
    middle_name = models.CharField(max_length=200, blank=True)
    iin = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)
    password = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.last_name + ' ' + self.phone


class CourseCategory(models.Model):
    title = models.CharField(max_length=300)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=300)
    category = models.ForeignKey(CourseCategory,blank=True, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='upload', blank=True)
    lessons_count = models.IntegerField(default=0, blank=True)
    description = models.TextField(blank=True)
    is_free = models.BooleanField(default=0)
    is_profession = models.BooleanField(default=0)
    is_certified = models.BooleanField(default=0)
    info1 = models.CharField(blank=True, max_length=300)
    info1_text = models.TextField(blank=True)

    info2 = models.CharField(blank=True, max_length=300)
    info2_text = models.TextField(blank=True)

    info3 = models.CharField(blank=True, max_length=300)
    info3_text = models.TextField(blank=True)

    info4 = models.CharField(blank=True, max_length=300)
    info4_text = models.TextField(blank=True)

    status = models.IntegerField(default=0)
    course_type = models.IntegerField(default=0, blank=True)


    def __str__(self):
        return self.title


class CourseItem(models.Model):
    title = models.CharField(max_length=300)
    video_link = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    description2 = models.TextField(blank=True)
    video_minutes = models.IntegerField(default=0, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    task = models.TextField(blank=True)
    task_code = models.TextField(blank=True)


    def __str__(self):
        return self.course.title + ' ' + self.title + ' ' + str(self.id)


class CourseItemParagraph(models.Model):
    title = models.CharField(max_length=300, blank=True)
    video_link = models.CharField(max_length=300, blank=True)
    description1 = models.TextField(blank=True)
    description2 = models.TextField(blank=True)
    description3 = models.TextField(blank=True)
    logo = models.ImageField(upload_to='upload', blank=True)
    course_item = models.ForeignKey(CourseItem, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    def __str__(self):
        return self.course_item.title + ' ' + self.title


class SiteuserCourse(models.Model):
    title = models.CharField(max_length=300, blank=True, default='New course')
    site_user = models.ForeignKey(Siteuser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField(blank=True)
    stop_datetime = models.DateTimeField(blank=True)
    position = models.IntegerField(blank=True, default=0)
    priority = models.IntegerField(blank=True, default=0)
    rate = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return f'{self.site_user.last_name} {self.site_user.first_name} {self.site_user.id} {self.course.title}'


class News(models.Model):
    title = models.CharField(max_length=300, blank=True, default='')
    mini_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    create_datetime = models.DateTimeField(blank=True)
    views_count = models.IntegerField(blank=True, default=0)
    logo = models.ImageField(upload_to='upload', blank=True)

    def __str__(self):
        return self.title
