from ninja import NinjaAPI, Schema
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth
from ninja_simple_jwt.auth.views.api import mobile_auth_router
from typing import List
from core.models import Course, CourseContent, CourseMember, Comment

# ============================
# JWT API
# ============================
api = NinjaAPI(
    title="SimpleLMS JWT API",
    version="1.0",
    urls_namespace="api-jwt"
)

# Router LOGIN / REGISTER JWT
api.add_router("/auth/", mobile_auth_router)

apiAuth = HttpJwtAuth()

# ============================
# SCHEMA
# ============================
class CourseMemberOut(Schema):
    id: int
    course_id: int
    user_id: int

    class Config:
        from_attributes = True


class EnrollOut(Schema):
    id: int
    course_id: int
    user_id: int

    class Config:
        from_attributes = True


class CommentIn(Schema):
    content_id: int
    comment: str


class CommentOut(Schema):
    id: int
    user_id: int
    comment: str
    course_content_id: int

    class Config:
        from_attributes = True


# ============================
# PROTECTED ROUTES (JWT)
# ============================
@api.get("mycourses/", auth=apiAuth, response=List[CourseMemberOut])
def get_mycourses(request):
    return CourseMember.objects.filter(user=request.user)


@api.post("course/{id}/enroll/", auth=apiAuth, response=EnrollOut)
def enroll_course(request, id: int):
    course = Course.objects.get(id=id)
    member, _ = CourseMember.objects.get_or_create(
        user=request.user,
        course=course
    )
    return member


@api.post("comments/", auth=apiAuth, response=CommentOut)
def post_comment(request, data: CommentIn):
    content = CourseContent.objects.get(id=data.content_id)

    if not CourseMember.objects.filter(user=request.user, course=content.course).exists():
        return {"detail": "not allowed"}

    c = Comment.objects.create(
        user=request.user,
        course_content=content,
        comment=data.comment
    )
    return c
