from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
  
    status_choices = [
        ('completed', 'Completed'),
        ('pending', 'Pending'),
    ]

    category_choices = [
        ('morning_routine', 'Morning Routine'),
        ('career', 'Career'),
        ('personal_growth', 'Personal Growth'),
        ('recreation', 'Recreation'),
    ]

    priority_choices = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)  
    status = models.CharField(max_length=50, choices=status_choices, default='pending')
    category = models.CharField(max_length=50, choices=category_choices, default='personal_growth')
    priority = models.CharField(max_length=50, choices=priority_choices, default='medium')
    due_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)      

    class Meta:
        ordering = ['-updated_at']  

    def __str__(self):
        return self.title
