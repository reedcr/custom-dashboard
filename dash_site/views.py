import os
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import IntegrityError
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

app_name = os.getenv('BUSINESS_NAME', 'Finance Manager')

"""
STATS FUNCTIONS
"""

# Retrieve financial data for specific month + year
def get_finance_month(yr, month):

    # Expense data for month + year
    expense_data = ExpenseModel.objects.filter(
        expense_date__year=yr,
        expense_date__month=month
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


# Generate Graph of Expenses over Time
def get_expense_time_graph(expenses):
    # Format data for Matplotlib
    dates = [expense.expense_date for expense in expenses]
    amounts = [expense.expense_amt for expense in expenses]
    
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


# GET CONTEXT INFO FOR FINANCE MONTH PAGE & CRUD FORM ENDPOINTS
def get_finance_month_context(request, yr=None, month=None):
     # Get distinct lists of available year and month choices for dropdown menus
    available_years = sorted(list(IncomeModel.objects.values_list('income_year', flat=True).distinct()))
    available_months = sorted(list(IncomeModel.objects.values_list('income_month', flat=True).distinct()))
    
    # unit_id_list = sorted(list(IncomeModel.objects.values_list('unit_id', flat=True).distinct()))
    # unit_id_choices = [(unit_id, unit_id) for unit_id in unit_id_list]
    unit_choices = IncomeForm.unit_id_list

    # Retrieve income and expenses data for specific month + year
    finance_month_data = get_finance_month(yr, month)

    # Add Income Form Instance
    crud_income_form = IncomeForm()
    crud_expense_form = ExpenseForm()
    
    context = {
        'available_years': available_years,
        'available_months': available_months,
        'unit_choices': unit_choices,
        "default_year": default_year,
        "default_month": default_month,
        'selected_year': int(yr) if yr else default_year,
        'selected_month': int(month) if month else default_month,
        "finance_month_data": finance_month_data,
        "crud_income_form": crud_income_form,
        "crud_expense_form": crud_expense_form,
        "app_name": app_name,
        "user": request.user,
    }
    
    return context



"""
ENDPOINTS
"""

# Insert New Income Payment
def submit_add_income(request, yr=None, month=None):
    context = get_finance_month_context(request, 
                                        int(yr) if yr else default_year, 
                                        int(month) if month else default_month)

    if request.method == 'POST':
        add_income_form = IncomeForm(request.POST)
        if add_income_form.is_valid():
            
            # Extract and clean data from the form
            unit_id = add_income_form.cleaned_data['unit_id']
            income_amt = add_income_form.cleaned_data['income_amt']
            income_date = add_income_form.cleaned_data['income_date']
            income_month = add_income_form.cleaned_data['income_month']
            income_year = add_income_form.cleaned_data['income_year']

            try:
                IncomeModel.objects.create(unit_id=unit_id, income_amt=income_amt, 
                                           income_date=income_date, income_month=income_month, 
                                           income_year=income_year)
                
            except IntegrityError:
                return HttpResponse("An error occurred while inserting data.")
                
            return redirect('finance_month', 
                            yr=int(yr) if yr else default_year, 
                            month=int(month) if month else default_month)  # Redirect to the updated page
    else:
        add_income_form = IncomeForm()
        context["crud_income_form"] = add_income_form

    return render(request, 'managers/finance_month.html', context)


# Update Income Payment
def submit_update_income(request, income_id, yr=None, month=None):
    context = get_finance_month_context(request, 
                                        int(yr) if yr else default_year, 
                                        int(month) if month else default_month)

    income_row = get_object_or_404(IncomeModel, pk=income_id)
    
    if request.method == 'POST':
        update_income_form = IncomeForm(request.POST, instance=income_row)
        
        if update_income_form.is_valid():
           
            try:
                update_income_form.save()
                
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}.")

            return redirect('finance_month', yr=int(yr) if yr else default_year, 
                            month=int(month) if month else default_month)  # Redirect to the updated page

    else:        
        update_income_form = IncomeForm(instance=income_row)
        context["crud_income_form"] = update_income_form

    
    return render(request, 'managers/finance_month.html', context)


# Delete Income Payment
def submit_delete_income(request, income_id, yr=None, month=None):
    context = get_finance_month_context(request, 
                                        int(yr) if yr else default_year, 
                                        int(month) if month else default_month)

    income_row = get_object_or_404(IncomeModel, pk=income_id)
    if request.method == 'POST':
            try:
                income_row.delete()

            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}.")
            
            return redirect('finance_month', yr=int(yr) if yr else default_year, 
                            month=int(month) if month else default_month)  # Redirect to the updated finance_month page
    
    return render(request, 'managers/finance_month.html', context)


# Insert New Expense
def submit_add_expense(request, yr=None, month=None):
    context = get_finance_month_context(request, 
                                        int(yr) if yr else default_year, 
                                        int(month) if month else default_month)

    if request.method == 'POST':
        add_expense_form = ExpenseForm(request.POST, request.FILES)
        
        if add_expense_form.is_valid():
            
            # Extract and clean data from the form
            unit_id = add_expense_form.cleaned_data['unit_id']
            expense_name = add_expense_form.cleaned_data['expense_name']
            expense_amt = add_expense_form.cleaned_data['expense_amt']
            expense_date = add_expense_form.cleaned_data['expense_date']
            expense_bldg = add_expense_form.cleaned_data['expense_bldg']
            expense_receipt = add_expense_form.cleaned_data['expense_receipt']
            
            try:
                ExpenseModel.objects.create(unit_id=unit_id, expense_name=expense_name, 
                                            expense_amt=expense_amt, expense_date=expense_date, 
                                            expense_bldg=expense_bldg, expense_receipt=expense_receipt)

            except IntegrityError:
                return HttpResponse("An error occurred while inserting data.")
                
            return redirect('finance_month', yr=int(yr) if yr else default_year, 
                            month=int(month) if month else default_month)  # Redirect to the updated finances_all page
    else:
        add_expense_form = ExpenseForm()
        context["crud-expense-form"] = add_expense_form
    
    return render(request, 'managers/finance_month.html', context)


