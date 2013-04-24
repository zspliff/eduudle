from django.contrib import admin
from euudle.models import *
from accounts.models import *
from stat_analysis.models import *

admin.site.register(coursera_course)
#admin.site.register(coursera_university)
#admin.site.register(coursera_instructor)
#admin.site.register(edx_university)
#admin.site.register(edx_instructor)
admin.site.register(edx_course)
admin.site.register(Account)
#admin.site.register(udacity_instructor)
admin.site.register(udacity_course)
admin.site.register(keyword)
admin.site.register(BaseCourse)
admin.site.register(BaseInstructor)
admin.site.register(common_university)
admin.site.register(Sessions)
admin.site.register(statistical_data)
