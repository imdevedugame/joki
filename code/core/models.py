from django.db import models
from django.contrib.auth.models import User

# ===============================
# 🟦 Model: Mata Kuliah
# ===============================
class Course(models.Model):
    name = models.CharField("Nama Matkul", max_length=100)
    description = models.TextField("Deskripsi", default='-')
    price = models.IntegerField("Harga", default=10000)
    image = models.ImageField("Gambar", null=True, blank=True)
    teacher = models.ForeignKey(User, verbose_name="Pengajar", on_delete=models.RESTRICT)
    created_at = models.DateTimeField("Dibuat pada", auto_now_add=True)
    updated_at = models.DateTimeField("Diperbarui pada", auto_now=True)

    class Meta:
        verbose_name = "Mata Kuliah"
        verbose_name_plural = "Mata Kuliah"

    def __str__(self) -> str:
        return f"{self.name} : {self.price}"


# ===============================
# 🟦 Model: Subscriber Matkul
# ===============================
ROLE_OPTIONS = [
    ('std', "Siswa"),
    ('ast', "Asisten"),
]

class CourseMember(models.Model):
    course = models.ForeignKey(Course, verbose_name="Matkul", on_delete=models.RESTRICT)
    user = models.ForeignKey(User, verbose_name="Siswa", on_delete=models.RESTRICT)
    role = models.CharField("Peran", max_length=3, choices=ROLE_OPTIONS, default='std')
    created_at = models.DateTimeField("Dibuat pada", auto_now_add=True)
    updated_at = models.DateTimeField("Diperbarui pada", auto_now=True)

    class Meta:
        verbose_name = "Subscriber Matkul"
        verbose_name_plural = "Subscriber Matkul"

    def __str__(self) -> str:
        return f"{self.course} - {self.user}"


# ===============================
# 🟦 Model: Konten Matkul
# ===============================
class CourseContent(models.Model):
    title = models.CharField("Judul Konten", max_length=200)
    description = models.TextField("Deskripsi", default='-')
    url = models.CharField("URL Video", max_length=200, null=True, blank=True)
    file = models.FileField("File", null=True, blank=True)
    course = models.ForeignKey(Course, verbose_name="Matkul", on_delete=models.RESTRICT)
    parent = models.ForeignKey("self", verbose_name="Induk", on_delete=models.RESTRICT, null=True, blank=True)
    created_at = models.DateTimeField("Dibuat pada", auto_now_add=True)
    updated_at = models.DateTimeField("Diperbarui pada", auto_now=True)

    class Meta:
        verbose_name = "Konten Matkul"
        verbose_name_plural = "Konten Matkul"

    def __str__(self) -> str:
        return f"[{self.course}] {self.title}"


# ===============================
# 🟦 Model: Komentar
# ===============================
class Comment(models.Model):
    course_content = models.ForeignKey(CourseContent, verbose_name="Konten", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Pengguna", on_delete=models.CASCADE)
    comment = models.TextField("Komentar")
    created_at = models.DateTimeField("Dibuat pada", auto_now_add=True)
    updated_at = models.DateTimeField("Diperbarui pada", auto_now=True)

    class Meta:
        verbose_name = "Komentar"
        verbose_name_plural = "Komentar"

    def __str__(self) -> str:
        return f"{self.user.username} - {self.course_content.title}"
