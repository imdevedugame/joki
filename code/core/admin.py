from django.contrib import admin
from .models import Course, CourseMember, CourseContent, Comment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'price', 'created_at')
    search_fields = ('name', 'teacher__username')
    list_filter = ('teacher',)
    ordering = ('-created_at',)

    class Meta:
        verbose_name = "Mata Kuliah"
        verbose_name_plural = "Mata Kuliah"


@admin.register(CourseMember)
class CourseMemberAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'role', 'created_at')
    search_fields = ('course__name', 'user__username')
    list_filter = ('role',)
    ordering = ('-created_at',)

    class Meta:
        verbose_name = "Subscriber Matkul"
        verbose_name_plural = "Subscriber Matkul"


@admin.register(CourseContent)
class CourseContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'url', 'created_at')
    search_fields = ('title', 'course__name')
    list_filter = ('course',)
    ordering = ('-created_at',)

    class Meta:
        verbose_name = "Konten Matkul"
        verbose_name_plural = "Konten Matkul"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('course_content', 'user', 'comment', 'created_at')
    search_fields = ('course_content__title', 'user__username')
    list_filter = ('course_content',)
    ordering = ('-created_at',)

    class Meta:
        verbose_name = "Komentar"
        verbose_name_plural = "Komentar"
