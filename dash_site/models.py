from django.db import models
import os
from dotenv import load_dotenv
load_dotenv()

# units/offices table
class UnitModel(models.Model):
    unit_id = models.CharField(primary_key=True, max_length=5, db_column=os.getenv('UNIT_ID_COLUMN', 'unit_id'))
    bldg_id = models.CharField(max_length=1, db_column=os.getenv('BLDG_ID_COLUMN', 'bldg_id'))
    unit_rooms = models.IntegerField(db_column=os.getenv('UNIT_ROOMS_COLUMN', 'unit_rooms'))
    unit_contract = models.CharField(max_length=255, db_column=os.getenv('UNIT_CONTRACT_COLUMN', 'unit_contract'))
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('UNIT_COST_COLUMN', 'unit_cost'))

    class Meta:
        db_table = os.getenv('UNIT_TABLE_NAME', 'unitTable')
        managed = False

    def __str__(self):
        return self.unit_id


# buildings table
class BldgModel(models.Model):
    bldg_id = models.CharField(primary_key=True, max_length=1, db_column=os.getenv('BLDG_ID_COLUMN', 'bldg_id'))
    bldg_own = models.CharField(max_length=255, db_column=os.getenv('BLDG_OWNER_COLUMN', 'bldg_own'))
    bldg_val = models.DecimalField(max_digits=20, decimal_places=2, db_column=os.getenv('BLDG_VALUE_COLUMN', 'bldg_val'))
    bldg_ins = models.DecimalField(max_digits=20, decimal_places=2, db_column=os.getenv('BLDG_INSXYR_COLUMN', 'bldg_ins'))

    class Meta:
        db_table = os.getenv('BLDG_TABLE_NAME', 'bldg_table')
        managed = False

    def __str__(self):
        return self.bldg_id


# expenses table
class ExpenseModel(models.Model):
    exp_id = models.AutoField(primary_key=True, db_column=os.getenv('EXP_ID_COLUMN', 'exp_id'))
    unit_id = models.CharField(max_length=5, db_column=os.getenv('UNIT_ID_COLUMN', 'unit_id'))
    exp_name = models.CharField(max_length=255, db_column=os.getenv('EXP_NAME_COLUMN', 'exp_name'))
    exp_amt = models.DecimalField(max_digits=15, decimal_places=2, db_column=os.getenv('EXP_AMT_COLUMN', 'exp_amt'))
    exp_date = models.DateField(db_column=os.getenv('EXP_DATE_COLUMN', 'exp_date'))
    exp_rct = models.FileField(upload_to='expense_receipts/', db_column=os.getenv('EXP_RCT_COLUMN', 'exp_rct'))
    exp_bldg = models.IntegerField(db_column=os.getenv('EXP_BLDG_COLUMN', 'exp_bldg'))

    class Meta:
        db_table = os.getenv('EXP_TABLE_NAME', 'expense_table')
        managed = False

    def __str__(self):
        expense = "{0}: {1} for {2} on {3}".format(self.unit_id, self.exp_amt, self.exp_name, self.exp_date)
        return expense


# icome table
class IncomeModel(models.Model):
    income_id = models.AutoField(primary_key=True, db_column=os.getenv('INCOME_ID_COLUMN', 'income_id'))
    unit_id = models.CharField(max_length=5, db_column=os.getenv('UNIT_ID_COLUMN', 'unit_id'))
    income_amt = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('INCOME_AMT_COLUMN', 'income_amt'))
    income_date = models.DateField(db_column=os.getenv('INCOME_DATE_COLUMN', 'income_date'))
    income_month = models.IntegerField(db_column=os.getenv('INCOME_MONTH_COLUMN', 'income_month'))
    income_year = models.IntegerField(db_column=os.getenv('INCOME_YEAR_COLUMN', 'income_year'))

    class Meta:
        db_table = os.getenv('INCOME_TABLE_NAME', 'income_table')
        managed = False
    
    def __str__(self):
        income = "{0}: {1} on {2}".format(self.unit_id, self.income_amt, self.income_date)
        return income


