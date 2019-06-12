from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from employees.choices import *

class Employees(models.Model):
    # profile_pic = models.ImageField(upload_to="profiles/", default="profiles/None/no-img.jpg")
    user_type = models.CharField(choices=USER_TYPE, max_length=50)
    company_id = models.CharField(choices=COMPANY, max_length=50, default=1)
    bunit_id = models.CharField(choices=BUSINESS_UNIT, max_length=100, default=1)
    emp_code = models.CharField(max_length=50)
    prefix = models.CharField(choices=PREFIX, max_length=20)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=500)
    employment_mode = models.CharField(choices=EMPLOYMENT_MODE, max_length=20)
    date_of_joining = models.DateField()
    reporting_manager = models.CharField(max_length=100)
    dept_id = models.CharField(choices=DEPARTMENTS_TYPE, max_length=20)
    role = models.CharField(choices=ROLE, max_length=20)
    job_title = models.CharField(choices=JOB_TITLE, max_length=50)
    email = models.EmailField(max_length=255)
    contact_no = models.BigIntegerField()
    hod_of_dept = models.CharField(default=0, max_length=20)
    added_by = models.IntegerField(null=True)
    added = models.DateTimeField(auto_now_add=True)
    updated_by = models.PositiveIntegerField(null=True)
    updated = models.DateTimeField(auto_now=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(choices=GENDER_CHOICES, max_length=25)
    position = models.CharField(choices=POSITION_CHOICES, max_length=25)
    nationality = models.CharField(max_length=255)
    marital_status = models.CharField(choices=MARITAL_STATUS_CHOICES, max_length=25)
    salary = models.PositiveIntegerField()
    deduction = models.PositiveIntegerField(default=0, null=True)
    earning = models.PositiveIntegerField(default=0, null=True)
    deduction_description = models.TextField(null=True)
    earning_description = models.TextField(null=True)
    activated = models.BooleanField(default=True)
    freeze = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('employees:detail', kwargs={'pk': self.pk})


class Contact(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    personal_contact_no = models.BigIntegerField()
    personal_email = models.EmailField(max_length=255)
    pr_street_address = models.CharField(max_length=1000)
    pr_pincode = models.PositiveIntegerField()
    pr_country = models.CharField(max_length=100)
    pr_states = models.CharField(max_length=100)
    pr_city = models.CharField(max_length=100)
    cr_street_address = models.CharField(max_length=1000)
    cr_pincode = models.PositiveIntegerField()
    cr_country = models.CharField(max_length=100)
    cr_states = models.CharField(max_length=100)
    emg_name = models.CharField(max_length=255)
    emg_email = models.EmailField()
    emg_contact_no = models.BigIntegerField()

    def get_absolute_url(self):
        return reverse('employees:contacts', kwargs={'pk': self.pk})


class Relationship(models.Model):
    RELATIONSHIP_TYPE_CHOICES = [
        ('wife', 'Wife'),
        ('child', 'Child'),
        ('husband', 'Husband'),
    ]
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    relationship_type = models.CharField(choices=RELATIONSHIP_TYPE_CHOICES, max_length=25)
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    date_of_birth = models.DateField()
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.relationship_type


def post_save_employee_receiver(sender, instance, created, *args, **kwargs):
    if created:
        qs = Employees.objects.filter(id=instance.id, national_identifier=instance.national_identifier)
        if qs.exists() and qs.count() == 1:
            employee = qs.first()
            position = employee.position
            if position == 'Employee':
                deduction = (employee.salary * 7.5) / 100
                employee.deduction = deduction
                employee.save()
            if position == 'Manager':
                deduction = (employee.salary * 12) / 100
                employee.deduction = deduction
                employee.save()
            if position == 'CEO':
                deduction = (employee.salary * 15) / 100
                employee.deduction = deduction
                employee.save()


# post_save.connect(post_save_employee_receiver, sender=Employees)