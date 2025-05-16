from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from ..models import Survey, Question, Choice, Response as SurveyResponse, Answer
from .serializers import (
    SurveySerializer,
    QuestionSerializer,
    ChoiceSerializer,
    ResponseSerializer,
    AnswerSerializer,
    SurveyCreateSerializer
)
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action

class SurveyCreateViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveyCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class SurveyViewSet(viewsets.ModelViewSet):
    """
    API endpoint for surveys with advanced filtering and analytics
    """
    queryset = Survey.objects.annotate(
        response_count=Count('responses')
    ).prefetch_related('questions__choices')
    serializer_class = SurveySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filterset_fields = ['created_by', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'response_count']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['get'], url_path='statistics')
    def get_statistics(self, request, pk=None):
        """
        Custom endpoint for survey statistics
        """
        survey = self.get_object()
        stats = {
            'total_responses': survey.responses.count(),
            'questions': []
        }

        for question in survey.questions.all():
            question_stats = {
                'id': question.id,
                'text': question.text,
                'type': question.question_type,
                'total_answers': question.answers.count()
            }

            if question.question_type == 'text':
                question_stats['sample_answers'] = list(
                    question.answers.exclude(text_answer__exact='')
                    .values_list('text_answer', flat=True)[:5]
                )
            else:
                question_stats['choices'] = []
                for choice in question.choices.all():
                    count = question.answers.filter(choice_answer=choice).count()
                    question_stats['choices'].append({
                        'id': choice.id,
                        'text': choice.text,
                        'count': count,
                        'percentage': count / question_stats['total_answers'] * 100 if question_stats['total_answers'] > 0 else 0
                    })

            stats['questions'].append(question_stats)

        return Response(stats)

class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for survey questions (Admin only)
    """
    queryset = Question.objects.select_related('survey').prefetch_related('choices')
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        survey_id = self.kwargs.get('survey_pk')
        if survey_id:
            return self.queryset.filter(survey__id=survey_id)
        return super().get_queryset()

class ChoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for question choices (Admin only)
    """
    queryset = Choice.objects.select_related('question')
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        question_id = self.kwargs.get('question_pk')
        if question_id:
            return self.queryset.filter(question__id=question_id)
        return super().get_queryset()

class ResponseViewSet(viewsets.ModelViewSet):
    """
    API endpoint for survey responses with answer validation
    """
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['survey', 'created_at']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return SurveyResponse.objects.filter(
            respondent=self.request.user
        ).prefetch_related('answers__question', 'answers__choice_answer')

    def perform_create(self, serializer):
        serializer.save(respondent=self.request.user)

    @action(detail=True, methods=['post'], url_path='submit-answers')
    def submit_answers(self, request, pk=None):
        """
        Submit multiple answers for a response
        """
        response = self.get_object()
        answers_data = request.data.get('answers', [])
        
        # Validate answers
        valid_answers = []
        for answer_data in answers_data:
            serializer = AnswerSerializer(data=answer_data)
            if serializer.is_valid():
                valid_answers.append(serializer.validated_data)
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Create answers
        for answer in valid_answers:
            question = answer['question']
            choices = answer.get('choice_answer', [])
            
            # Validate question belongs to survey
            if question.survey != response.survey:
                return Response(
                    {'error': 'Question does not belong to survey'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create answer
            answer_obj = Answer.objects.create(
                response=response,
                question=question,
                text_answer=answer.get('text_answer', '')
            )
            
            # Add choices if applicable
            if question.question_type in ['single', 'multiple']:
                answer_obj.choice_answer.set(choices)

        return Response({'status': 'answers submitted'})

class AnswerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoint for viewing answers
    """
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Answer.objects.filter(
            response__respondent=self.request.user
        ).select_related('question', 'response')