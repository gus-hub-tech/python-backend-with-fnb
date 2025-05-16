# 📝 Survey API - Django DRF

This API allows authenticated users to create surveys, including nested questions and answer choices. It also includes endpoints for answering surveys and viewing responses.

---

## 🔐 Authentication

Only authenticated users can access the survey creation endpoint. This is enforced using Django REST Framework's permission system.

```python
permission_classes = [IsAuthenticated]
