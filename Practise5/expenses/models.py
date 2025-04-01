from django.db import models
from django.contrib.auth.models import User

# 1. Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# 2. Expense Model
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.description} - ${self.amount}"

    class Meta:
        ordering = ['-date']

# 3. GroupExpense Model
class GroupExpense(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    users = models.ManyToManyField(User)

    def split_expense(self):
        user_count = self.users.count()
        return self.amount / user_count if user_count else 0
