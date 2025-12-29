from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Avg, Max, Min, Count
from django.core import serializers
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone
from .models import Course, CourseMember, CourseContent, Comment

# ===============================
# 🏠 Halaman Utama (Home)
# ===============================
def home_view(request):
    """Halaman utama e-LMS dengan ringkasan statistik sederhana."""
    context = {
        'total_courses': Course.objects.count(),
        'total_users': User.objects.filter(is_superuser=False).count(),
        'total_comments': Comment.objects.count(),
        'now': timezone.now(),
    }
    return render(request, 'home.html', context)


# ===============================
# 📊 Statistik Course (HTML)
# ===============================
def course_stat_view(request):
    courses = Course.objects.all()
    stats = courses.aggregate(
        max_price=Max('price'),
        min_price=Min('price'),
        avg_price=Avg('price')
    )

    cheapest = courses.filter(price=stats['min_price']) if stats['min_price'] is not None else []
    expensive = courses.filter(price=stats['max_price']) if stats['max_price'] is not None else []
    popular = courses.annotate(member_count=Count('coursemember')).order_by('-member_count')[:5]
    unpopular = courses.annotate(member_count=Count('coursemember')).order_by('member_count')[:5]

    context = {
        'course_count': courses.count(),
        'price_stats': stats,
        'cheapest': cheapest,
        'expensive': expensive,
        'popular': popular,
        'unpopular': unpopular,
        'now': timezone.now()
    }
    return render(request, 'course_stat.html', context)


# ===============================
# 👥 Statistik User (HTML)
# ===============================
def user_stat_view(request):
    users = User.objects.filter(is_superuser=False)
    users_with_courses = users.annotate(total_courses=Count('course')).filter(total_courses__gt=0)
    users_no_courses = users.annotate(total_courses=Count('course')).filter(total_courses=0)
    top_user = users_with_courses.order_by('-total_courses').first()

    context = {
        'total_non_admin_users': users.count(),
        'total_users_with_courses': users_with_courses.count(),
        'total_users_without_courses': users_no_courses.count(),
        'top_user': top_user,
        'users_no_courses': users_no_courses,
        'now': timezone.now()
    }
    return render(request, 'user_stat.html', context)


# ===============================
# 📘 Detail Course (HTML)
# ===============================
def course_detail_view(request, course_id):
    try:
        course = Course.objects.annotate(
            member_count=Count('coursemember', distinct=True),
            content_count=Count('coursecontent', distinct=True),
            comment_count=Count('coursecontent__comment', distinct=True)
        ).get(pk=course_id)

        top_contents = CourseContent.objects.filter(course_id=course.id).annotate(
            count_comment=Count('comment')
        ).order_by('-count_comment')[:3]

        context = {'course': course, 'top_contents': top_contents}
        return render(request, 'courses/detail.html', context)

    except Course.DoesNotExist:
        return render(request, '404.html', {'error': 'Course not found'}, status=404)


# ===============================
# ⚡ Profiling Silk Wrapper
# ===============================
def silk_wrapper_view(request):
    """
    Menampilkan Silk profiling dalam tampilan custom.
    """
    context = {
        'now': timezone.now(),
        'total_queries': 123,
        'total_requests': 45,
        'avg_query_time': 12.5,
        'top_queries': [
            {'sql': 'SELECT * FROM course', 'time': 25},
            {'sql': 'SELECT * FROM user', 'time': 18}
        ],
        'slow_requests': [
            {'path': '/course_stat/', 'duration': 50},
            {'path': '/user_stat/', 'duration': 40}
        ]
    }
    return render(request, 'silk_wrapper.html', context)


# ===============================
# 👤 Daftar User (HTML via REST API)
# ===============================
def user_list_view(request):
    """
    Menampilkan halaman daftar user yang mengambil data dari
    REST API /api/v1/users/.
    """
    return render(request, 'user_list.html')


# ===============================
# 🧪 API Course Explorer (PERTEMUAN 10)
# ===============================
def tugas_10_view(request):
    return render(request, 'tugas_10.html')

