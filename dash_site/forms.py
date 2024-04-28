# Forms
from django import forms
from .models import IncomeModel, ExpenseModel, ClientModel
import datetime

# Form to Insert New Income
class IncomeForm(forms.ModelForm):
    
    # Convert the flat list of unit_id values into a list of tuples
    unit_id_choices = IncomeModel.objects.values_list('unit_id', flat=True).distinct()
    unit_id_choices = [(unit_id, unit_id) for unit_id in unit_id_choices]
    
    income_unit_id = forms.ChoiceField(choices=unit_id_choices, label='Unit ID', required=True)
    income_amt = forms.DecimalField(initial=0.00, label='Income Amount', required=True)
    income_date = forms.DateField(widget=forms.SelectDateWidget(), initial=datetime.date.today(), label='Date', required=True)
    income_month = forms.IntegerField(initial=datetime.date.today().month, label='Month #', required=False)
    income_year = forms.IntegerField(initial=datetime.date.today().year, label='Year', required=False)

    class Meta:
        model = IncomeModel
        fields = ['income_unit_id', 'income_amt', 'income_date', 'income_month', 'income_year']
        exclude = ['income_id']

    def __init__(self, *args, **kwargs):
        self.readonly = kwargs.pop('readonly', False)  # Check if readonly is specified
        super(IncomeForm, self).__init__(*args, **kwargs)
        if self.readonly:
            self.make_readonly()

    def make_readonly(self):
        for field_name, field in self.fields.items():
            field.widget.attrs['readonly'] = True


# Form to Insert New Expense
class ExpenseForm(forms.ModelForm):

    # Convert the flat list of unit_id values into a list of tuples
    unit_id_choices = ExpenseModel.objects.values_list('unit_id', flat=True).distinct()
    unit_id_choices = [(unit_id, unit_id) for unit_id in unit_id_choices]

    exp_unit_id = forms.ChoiceField(choices=unit_id_choices, label='Unit ID', required=True)
    exp_name = forms.CharField(max_length=255, initial='Maintenance Supplies', label='Expense Name', required=False)
    exp_amt = forms.DecimalField(initial=0.00, label='Expense Amount', required=True)
    exp_date = forms.DateField(widget=forms.SelectDateWidget(), initial=datetime.date.today(), label='Date', required=True)
    exp_rct = forms.FileField(label='Receipt File', required=False)
    exp_bldg = forms.ChoiceField(widget=forms.RadioSelect,  # Radio buttons for selection
        choices=((1, 'Yes'), (0, 'No')),  # Radio choices
        label='Applies to Entire Building', required=False)
    
    class Meta:
        model = ExpenseModel
        fields = ['exp_unit_id', 'exp_name', 'exp_amt', 'exp_date', 'exp_rct', 'exp_bldg']
        exclude = ['exp_id']

    
    def __init__(self, *args, **kwargs):
        self.readonly = kwargs.pop('readonly', False)  # Check if readonly is specified
        super(ExpenseForm, self).__init__(*args, **kwargs)
        if self.readonly:
            self.make_readonly()

    def make_readonly(self):
        for field_name, field in self.fields.items():
            field.widget.attrs['readonly'] = True