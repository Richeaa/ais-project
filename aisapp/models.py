from django.db import models

class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username}"
    
    class Meta:
        db_table = 'profile'
        managed = False

class Form(models.Model):
    form_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, db_column='user_id', related_name='forms')
    raw_material = models.CharField(max_length=100, db_column='title')
    submitted_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} request {self.raw_material} at {self.submitted_at} for {self.quantity}" 
    
    class Meta:
        db_table = 'form'
        managed = False

class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, db_column='user_id', related_name='reports')
    title = models.CharField(max_length=150)
    content = models.TextField()
    file = models.FileField(upload_to='uploads/reports/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} report {self.title} at {self.submitted_at}"
    
    class Meta:
        db_table = 'report'
        managed = False
        
class Product(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'product'
        managed = False

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'inventory'
        managed = False

class ProductionSchedule(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    start_date = models.DateField()
    estimated_end_date = models.DateField()
    priority = models.IntegerField()

    class Meta:
        db_table = 'production_schedule'
        managed = False

class ProductionIssue(models.Model):
    issue_time = models.DateTimeField(auto_now_add=True)
    issue_type = models.CharField(max_length=50, choices=[('Machine', 'Machine'), ('Material', 'Material'), ('Human', 'Human Error')])
    description = models.TextField()

    class Meta:
        db_table = 'production_issue'
        managed = False
