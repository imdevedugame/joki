import os
import sys
import django
import csv

# ====== Setup Django ======
sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 3)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'simplelms.settings'
django.setup()

from django.contrib.auth.models import User
from core.models import Course, CourseMember, CourseContent, Comment

BASE_DIR = './csv_data'

# ====== IMPORT USERS ======
with open(os.path.join(BASE_DIR, 'user-data.csv'), newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not User.objects.filter(username=row['username']).exists():
            User.objects.create_user(
                username=row['username'],
                password=row['password'],
                email=row['email']
            )
print("✅ Users imported!")

# ====== IMPORT COURSES ======
with open(os.path.join(BASE_DIR, 'course-data.csv'), newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        teacher = User.objects.get(pk=int(row['teacher']))
        if not Course.objects.filter(name=row['name'], teacher=teacher).exists():
            Course.objects.create(
                name=row['name'],
                description=row['description'],
                price=int(row['price']),
                teacher=teacher
            )
print("✅ Courses imported!")

# ====== IMPORT COURSE MEMBERS ======
with open(os.path.join(BASE_DIR, 'member-data.csv'), newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        course = Course.objects.get(pk=int(row['course_id']))
        user = User.objects.get(pk=int(row['user_id']))
        if not CourseMember.objects.filter(course=course, user=user).exists():
            CourseMember.objects.create(
                course=course,
                user=user,
                role=row.get('roles', 'std')
            )
print("✅ Course Members imported!")

# ====== IMPORT COURSE CONTENT ======
with open(os.path.join(BASE_DIR, 'content-data.csv'), newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        course = Course.objects.get(pk=int(row['course_id']))
        if not CourseContent.objects.filter(title=row['title'], course=course).exists():
            parent = None
            if row.get('parent_id'):
                try:
                    parent = CourseContent.objects.get(pk=int(row['parent_id']))
                except CourseContent.DoesNotExist:
                    parent = None
            CourseContent.objects.create(
                title=row['title'],
                description=row.get('description', '-'),
                url=row.get('url'),
                file=row.get('file'),
                course=course,
                parent=parent
            )
print("✅ Course Content imported!")

# ====== IMPORT COMMENTS ======
with open(os.path.join(BASE_DIR, 'comment-data.csv'), newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            content = CourseContent.objects.get(pk=int(row['course_content_id']))
            user = User.objects.get(pk=int(row['user_id']))
        except (CourseContent.DoesNotExist, User.DoesNotExist, ValueError):
            continue  # skip baris invalid
        if not Comment.objects.filter(course_content=content, user=user, comment=row['comment']).exists():
            Comment.objects.create(
                course_content=content,
                user=user,
                comment=row['comment']
            )
print("✅ Comments imported!")
