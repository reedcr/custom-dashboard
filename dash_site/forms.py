# Forms
from django import forms
from .models import IncomeModel, ExpenseModel, ClientModel
import datetime

# Form to Insert New Income
class IncomeForm(forms.ModelForm):
    
    # Convert the flat list of unit_id values into a list of tuples
    unit_id_list = sorted(list(IncomeModel.objects.values_list('unit_id', flat=True).distinct()))
    unit_id_choices = [(unit_id, unit_id) for unit_id in unit_id_list]
    
    income_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    unit_id = forms.ChoiceField(choices=unit_id_choices, label='Unit ID', required=True)
    income_amt = forms.DecimalField(initial=0.00, label='Income Amount', required=True)
    income_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=datetime.date.today(), label='Date', required=True)
    income_month = forms.IntegerField(initial=datetime.date.today().month, label='Month #', required=False)
    income_year = forms.IntegerField(initial=datetime.date.today().year, label='Year', required=False)

    class Meta:
        model = IncomeModel
        fields = ['income_id', 'unit_id', 'income_amt', 'income_date', 'income_month', 'income_year']
        exclude = []

    def __init__(self, *args, **kwargs):
        self.readonly = kwargs.pop('readonly', False)  # Check if readonly is specified
        super(IncomeForm, self).__init__(*args, **kwargs)
        self.fields['income_id'].widget.attrs.update({'id': 'form_income_id', 'class': 'crud-income-field'})
        self.fields['unit_id'].widget.attrs.update({'id': 'form_income_unit_id', 'class': 'crud-income-field'})
        self.fields['income_amt'].widget.attrs.update({'id': 'form_income_amt', 'class': 'crud-income-field'})
        self.fields['income_date'].widget.attrs.update({'id': 'form_income_date', 'class': 'crud-income-field'})
        self.fields['income_month'].widget.attrs.update({'id': 'form_income_month', 'class': 'crud-income-field'})
        self.fields['income_year'].widget.attrs.update({'id': 'form_income_year', 'class': 'crud-income-field'})

    def getUnitChoices(self):
        return self.unit_id_choices
        

    # def make_readonly(self):
    #     for field in self.fields.items():
    #         field.widget.attrs['readonly'] = True


# Form to Insert New Expense
class ExpenseForm(forms.ModelForm):

    # Convert the flat list of unit_id values into a list of tuples
    unit_id_choices = ExpenseModel.objects.values_list('unit_id', flat=True).distinct()
    unit_id_choices = [(unit_id, unit_id) for unit_id in unit_id_choices]

    expense_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    unit_id = forms.ChoiceField(choices=unit_id_choices, label='Unit ID', required=True)
    expense_name = forms.CharField(max_length=255, initial='Maintenance Supplies', label='Expense Name', required=False)
    expense_amt = forms.DecimalField(initial=0.00, label='Expense Amount', required=True)
    expense_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=datetime.date.today(), label='Date', required=True)
    expense_bldg = forms.ChoiceField(choices=[(1, 'Yes'),(0, 'No')], label='Applies to Entire Building', required=False)
    expense_receipt = forms.FileField(label='Receipt File', required=False)
    
    class Meta:
        model = ExpenseModel
        fields = ['expense_id', 'unit_id', 'expense_name', 'expense_amt', 'expense_date', 'expense_bldg', 'expense_receipt']
        exclude = []

    
    def __init__(self, *args, **kwargs):
        self.readonly = kwargs.pop('readonly', False)  # Check if readonly is specified
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['expense_id'].widget.attrs.update({'id': 'form_expense_id', 'class': 'crud-expense-field'})
        self.fields['unit_id'].widget.attrs.update({'id': 'form_expense_unit_id', 'class': 'crud-expense-field'})
        self.fields['expense_name'].widget.attrs.update({'id': 'form_expense_name', 'class': 'crud-expense-field'})
        self.fields['expense_amt'].widget.attrs.update({'id': 'form_expense_amt', 'class': 'crud-expense-field'})
        self.fields['expense_date'].widget.attrs.update({'id': 'form_expense_date', 'class': 'crud-expense-field'})
        self.fields['expense_bldg'].widget.attrs.update({'id': 'form_expense_bldg', 'class': 'crud-expense-field'})
        self.fields['expense_receipt'].widget.attrs.update({'id': 'form_expense_receipt', 'class': 'crud-expense-field'})
        
    # if self.readonly:
    #     self.make_readonly()

    # def make_readonly(self):
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['readonly'] = True