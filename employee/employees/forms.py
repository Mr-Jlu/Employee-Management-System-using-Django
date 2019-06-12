from django import forms
from .models import Employees, Relationship, Contact
from employees.choices import *
from django_countries.data import COUNTRIES

class AddEmployeeForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(
        attrs={
            'placeholder': 'First name',
            'class': 'form-control',
        }))
    middle_name = forms.CharField(label='Middle name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Middle name',
            'class': 'form-control',
        }))
    last_name = forms.CharField(label='Last name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Last name',
            'class': 'form-control',
        }))
    full_name = forms.CharField(label='Full name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Full name',
            'class': 'form-control',
        }))

    employment_mode = forms.ChoiceField(choices=EMPLOYMENT_MODE, label="Mode Of Employment", initial='', widget=forms.Select(), required=True)

    bunit_id = forms.ChoiceField(choices=BUSINESS_UNIT, label="Business Unit", initial='', widget=forms.Select(), required=True)

    contact_no = forms.IntegerField(label='Contact Number', widget=forms.TextInput(
        attrs={
            'placeholder': 'Mobile Number',
            'class': 'form-control',
            'type': 'number',
        }))
    date_of_joining = forms.DateField(label='Date Of Joining', widget=forms.TextInput(
        attrs={
            'placeholder': 'Date Of Joining',
            'class': 'form-control',
            'type': 'date',
        }))
    # date_of_birth = forms.DateField(label='Date Of Joining', widget=forms.TextInput(
    #     attrs={
    #         'placeholder': 'Date Of Joining',
    #         'class': 'form-control',
    #         'type': 'date',
    #     }))
    age = forms.IntegerField(label='Age', widget=forms.TextInput(
        attrs={
            'placeholder': '',
            'class': 'form-control',
            'type': 'number',
        }))

    class Meta:
        model = Employees
        fields = [
            'user_type',
            'company_id',
            'bunit_id',
            'emp_code',
            'prefix',
            'first_name',
            'middle_name',
            'last_name',
            'full_name',
            'employment_mode',
            'reporting_manager',
            'role',
            'dept_id',
            'job_title',
            'position',
            'date_of_joining',
            'email',
            'contact_no',
            'age',
            'salary',
        ]

    def clean_national_identifier(self):
        national_identifier = self.cleaned_data.get('national_identifier')
        qs = Employees.objects.filter(national_identifier__iexact=national_identifier)
        if qs.exists():
            raise forms.ValidationError('This Employee is already Added before!')
        if int(national_identifier) <= 0:
            raise forms.ValidationError('National Identifier must be bigger than 0!')
        if len(str(national_identifier)) < 14 or len(str(national_identifier)) > 14:
            raise forms.ValidationError('National Identifier must be 14 number!')
        return int(national_identifier)

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        position = self.cleaned_data.get('position')
        if position == 'Employee':
            if int(salary) < 5000 or int(salary) > 10000:
                raise forms.ValidationError('salary for employee must be between 5000-10000')
        if position == 'Manager':
            if int(salary) < 10000 or int(salary) > 19000:
                raise forms.ValidationError('salary for manager must be between 10000-19000')
        if position == 'CEO':
            if int(salary) < 19000 or int(salary) > 25000:
                raise forms.ValidationError('salary for CEO must be between 19000-25000')
        return salary


class AddEmployeeContact(forms.ModelForm):
    pr_country = forms.ChoiceField(choices=sorted(COUNTRIES.items()))
    cr_country = forms.ChoiceField(choices=sorted(COUNTRIES.items()))

    class Meta:
        model = Contact
        fields = "__all__"



