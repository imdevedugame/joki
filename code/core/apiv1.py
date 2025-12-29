from ninja import NinjaAPI, Schema
from ninja.throttling import AnonRateThrottle
from ninja.pagination import paginate, PageNumberPagination
from ninja import Query, FilterSchema
from ninja.router import Router

from django.contrib.auth.models import User
from django.db.models import Q
from core.models import Course, CourseContent, CourseMember, Comment
from typing import List, Optional

# =====================================================
# PUBLIC API (NON-JWT)
# =====================================================
apiv1 = NinjaAPI(
    title="SimpleLMS Public API (Non-JWT)",
    version="1.0",
    urls_namespace="api-nonjwt",
)

# =====================================================
# ROUTER (TANPA THROTTLING GLOBAL ❗)
# =====================================================
router = Router()

# =====================================================
# HELLO (TES THROTTLING) ✅
# =====================================================
@router.get("hello/", throttle=AnonRateThrottle("10/s"))
def hello_api(request):
    return {"message": "Menyala abangkuhh 🔥❤️"}

# =====================================================
# USER
# =====================================================
class RegisterSchema(Schema):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str


class UserOut(Schema):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True


@router.post("register/", response=UserOut)
def register(request, data: RegisterSchema):
    return User.objects.create_user(
        username=data.username,
        password=data.password,
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
    )


@router.get("users/", response=List[UserOut])
def get_users(request):
    return User.objects.all()

# =====================================================
# COURSE SCHEMA
# =====================================================
class CourseIn(Schema):
    name: str
    description: str
    price: int


class CourseOut(Schema):
    id: int
    name: str
    description: str
    price: int
    teacher_id: int

    class Config:
        from_attributes = True

# =====================================================
# FILTER COURSE
# =====================================================
class CourseFilter(FilterSchema):
    search: Optional[str] = None
    price_gte: Optional[int] = None
    price_lte: Optional[int] = None

    def filter_search(self, value: str):
        return Q(name__icontains=value) | Q(description__icontains=value)

    def filter_price_gte(self, value: int):
        return Q(price__gte=value)

    def filter_price_lte(self, value: int):
        return Q(price__lte=value)

# =====================================================
# LIST COURSE (FILTER + SORT + PAGINATION) ✅
# =====================================================
@router.get("courses/", response=List[CourseOut])
@paginate(PageNumberPagination, page_size=5)
def list_courses(request, filters: CourseFilter = Query(None)):
    queryset = Course.objects.all()

    # FILTERING
    if filters:
        queryset = filters.filter(queryset)

    # SORTING
    order_by = request.GET.get("order_by")
    allowed = ["price", "-price", "name", "-name"]
    if order_by in allowed:
        queryset = queryset.order_by(order_by)

    return queryset

# =====================================================
# CRUD COURSE
# =====================================================
@router.post("courses/", response=CourseOut)
def create_course(request, data: CourseIn):
    teacher = User.objects.first()
    return Course.objects.create(
        name=data.name,
        description=data.description,
        price=data.price,
        teacher=teacher,
    )


@router.put("courses/{course_id}", response=CourseOut)
def update_course(request, course_id: int, data: CourseIn):
    course = Course.objects.get(id=course_id)
    course.name = data.name
    course.description = data.description
    course.price = data.price
    course.save()
    return course


@router.delete("courses/{course_id}")
def delete_course(request, course_id: int):
    CourseMember.objects.filter(course_id=course_id).delete()
    CourseContent.objects.filter(course_id=course_id).delete()
    Course.objects.filter(id=course_id).delete()
    return {"message": "Course deleted"}

# =====================================================
# CONTENT
# =====================================================
class ContentIn(Schema):
    title: str
    description: str
    url: Optional[str] = None


class ContentOut(Schema):
    id: int
    title: str
    description: str
    url: Optional[str]
    course_id: int

    class Config:
        from_attributes = True


@router.get("contents/{course_id}", response=List[ContentOut])
def list_content(request, course_id: int):
    return CourseContent.objects.filter(course_id=course_id)


@router.post("contents/{course_id}", response=ContentOut)
def create_content(request, course_id: int, data: ContentIn):
    return CourseContent.objects.create(
        title=data.title,
        description=data.description,
        url=data.url,
        course_id=course_id,
    )


@router.delete("contents/{content_id}")
def delete_content(request, content_id: int):
    CourseContent.objects.filter(id=content_id).delete()
    return {"message": "Content deleted"}

# =====================================================
# COMMENT
# =====================================================
class CommentIn(Schema):
    user_id: int
    comment: str


class CommentOut(Schema):
    id: int
    user_id: int
    comment: str
    course_content_id: int

    class Config:
        from_attributes = True


@router.post("comment/{content_id}", response=CommentOut)
def add_comment(request, content_id: int, data: CommentIn):
    return Comment.objects.create(
        course_content_id=content_id,
        user_id=data.user_id,
        comment=data.comment,
    )


@router.get("comment/{content_id}", response=List[CommentOut])
def list_comment(request, content_id: int):
    return Comment.objects.filter(course_content_id=content_id)

# =====================================================
# REGISTER ROUTER
# =====================================================
apiv1.add_router("", router)
