from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
import csv
from matplotlib import pyplot as plt
from io import BytesIO
import base64
from .models import ExpenseModel, IncomeModel, ClientModel, BldgExpYrModel, BldgIncomeYrModel, UnitExpYrModel, UnitIncomeYrModel
from .forms import IncomeForm, ExpenseForm
from dotenv import load_dotenv
load_dotenv()


# Get the current date
current_date = datetime.now()

# Set default values for year and month
default_year = current_date.year
default_month = current_date.month


# Home Page
def index(request):
    return render(request, "index.html")

# Profile View Portal
@login_required
def profile_view(request):
    user = request.user
    if user.is_staff:
        client_all = ClientModel.objects.order_by("unit_id")
        expense_all = ExpenseModel.objects.order_by("-exp_date")
        income_all = IncomeModel.objects.order_by("-income_date")

        context = {
            "client_all": client_all,
            "expense_all": expense_all, 
            "income_all": income_all,
            "default_year": default_year,
            "default_month": default_month,
            "user": user,
        }
        return render(request, 'dashboard.html', context)
    else:
        return render(request, 'index.html', {'user': user})


def get_expense_graph(expenses):
    # Format data for Matplotlib
    dates = [expense.exp_date for expense in expenses]
    amounts = [expense.exp_amt for expense in expenses]
    
    # Generate Matplotlib graph
    plt.plot(dates, amounts, marker='o', linestyle='-')
    plt.xlabel('Date')
    plt.ylabel('Expense Amount')
    plt.title('Expense Trends Over Time')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    
    # Convert x-axis dates to a more readable format (optional)
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
    
    # Ensure that there's enough space for x-axis labels
    plt.tight_layout()
    
    # Save the Matplotlib graph as a PNG image (optional)
    plt.savefig('expense_trends.png')
    
    # Convert the Matplotlib graph to a base64-encoded string (optional)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode()
    buffer.close()

    return img_str

# Manager Dashboard
@login_required
def dashboard(request):
    client_all = ClientModel.objects.order_by("unit_id")
    expense_all = ExpenseModel.objects.order_by("-exp_date")
    income_all = IncomeModel.objects.order_by("-income_date")
    expense_graph = get_expense_graph(expense_all)
    
    context = {
        "client_all": client_all,
        "expense_all": expense_all,
        "expense_graph": expense_graph,
        "income_all": income_all,
        "default_year": default_year,
        "default_month": default_month
    }
    
    return render(request, "dashboard.html", context)


# ALL FINANCES PAGE
# Retrieve financial data for specific month + year
def get_finance_month(yr, month):

    # Expense data for month + year
    expense_data = ExpenseModel.objects.filter(
        exp_date__year=yr,
        exp_date__month=month
    )
    
    # Income data for month + year
    income_data = IncomeModel.objects.filter(
        income_year=yr, 
        income_month=month
    )

    finance_month_data = {
        "expense_data": expense_data, 
        "income_data": income_data
    }

    return finance_month_data

# Render financial data for specific month + year
@login_required
def finance_month(request, yr=None, month=None):
    
    # Get distinct lists of available year and month choices for dropdown menus
    available_years = sorted(list(IncomeModel.objects.values_list('income_year', flat=True).distinct()))
    available_months = sorted(list(IncomeModel.objects.values_list('income_month', flat=True).distinct()))

    # Retrieve income and expenses data for specific month + year
    finance_month_data = get_finance_month(yr, month)

    # Insert Income Form Instance
    add_income_form = IncomeForm()

    # Update Income Form Instance
    update_income_form = IncomeForm()

    # Delete Income Form Instance
    delete_income_form = IncomeForm(readonly=True)
    
    # Insert Expense Form Instance
    add_expense_form = ExpenseForm()

    # Update Expense Form Instance
    update_expense_form = ExpenseForm()

    # Delete Expense From Instance
    delete_expense_form = ExpenseForm(readonly=True)
    
    context = {
        'available_years': available_years,
        'available_months': available_months,
        "default_year": default_year,
        "default_month": default_month,
        'selected_year': int(yr) if yr else default_year,
        'selected_month': int(month) if month else default_month,
        "finance_month_data": finance_month_data,
        "add_income_form": add_income_form,
        "update_income_form": update_income_form,
        "delete_income_form": delete_income_form,
        "add_expense_form": add_expense_form,
        "update_expense_form": update_expense_form,
        "delete_expense_form": delete_expense_form,
        "user": request.user,
    }

    return render(request, "finance_month.html", context)