# clients table
class ClientModel(models.Model):
    client_id = models.AutoField(primary_key=True, db_column=os.getenv('CLIENT_ID_COLUMN', 'client_id'))
    unit_id = models.CharField(max_length=5, db_column=os.getenv('UNIT_ID_COLUMN', 'unit_id'))
    client_last_name = models.CharField(max_length=255, db_column=os.getenv('CLIENT_LAST_COLUMN', 'client_last_name'))
    client_first_name = models.CharField(max_length=255, db_column=os.getenv('CLIENT_FIRST_COLUMN', 'client_first_name'))
    client_contract_date = models.DateField(db_column=os.getenv('CLIENT_CONTRACT_DATE_COLUMN', 'client_contract_date'))
    client_contract = models.CharField(max_length=255, db_column=os.getenv('CLIENT_CONTRACT_COLUMN', 'client_contract'))
    client_property = models.IntegerField(db_column=os.getenv('CLIENT_PROPERTY_COLUMN', 'client_property'))

    class Meta:
        db_table = os.getenv('CLIENT_TABLE_NAME', 'client_table')
        managed = False
    
    def __str__(self):
        client = "{0}: {1}, {2}".format(self.unit_id, self.client_last_name, self.client_first_name)
        return client
    

# view of expenses x building x year & month
class BldgExpYrModel(models.Model):
    
    # Building ID column
    unit_id = models.CharField(max_length=1, db_column=os.getenv('BLDG_ID_COLUMN', 'unit_id'))
    
    # Columns for each month of expenses
    jan = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('JANUARY_COLUMN', 'jan'))
    feb = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('FEBRUARY_COLUMN', 'feb'))
    mar = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('MARCH_COLUMN', 'mar'))
    apr = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('APRIL_COLUMN', 'apr'))
    may = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('MAY_COLUMN', 'may'))
    jun = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('JUNE_COLUMN', 'jun'))
    jul = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('JULY_COLUMN', 'jul'))
    aug = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('AUGUST_COLUMN', 'aug'))
    sep = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('SEPTEMBER_COLUMN', 'sep'))
    oct = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('OCTOBER_COLUMN', 'oct'))
    nov = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('NOVEMBER_COLUMN', 'nov'))
    dec = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('DECEMBER_COLUMN', 'dec'))
    
    # Column for total yearly expenses per building
    year_total = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('YEAR_TOTAL_COLUMN', 'year_total'))
    
    # Year (int) column
    year = models.IntegerField(db_column=os.getenv('EXP_YEAR_COLUMN', 'year'))

    class Meta:
        db_table = os.getenv('BLDG_EXPENSES_VIEW_NAME', 'bldg_exp_view')
        managed = False

    def save(self, *args, **kwargs):
        # Override save method to prevent saving
        pass
    
    def __str__(self):
        expenses = "{0}: {1} for {2}".format(self.unit_id, self.year_total, self.year)
        return expenses
        

# view of income x building x year & month
class BldgIncomeYrModel(models.Model):
    
    # Buidling ID column
    unit_id = models.CharField(max_length=1, db_column=os.getenv('BLDG_ID_COLUMN', 'unit_id'))
    
    # Columns for each month of expenses
    jan = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('JANUARY_COLUMN', 'jan'))
    feb = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('FEBRUARY_COLUMN', 'feb'))
    mar = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('MARCH_COLUMN', 'mar'))
    apr = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('APRIL_COLUMN', 'apr'))
    may = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('MAY_COLUMN', 'may'))
    jun = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('JUNE_COLUMN', 'jun'))
    jul = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('JULY_COLUMN', 'jul'))
    aug = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('AUGUST_COLUMN', 'aug'))
    sep = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('SEPTEMBER_COLUMN', 'sep'))
    oct = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('OCTOBER_COLUMN', 'oct'))
    nov = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('NOVEMBER_COLUMN', 'nov'))
    dec = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('DECEMBER_COLUMN', 'dec'))
    
    # Column for total yearly expenses per building
    year_total = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('YEAR_TOTAL_COLUMN', 'year_total'))
    
    # Year (int) column
    year = models.IntegerField(db_column=os.getenv('INCOME_YEAR_COLUMN', 'year'))

    class Meta:
        db_table = os.getenv('BLDG_INCOME_VIEW_NAME', 'bldg_income_view')
        managed = False

    def save(self, *args, **kwargs):
        # Override save method to prevent saving
        pass
    
    def __str__(self):
        income = "{0}: {1} for {2}".format(self.unit_id, self.year_total, self.year)
        return income


