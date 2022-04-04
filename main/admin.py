from django.contrib import admin
from main.models import *


class SiteuserAdmin(admin.ModelAdmin):
    pass
admin.site.register(Siteuser, SiteuserAdmin)


class CourseCategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(CourseCategory, CourseCategoryAdmin)


class CourseAdmin(admin.ModelAdmin):
    pass
admin.site.register(Course, CourseAdmin)


class CourseItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(CourseItem, CourseItemAdmin)


class CourseItemParagraphAdmin(admin.ModelAdmin):
    pass
admin.site.register(CourseItemParagraph, CourseItemParagraphAdmin)


class SiteuserCourseAdmin(admin.ModelAdmin):
    pass
admin.site.register(SiteuserCourse, SiteuserCourseAdmin)


class NewsAdmin(admin.ModelAdmin):
    pass
admin.site.register(News, NewsAdmin)