# FINANCES BY BUILDING + YEAR
# Retrive yearly financial data for specific building
def get_finance_building(yr):
    
     # Expense data for month + year
    expense_data = BldgExpYrModel.objects.filter(
        year=yr
        ).values("unit_id", "jan", "feb", "mar", "apr", "may",
                "jun", "jul", "aug", "sep", "oct", 
                "nov", "dec", "year_total")
    
    # Income data for month + year
    income_data = BldgIncomeYrModel.objects.filter(
        year=yr
        ).values("unit_id", "jan", "feb", "mar", "apr", "may",
                "jun", "jul", "aug", "sep", "oct", 
                "nov", "dec", "year_total")

    finance_building = {
        "expense_data": expense_data, 
        "income_data": income_data
    }
    
    return finance_building


# FINANCES BY APARTMENT + YEAR
# Retrive yearly financial data for each apartment
def get_finance_unit(yr):

     # Expense data for month + year
    expense_data = UnitExpYrModel.objects.filter(
        year=yr
        ).values("unit_id", "jan", "feb", "mar", "apr", "may",
                "jun", "jul", "aug", "sep", "oct", 
                "nov", "dec", "year_total")
    
    # Income data for month + year
    income_data = UnitIncomeYrModel.objects.filter(
        year=yr
        ).values("unit_id", "jan", "feb", "mar", "apr", "may",
                "jun", "jul", "aug", "sep", "oct", 
                "nov", "dec", "year_total")
    
    finance_unit = {
        "expense_data": expense_data, 
        "income_data": income_data
    }
    return finance_unit


# Render yearly financial data for selected unit (building or apartment)
@login_required
def finance_unit(request, yr=None):
    available_years = sorted(list(IncomeModel.objects.values_list('income_year', flat=True).distinct()))

    finance_unit = get_finance_unit(yr)
    finance_building = get_finance_building(yr)

    context = {
        "available_years": available_years,
        "default_year": default_year,
        "default_month": default_month,
        "finance_unit": finance_unit,
        "finance_building": finance_building,
        "selected_year": int(yr) if yr else default_year,
        "user": request.user,
    }

    return render(request, "finance_unit.html", context)


# EXPORT DATA TO CSV
def export_to_csv(request):
    
    # Get export_id
    export_id = request.GET.get('export_id')
    
    # Get year
    yr = request.GET.get('yr')
    
    # Switch between export ID choices
    # BLDG INCOME
    if export_id == "bldg_income":
        # Income data for bldg + year
        export_data = BldgIncomeYrModel.objects.filter(
            year=yr
        ).values("unit_id", "jan", "feb", "mar", "apr", "may",
                "jun", "jul", "aug", "sep", "oct", 
                "nov", "dec", "year_total")
    
    # BLDG EXPENSES
    elif export_id == "bldg_expenses":
        # Expense data for month + year
        export_data = BldgExpYrModel.objects.filter(
            year=yr
        ).values("unit_id", "jan", "feb", "mar", "apr", "may",
                "jun", "jul", "aug", "sep", "oct", 
                "nov", "dec", "year_total")
    
    # UNIT INCOME
    elif export_id == "unit_income":
        # Income data for month + year
        export_data = UnitIncomeYrModel.objects.filter(
            year=yr
        ).values("unit_id", "jan", "feb", "mar", "apr", "may",
                "jun", "jul", "aug", "sep", "oct", 
                "nov", "dec", "year_total")
       
    # APARTMENT EXPENSES
    elif export_id == "unit_expenses":
        # Expense data for month + year
        export_data = UnitExpYrModel.objects.filter(
            year=yr
        ).values("unit_id", "jan", "feb", "mar", "apr", "may",
                "jun", "jul", "aug", "sep", "oct", 
                "nov", "dec", "year_total")
    
    # CSV Response
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{export_id}_{yr}.csv"'

    # Write header to CSV
    writer = csv.writer(response)
    writer.writerow(["Unit", "January", "February", "March", "April", 
                     "May", "June", "July", "August", "September", 
                     "October", "November", "December", "Year Total"])  # Header row

    # Write export_data to CSV
    for item in export_data:
        writer.writerow([item['unit_id'], item['jan'], item['feb'], item['mar'], item['apr'],
                         item['may'], item['jun'], item['jul'], item['aug'], item['sep'],
                         item['oct'], item['nov'], item['dec'], item['year_total']])  # Data rows

    return response


