from rest_framework import routers
from views import QuestionViewSet, AnswerViewSet, TrackerViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'questions', QuestionViewSet, base_name='questions')
router.register(r'answers', AnswerViewSet, base_name='answers')
router.register(r'trackers', TrackerViewSet, base_name='trackers')