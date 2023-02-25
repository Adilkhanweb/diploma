# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from api.v1.serializers import CourseListSerializer
# from course.models import Course
#
#
# @api_view(["GET"])
# def get_courses(request):
#     courses = Course.objects.all()
#     serializer = CourseListSerializer(courses, many=True)
#     return Response(serializer.data)
#
#
# class CourseList(APIView):
#     def get(self, request):
#         courses = Course.objects.all()
#         serializer = CourseListSerializer(courses, many=True)
#         return Response(serializer.data)
