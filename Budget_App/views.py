from django.shortcuts import render

# Create your views here.
from .forms import TransactionForm
from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import Transaction, Category
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    total_income = transactions.filter(category__type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = transactions.filter(category__type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    return render(request, 'Budget_App/dashboard.html', {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
    })

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user  # Przypisujemy transakcję do zalogowanego usera
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()

    return render(request, 'Budget_App/add_transaction.html', {'form': form})
@login_required
def delete_transaction(request, pk):
    transaction = Transaction.objects.get(id=pk, user=request.user)
    transaction.delete()
    return redirect('dashboard')