from django.db import models

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    assigned_to = models.ForeignKey(
        'user.CustomUser',
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True,
        blank=True
    )

    due_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('IN_PROGRESS', 'In Progress'),
            ('COMPLETED', 'Completed'),
        ],
        default='PENDING'
    )   
    completion_report = models.TextField(null=True, blank=True)
    worked_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title