# FORM: Insert New Income Payment
def insert_new_income(request):
    if request.method == 'POST':
        add_income_form = IncomeForm(request.POST)
        if add_income_form.is_valid():
            
            # Extract and clean data from the form
            unit_id = add_income_form.cleaned_data['income_unit_id']
            income_amt = add_income_form.cleaned_data['income_amt']
            income_date = add_income_form.cleaned_data['income_date']
            income_month = add_income_form.cleaned_data['income_month']
            income_year = add_income_form.cleaned_data['income_year']

            try:
                IncomeModel.objects.create(unit_id=unit_id, income_amt=income_amt, income_date=income_date, income_month=income_month, income_year=income_year)
                
            except IntegrityError:
                return HttpResponse("An error occurred while inserting data.")
                
            return redirect('finance_month')  # Redirect to the updated finances_all page
    else:
        add_income_form = IncomeForm()
    
    return render(request, 'finance_month.html', {'add_income_form': add_income_form})


# FORM: Update Income Payment
def update_income(request, income_id):
    income_row = get_object_or_404(IncomeModel, pk=income_id)
    if request.method == 'POST':
        update_income_form = IncomeForm(request.POST, instance=income_row)
        if update_income_form.is_valid():
            try:
                update_income_form.save()
                
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}.")
                
            return redirect('finance_month')  # Redirect to the updated finances_all page
    else:
        update_income_form = IncomeForm()
    
    return render(request, 'finance_month.html', {'update_income_form': update_income_form})


# FORM: Delete Income Payment
def delete_income(request, income_id):
    income_row = get_object_or_404(IncomeModel, pk=income_id)
    if request.method == 'POST':
            try:
                income_row.delete()
                return redirect('finance_month')  # Redirect to the updated finance_month page

            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}.")
    
    return render(request, 'finance_month.html')


# FORM: Insert New Expense
def insert_new_expense(request):
    if request.method == 'POST':
        add_expense_form = ExpenseForm(request.POST)
        if add_expense_form.is_valid():
            
            # Extract and clean data from the form
            unit_id = add_expense_form.cleaned_data['exp_unit_id']
            exp_name = add_expense_form.cleaned_data['exp_name']
            exp_amt = add_expense_form.cleaned_data['exp_amt']
            exp_date = add_expense_form.cleaned_data['exp_date']
            exp_rct = add_expense_form.cleaned_data['exp_rct']
            exp_bldg = add_expense_form.cleaned_data['exp_bldg']
            
            try:
                ExpenseModel.objects.create(unit_id=unit_id, exp_name=exp_name, exp_amt=exp_amt, exp_date=exp_date, exp_rct=exp_rct, exp_bldg=exp_bldg)

            except IntegrityError:
                return HttpResponse("An error occurred while inserting data.")
                
            return redirect('finance_month')  # Redirect to the updated finances_all page
    else:
        add_expense_form = ExpenseForm()
    
    return render(request, 'finance_month.html', {'add_expense_form': add_expense_form})


# FORM: Update Expense Payment
def update_expense(request, expense_id):
    expense_row = get_object_or_404(ExpenseModel, pk=expense_id)
    if request.method == 'POST':
        update_expense_form = ExpenseForm(request.POST, instance=expense_row)
        if update_expense_form.is_valid():
            try:
                update_expense_form.save()
                
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}.")
                
            return redirect('finance_month')  # Redirect to the updated finances_all page
    else:
        update_expense_form = IncomeForm()
    
    return render(request, 'finance_month.html', {'update_expense_form': update_expense_form})


# FORM: Delete Expense
def delete_expense(request, income_id):
    expense_row = get_object_or_404(ExpenseModel, pk=income_id)
    if request.method == 'POST':
            try:
                expense_row.delete()
                return redirect('finance_month')  # Redirect to the updated finance_month page

            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}.")
    
    return render(request, 'finance_month.html')
