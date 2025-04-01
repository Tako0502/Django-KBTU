from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from decimal import Decimal, InvalidOperation

from .models import Expense, Category, GroupExpense
from .filters import ExpenseFilter
from django.contrib.auth.models import User

def home(request):
    return render(request, 'expenses/home.html')

# -----------------------------
# 1. Expense Views
# -----------------------------
@login_required
def expense_list(request):
    """
    List all expenses of the logged-in user with optional filtering.
    """
    expenses = Expense.objects.filter(user=request.user)
    expense_filter = ExpenseFilter(request.GET, queryset=expenses, user=request.user)
    filtered_expenses = expense_filter.qs
    return render(
        request,
        'expenses/expense_list.html',
        {
            'filter': expense_filter,
            'expenses': filtered_expenses
        }
    )

@login_required
def add_expense(request):
    if request.method == 'POST':
        try:
            # Get amount and validate
            amount = request.POST.get('amount', '').strip()
            if not amount:
                raise ValueError('Amount is required')
            
            try:
                amount = Decimal(amount)
                if amount <= 0:
                    raise ValueError('Amount must be greater than 0')
            except InvalidOperation:
                raise ValueError('Invalid amount format')
            
            # Get description and validate
            description = request.POST.get('description', '').strip()
            if not description:
                raise ValueError('Description is required')
            
            # Get date and validate
            date_str = request.POST.get('date')
            if not date_str:
                date_str = timezone.now().date()
            
            # Create and save expense
            expense = Expense(
                user=request.user,
                amount=amount,
                description=description,
                date=date_str
            )
            
            # Handle category if provided
            category_id = request.POST.get('category')
            if category_id:
                try:
                    category = Category.objects.get(id=category_id, user=request.user)
                    expense.category = category
                except Category.DoesNotExist:
                    pass  # Ignore invalid category
            
            expense.save()
            return redirect('expense_list')
            
        except ValueError as e:
            # Handle validation errors
            return render(request, 'expenses/add_expense.html', {
                'error': str(e),
                'categories': Category.objects.filter(user=request.user),
                'today': timezone.now(),
                # Preserve form data
                'form_data': {
                    'amount': request.POST.get('amount', ''),
                    'description': request.POST.get('description', ''),
                    'category': request.POST.get('category', ''),
                    'date': request.POST.get('date', '')
                }
            })
    
    # GET request
    return render(request, 'expenses/add_expense.html', {
        'categories': Category.objects.filter(user=request.user),
        'today': timezone.now()
    })

@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    categories = Category.objects.filter(user=request.user)
    
    if request.method == 'POST':
        expense.amount = request.POST.get('amount')
        expense.description = request.POST.get('description')
        expense.category_id = request.POST.get('category')
        expense.date = request.POST.get('date')
        expense.save()
        return redirect('expense_list')
    
    return render(request, 'expenses/edit_expense.html', {
        'expense': expense,
        'categories': categories
    })

@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
    return redirect('expense_list')

# -----------------------------
# 2. Category Views
# -----------------------------
@login_required
def category_list(request):
    """
    List categories owned by the current user.
    """
    categories = Category.objects.filter(user=request.user)
    return render(request, 'expenses/category_list.html', {'categories': categories})

@login_required
def add_category(request):
    """
    Create a new category for the current user.
    """
    if request.method == 'POST':
        Category.objects.create(name=request.POST['name'], user=request.user)
        return redirect('category_list')
    return render(request, 'expenses/add_category.html')

@login_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.save()
        return redirect('category_list')
    return render(request, 'expenses/edit_category.html', {'category': category})

@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
    return redirect('category_list')

# -----------------------------
# 3. GroupExpense Views
# -----------------------------
@login_required
def group_expense_list(request):
    """
    Display all group expenses. 
    (Optionally, filter by those that include the current user if needed.)
    """
    group_expenses = GroupExpense.objects.all().order_by('-date')
    return render(request, 'expenses/group_expense_list.html', {'group_expenses': group_expenses})

@login_required
def add_group_expense(request):
    """
    Create a group expense shared by multiple users.
    """
    if request.method == 'POST':
        name = request.POST['name']
        amount = request.POST['amount']
        users = request.POST.getlist('users')

        group_expense = GroupExpense.objects.create(
            name=name,
            amount=amount,
            date=timezone.now()  # or parse from POST if needed
        )
        group_expense.users.set(users)
        return redirect('group_expense_list')

    # Show a form on GET
    all_users = User.objects.all()
    return render(request, 'expenses/add_group_expense.html', {'all_users': all_users})

@login_required
def edit_group_expense(request, pk):
    group_expense = get_object_or_404(GroupExpense, pk=pk)
    if request.method == 'POST':
        group_expense.name = request.POST.get('name')
        group_expense.amount = request.POST.get('amount')
        group_expense.date = request.POST.get('date')
        group_expense.users.set(request.POST.getlist('users'))
        group_expense.save()
        return redirect('group_expense_list')
    return render(request, 'expenses/edit_group_expense.html', {
        'group_expense': group_expense,
        'users': User.objects.all()
    })

@login_required
def delete_group_expense(request, pk):
    group_expense = get_object_or_404(GroupExpense, pk=pk)
    if request.method == 'POST':
        group_expense.delete()
    return redirect('group_expense_list')