class UpdateEmployeeForm(forms.ModelForm):
    first_name = forms.CharField(label='First name', widget=forms.TextInput(
        attrs={
            'placeholder': 'First name',
            'class': 'form-control',
        }))
    middle_name = forms.CharField(label='Middle name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Middle name',
            'class': 'form-control',
        }))
    last_name = forms.CharField(label='Last name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Last name',
            'class': 'form-control',
        }))
    full_name = forms.CharField(label='Full name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Full name',
            'class': 'form-control',
        }))
    employment_mode = forms.ChoiceField(choices=EMPLOYMENT_MODE, label="Mode Of Employment", initial='',
                                        widget=forms.Select(), required=True)

    bunit_id = forms.ChoiceField(choices=BUSINESS_UNIT, label="Business Unit", initial='', widget=forms.Select(),
                                 required=True)

    contact_no = forms.IntegerField(label='Contact Number', widget=forms.TextInput(
        attrs={
            'placeholder': 'Mobile Number',
            'class': 'form-control',
            'type': 'number',
        }))

    class Meta:
        model = Employees
        fields = [
            'user_type',
            'company_id',
            'bunit_id',
            'emp_code',
            'prefix',
            'first_name',
            'middle_name',
            'last_name',
            'full_name',
            'employment_mode',
            'reporting_manager',
            'role',
            'dept_id',
            'job_title',
            'position',
            'date_of_joining',
            'email',
            'contact_no',
        ]

    def clean_national_identifier(self):
        national_identifier = self.cleaned_data.get('national_identifier')
        if int(national_identifier) <= 0:
            raise forms.ValidationError('National Identifier must be bigger than 0!')
        if len(str(national_identifier)) < 14 or len(str(national_identifier)) > 14:
            raise forms.ValidationError('National Identifier must be 14 number!')
        return int(national_identifier)


class UpdateSalaryForm(forms.ModelForm):
    position = forms.CharField(widget=forms.HiddenInput)
    salary = forms.IntegerField(label='Salary', widget=forms.TextInput(
        attrs={
            'placeholder': 'Salary',
            'class': 'form-control',
            'type': 'number',
        }))
    deduction = forms.IntegerField(label='Deduction', widget=forms.TextInput(
        attrs={
            'placeholder': 'Deduction',
            'class': 'form-control',
            'type': 'number',
        }))
    deduction_description = forms.CharField(label='Deduction Description', required=False, widget=forms.Textarea(
        attrs={
            'placeholder': 'Deduction Description',
            'class': 'form-control',
        }))
    earning = forms.IntegerField(label='Earning', widget=forms.TextInput(
        attrs={
            'placeholder': 'Earning',
            'class': 'form-control',
            'type': 'number',
        }))
    earning_description = forms.CharField(label='Earning Description', required=False, widget=forms.Textarea(
        attrs={
            'placeholder': 'Earning Description',
            'class': 'form-control',
        }))

    class Meta:
        model = Employees
        fields = [
            'position',
            'salary',
            'deduction',
            'deduction_description',
            'earning',
            'earning_description',
        ]

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        position = self.cleaned_data.get('position')
        if position == 'Employee':
            if int(salary) < 5000 or int(salary) > 10000:
                raise forms.ValidationError('salary for employee must be between 5000-10000')
        if position == 'Manager':
            if int(salary) < 10000 or int(salary) > 19000:
                raise forms.ValidationError('salary for manager must be between 10000-19000')
        if position == 'CEO':
            if int(salary) < 19000 or int(salary) > 25000:
                raise forms.ValidationError('salary for CEO must be between 19000-25000')
        return salary


class AddRelationForm(forms.ModelForm):
    name = forms.CharField(label='Name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Name',
            'class': 'form-control',
        }))
    age = forms.IntegerField(label='Age', widget=forms.TextInput(
        attrs={
            'placeholder': 'Age',
            'class': 'form-control',
            'type': 'number',
        }))
    date_of_birth = forms.DateField(label='Date Of Birth', widget=forms.TextInput(
        attrs={
            'placeholder': 'Date Of Birth',
            'class': 'form-control',
            'type': 'date',
        }))

    class Meta:
        model = Relationship
        fields = [
            'relationship_type',
            'name',
            'age',
            'date_of_birth',
        ]

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if int(age) <= 0:
            raise forms.ValidationError('Age must be bigger than 0!')
        return age
