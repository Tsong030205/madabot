from django.db import models

class FAQ(models.Model):
    LANGUAGE_CHOICES = [
        ('fr', 'Français'),
        ('mg', 'Malgache'),
    ]
    question = models.CharField(max_length=255)
    answer = models.TextField()
    keywords = models.CharField(max_length=255)  # Mots-clés séparés par des virgules
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='fr')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question} ({self.language})"
    
class Reservation(models.Model):
    LANGUAGE_CHOICES = [
        ('fr', 'Français'),
        ('mg', 'Malgache'),
    ]
    destination = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    num_people = models.PositiveIntegerField()
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='fr')
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"Réservation pour {self.destination} ({self.language})"
    
class Destination(models.Model):
    LANGUAGE_CHOICES = [
        ('fr', 'Français'),
        ('mg', 'Malgache'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    activities = models.TextField()
    image = models.ImageField(upload_to='destinations/', null=True, blank=True)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='fr')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.language})"
    
class BudgetEstimate(models.Model):
    LANGUAGE_CHOICES = [
        ('fr', 'Français'),
        ('mg', 'Malgache'),
    ]
    destination = models.CharField(max_length=100)
    duration_days = models.PositiveIntegerField()
    num_people = models.PositiveIntegerField()
    accommodation_type = models.CharField(max_length=20, choices=[
        ('economique', 'Économique'),
        ('standard', 'Standard'),
        ('luxe', 'Luxe'),
    ])
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='fr')
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Estimation pour {self.destination} ({self.language})"