# Update Expense Payment
def submit_update_expense(request, expense_id, yr=None, month=None):
    # Get context for rendering finance_month page
    context = get_finance_month_context(request, 
                                        int(yr) if yr else default_year, 
                                        int(month) if month else default_month)

    # Get original data from the updated row
    expense_row = get_object_or_404(ExpenseModel, pk=expense_id)
    
    # Handle POST request
    if request.method == 'POST':

        # Get updated row contents
        update_expense_form = ExpenseForm(request.POST, request.FILES, instance=expense_row)
        
        # Validate form
        if update_expense_form.is_valid():

            try:
                # Get form data as object without committing
                update_expense_obj = update_expense_form.save(commit=False)

                # Check if new receipt file has been uploaded
                # Set form object's expense_receipt field to new file if exists
                if 'expense_receipt' in request.FILES and request.FILES['expense_receipt']:
                    update_expense_obj.expense_receipt = request.FILES['expense_receipt']
                    
                # Set form object's expense_receipt field to current file 
                # if there is no new upload 
                else:
                    update_expense_obj.expense_receipt = expense_row.expense_receipt
                               
                # Save form
                update_expense_obj.save()

            # Handle errors
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}.")
                
            return redirect('finance_month', yr=int(yr) if yr else default_year, 
                            month=int(month) if month else default_month)  # Redirect to the updated finances_all page
    
    # Handle GET requests
    else:
        update_expense_form = IncomeForm()
        context["crud-expense-form"] = update_expense_form
    
    # Render finance_month page
    return render(request, 'managers/finance_month.html', context)


# Delete Expense
def submit_delete_expense(request, expense_id, yr=None, month=None):
    context = get_finance_month_context(request, 
                                        int(yr) if yr else default_year, 
                                        int(month) if month else default_month)

    expense_row = get_object_or_404(ExpenseModel, pk=expense_id)
    
    if request.method == 'POST':
            try:
                expense_row.delete()
                return redirect('finance_month', yr=int(yr) if yr else default_year, 
                            month=int(month) if month else default_month)  # Redirect to the updated finance_month page

            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}.")
    
    return render(request, 'managers/finance_month.html', context)




"""
VIEWS
"""

# Home Page
def index(request):

    context = {
        "default_year": default_year,
        "default_month": default_month,
        "app_name": app_name,
    }

    return render(request, "index.html", context)


# Contact Page
def contact(request):

    context = {
        "default_year": default_year,
        "default_month": default_month,
        "app_name": app_name,
    }

    return render(request, "contact.html", context)


# Dashboard View Portal
@login_required
def profile_view(request):
    user = request.user
    if user.is_staff:
        client_all = ClientModel.objects.order_by("unit_id")
        expense_all = ExpenseModel.objects.order_by("-expense_date")
        income_all = IncomeModel.objects.order_by("-income_date")
        expense_graph = get_expense_time_graph(expense_all)

        context = {
            "client_all": client_all,
            "expense_all": expense_all, 
            "income_all": income_all,
            "expense_graph": expense_graph,
            "default_year": default_year,
            "default_month": default_month,
            "user": user,
            "app_name": app_name,
        }
        return render(request, 'managers/dashboard_manager.html', context)
    else:

        context = {
            "default_year": default_year,
            "default_month": default_month,
            "user": user,
            "app_name": app_name,
        }
        return render(request, 'tenants/dashboard_tenant.html', context)



"""
MANAGER VIEWS
"""
# Manager Dashboard
@login_required
def dashboard_manager(request):
    client_all = ClientModel.objects.order_by("unit_id")
    expense_all = ExpenseModel.objects.order_by("-expense_date")
    income_all = IncomeModel.objects.order_by("-income_date")
    expense_graph = get_expense_time_graph(expense_all)
    
    context = {
        "client_all": client_all,
        "expense_all": expense_all,
        "expense_graph": expense_graph,
        "income_all": income_all,
        "default_year": default_year,
        "default_month": default_month,
        "app_name": app_name,
    }
    
    return render(request, 'managers/dashboard_manager.html', context)



# FINANCES BY MONTH + YEAR
# financial data for specific month + year
@login_required
def finance_month(request, yr=None, month=None):
    context = get_finance_month_context(request, 
                                        int(yr) if yr else default_year, 
                                        int(month) if month else default_month)

    return render(request, "managers/finance_month.html", context)


# FINANCES BY BUILDING/APARTMENT + YEAR
# Yearly financial data for selected unit (building or apartment)
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
        "app_name": app_name,
    }

    return render(request, "managers/finance_unit.html", context)


"""
TENANT VIEWS
"""

@login_required
def dashboard_customer(request):
    
    
    context = {
        "default_year": default_year,
        "default_month": default_month,
        "app_name": app_name,
    }
    
    return render(request, "customers/dashboard_customer.html", context)


# Rent Payment Page for Tenants
@login_required
def submit_payment(request, payment_id):
    
    
    context = {
        "default_year": default_year,
        "default_month": default_month,
        "app_name": app_name,
    }
    
    return render(request, "customers/submit_payment.html", context)


# Maintenance Request Page for Tenants
@login_required
def service_request(request, service_id):
    
    
    context = {
        "default_year": default_year,
        "default_month": default_month,
        "app_name": app_name,
    }
    
    return render(request, "customers/service_request.html", context)