from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from core.models import Course, CourseMember, CourseContent


# ==================================================
# Test Model: Course
# ==================================================
class CourseModelTest(TestCase):

    def setUp(self):
        self.teacher = User.objects.create(username="teacher1")
        self.course = Course.objects.create(
            name="Pemrograman Django",
            description="Belajar Django",
            price=150000,
            teacher=self.teacher
        )

    def test_course_creation(self):
        course = Course.objects.get(name="Pemrograman Django")
        self.assertEqual(course.price, 150000)
        self.assertEqual(course.teacher.username, "teacher1")
        self.assertEqual(str(course), "Pemrograman Django : 150000")


# ==================================================
# Test Model: CourseMember
# ==================================================
class CourseMemberModelTest(TestCase):

    def setUp(self):
        self.teacher = User.objects.create(username="teacher1")
        self.student = User.objects.create(username="student1")
        self.course = Course.objects.create(
            name="Pemrograman Django",
            teacher=self.teacher
        )

    def test_course_member_creation(self):
        member = CourseMember.objects.create(
            course=self.course,
            user=self.student,
            role="std"
        )

        self.assertEqual(member.user.username, "student1")
        self.assertEqual(member.course.name, "Pemrograman Django")
        self.assertEqual(member.role, "std")


# ==================================================
# Test Model: CourseContent
# ==================================================
class CourseContentModelTest(TestCase):

    def setUp(self):
        self.teacher = User.objects.create(username="teacher1")
        self.course = Course.objects.create(
            name="Pemrograman Django",
            teacher=self.teacher
        )

    def test_course_content_creation(self):
        content = CourseContent.objects.create(
            title="Pengenalan Django",
            description="Materi dasar Django",
            course=self.course
        )

        self.assertEqual(content.course.name, "Pemrograman Django")
        self.assertEqual(content.title, "Pengenalan Django")
        self.assertEqual(str(content), f"[{self.course}] Pengenalan Django")


# ==================================================
# Test Query Course by Teacher
# ==================================================
class CourseQueryTest(TestCase):

    def setUp(self):
        self.teacher1 = User.objects.create(username="teacher1")
        self.teacher2 = User.objects.create(username="teacher2")

        Course.objects.create(name="Django", teacher=self.teacher1)
        Course.objects.create(name="Flask", teacher=self.teacher2)

    def test_course_filter_by_teacher(self):
        courses = Course.objects.filter(teacher=self.teacher1)
        self.assertEqual(courses.count(), 1)
        self.assertEqual(courses.first().name, "Django")


# ==================================================
# Test Validation Course
# ==================================================
class CourseValidationTest(TestCase):

    def setUp(self):
        self.teacher = User.objects.create(username="teacher1")

    def test_course_name_empty(self):
        course = Course(
            name="",
            description="Belajar Django",
            price=100000,
            teacher=self.teacher
        )
        with self.assertRaises(ValidationError):
            course.full_clean()

    def test_course_negative_price(self):
        course = Course(
            name="Course Harga Negatif",
            description="Test harga negatif",
            price=-5000,
            teacher=self.teacher
        )

        # Karena tidak ada validator harga, ini harusnya valid
        course.full_clean()
        course.save()

        saved_course = Course.objects.get(name="Course Harga Negatif")
        self.assertEqual(saved_course.price, -5000)


# ==================================================
# Test Filtering Course by Price
# ==================================================
class CourseFilteringTest(TestCase):

    def setUp(self):
        self.teacher = User.objects.create(username="teacher1")

        Course.objects.create(name="Kursus 1", price=100000, teacher=self.teacher)
        Course.objects.create(name="Kursus 2", price=200000, teacher=self.teacher)
        Course.objects.create(name="Kursus 3", price=300000, teacher=self.teacher)

    def test_filter_courses_by_price(self):
        affordable_courses = Course.objects.filter(price__lt=200000)
        self.assertEqual(affordable_courses.count(), 1)
        self.assertEqual(affordable_courses.first().name, "Kursus 1")