# view of expenses x apartment x year & month
class UnitExpYrModel(models.Model):
    
    # Apartment ID Column
    unit_id = models.CharField(max_length=1, db_column=os.getenv('UNIT_ID_COLUMN', 'unit_id'))
    
    # Columns for each month of expenses
    jan = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('JANUARY_COLUMN', 'jan'))
    feb = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('FEBRUARY_COLUMN', 'feb'))
    mar = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('MARCH_COLUMN', 'mar'))
    apr = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('APRIL_COLUMN', 'apr'))
    may = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('MAY_COLUMN', 'may'))
    jun = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('JUNE_COLUMN', 'jun'))
    jul = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('JULY_COLUMN', 'jul'))
    aug = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('AUGUST_COLUMN', 'aug'))
    sep = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('SEPTEMBER_COLUMN', 'sep'))
    oct = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('OCTOBER_COLUMN', 'oct'))
    nov = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('NOVEMBER_COLUMN', 'nov'))
    dec = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('DECEMBER_COLUMN', 'dec'))
    
    # Column for total yearly expenses per building
    year_total = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('YEAR_TOTAL_COLUMN', 'year_total'))
    
    # Year (int) column
    year = models.IntegerField(db_column=os.getenv('EXP_YEAR_COLUMN', 'year'))

    class Meta:
        db_table = os.getenv('UNIT_EXPENSES_VIEW_NAME', 'unit_exp_view')
        managed = False

    def save(self, *args, **kwargs):
        # Override save method to prevent saving
        pass
    
    def __str__(self):
        expenses = "{0}: {1} for {2}".format(self.unit_id, self.year_total, self.year)
        return expenses

# view of income x unit x year & month
class UnitIncomeYrModel(models.Model):
    
    # Apartment ID Column
    unit_id = models.CharField(max_length=1, db_column=os.getenv('UNIT_ID_COLUMN', 'unit_id'))

    # Columns for each month of expenses
    jan = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('JANUARY_COLUMN', 'jan'))
    feb = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('FEBRUARY_COLUMN', 'feb'))
    mar = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('MARCH_COLUMN', 'mar'))
    apr = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('APRIL_COLUMN', 'apr'))
    may = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('MAY_COLUMN', 'may'))
    jun = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('JUNE_COLUMN', 'jun'))
    jul = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('JULY_COLUMN', 'jul'))
    aug = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('AUGUST_COLUMN', 'aug'))
    sep = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('SEPTEMBER_COLUMN', 'sep'))
    oct = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('OCTOBER_COLUMN', 'oct'))
    nov = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('NOVEMBER_COLUMN', 'nov'))
    dec = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('DECEMBER_COLUMN', 'dec'))
    
    # Column for total yearly expenses per building
    year_total = models.DecimalField(max_digits=10, decimal_places=2, db_column=os.getenv('YEAR_TOTAL_COLUMN', 'year_total'))
    
    # Year (int) column
    year = models.IntegerField(db_column=os.getenv('INCOME_YEAR_COLUMN', 'year'))

    class Meta:
        db_table = os.getenv('UNIT_INCOME_VIEW_NAME', 'unit_income_view')
        managed = False

    def save(self, *args, **kwargs):
        # Override save method to prevent saving
        pass
    
    def __str__(self):
        income = "{0}: {1} for {2}".format(self.unit_id, self.year_total, self.year)
        return income
    

