from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    # Wybory dla typu kategorii
    TYPES = (
        ('income', 'Przychód'),
        ('expense', 'Wydatek'),
    )
    name = models.CharField(max_length=100, verbose_name="Nazwa kategorii")
    type = models.CharField(max_length=10, choices=TYPES, verbose_name="Typ")

    def __str__(self):
        # To sprawia, że w panelu admina zobaczysz nazwę, np. "Jedzenie (Wydatek)"
        return f"{self.name} ({self.get_type_display()})"

    class Meta:
        verbose_name_plural = "Categories"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Użytkownik")
    title = models.CharField(max_length=200, verbose_name="Tytuł")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Kwota")
    date = models.DateField(verbose_name="Data")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategoria")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.amount} zł"