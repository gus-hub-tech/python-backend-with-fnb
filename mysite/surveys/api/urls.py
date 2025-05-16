
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SurveyViewSet,
    QuestionViewSet,
    ChoiceViewSet,
    ResponseViewSet,
    AnswerViewSet,
    SurveyCreateViewSet
)

router = DefaultRouter()
router.register(r'surveys', SurveyViewSet)
router.register(r'answers', AnswerViewSet, basename='answer') # Added basename
router.register(r'responses', ResponseViewSet, basename='response') # Added basename
router.register(r'surveys/create', SurveyCreateViewSet, basename='survey-create')


# Nested routers
survey_router = DefaultRouter()
survey_router.register(r'questions', QuestionViewSet, basename='survey-questions')

question_router = DefaultRouter()
question_router.register(r'choices', ChoiceViewSet, basename='question-choices')

urlpatterns = [
    path('', include(router.urls)),
    path('surveys/<int:survey_pk>/', include(survey_router.urls)),
    path('questions/<int:question_pk>/', include(question_router.urls)),
    path('auth/', include('dj_rest_auth.urls')),
]
