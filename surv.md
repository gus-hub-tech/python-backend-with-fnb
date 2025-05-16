# 📝 Survey API - Django REST Framework

This project provides a simple REST API for creating and managing surveys using Django and Django REST Framework (DRF). The core component in this example is the `SurveyCreateViewSet`, which allows authenticated users to perform CRUD operations on surveys.

---

## 📁 Project Structure

your_project/
├── surveys/
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── urls.py
│ └── ...
├── your_project/
│ └── settings.py
└── manage.py

yaml
Copy
Edit

---

## 🚀 Features

- Full CRUD support for surveys
- Authentication required (using DRF's token/session authentication)
- Automatically records the user who created each survey
- Modular and scalable architecture

---

## 🔧 ViewSet Overview: `SurveyCreateViewSet`

```python
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Survey
from .serializers import SurveyCreateSerializer

class SurveyCreateViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveyCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
What it does:
Component	Description
ModelViewSet	Provides full CRUD operations
queryset	Fetches all Survey records
serializer_class	Uses SurveyCreateSerializer to validate and serialize data
permission_classes	Restricts access to authenticated users only
perform_create	Automatically sets created_by to the current user during survey creation

🧠 Model: Survey
Example model used by this viewset:

python
Copy
Edit
from django.db import models
from django.contrib.auth.models import User

class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
🧪 Serializer: SurveyCreateSerializer
Example serializer:

python
Copy
Edit
from rest_framework import serializers
from .models import Survey

class SurveyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'created_at']
