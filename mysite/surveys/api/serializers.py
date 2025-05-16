from rest_framework import serializers
from ..models import Survey, Question, Choice, Response, Answer

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'value']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'is_required', 'order', 'choices']

class SurveyCreateSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Survey
        fields = [
            'title', 'description', 'is_active',
            'questions'
        ]
        extra_kwargs = {
            'created_by': {'read_only': True}
        }

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        survey = Survey.objects.create(
            **validated_data,
            created_by=self.context['request'].user
        )

        for question_data in questions_data:
            choices_data = question_data.pop('choices', [])
            question = Question.objects.create(
                survey=survey,
                **question_data
            )

            for choice_data in choices_data:
                Choice.objects.create(
                    question=question,
                    **choice_data
                )

        return survey

class SurveySerializer(serializers.HyperlinkedModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    created_by = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = Survey
        fields = [
            'url', 'id', 'title', 'description', 
            'created_by', 'created_at', 'updated_at',
            'is_active', 'questions'
        ]

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['question', 'text_answer', 'choice_answer']



class ResponseSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    
    class Meta:
        model = Response
        fields = ['id', 'survey', 'respondent', 'created_at', 'answers']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        response = Response.objects.create(**validated_data)
        
        for answer_data in answers_data:
            choices = answer_data.pop('choice_answer', [])
            answer = Answer.objects.create(response=response, **answer_data)
            answer.choice_answer.set(choices)
            
        return response