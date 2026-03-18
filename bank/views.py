from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Account, Transaction
import random
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# ✅ Generate account number
def generate_account_number():
    return str(random.randint(100000000000, 999999999999))

# ✅ Home (redirect)
def home(request):
    return redirect('login')

# ✅ Create account
def create_account(request):
    if request.user.is_authenticated:
        if not Account.objects.filter(user=request.user).exists():
            Account.objects.create(
                user=request.user,
                account_number=generate_account_number()
            )
    return redirect('dashboard')

# ✅ Dashboard
@login_required(login_url='/login/')
def dashboard(request):
    account, created = Account.objects.get_or_create(
        user=request.user,
        defaults={'account_number': generate_account_number()}
    )

    transactions = Transaction.objects.filter(account=account)

    return render(request, 'dashboard.html', {
        'balance': account.balance,
        'transactions': transactions
    })

# ✅ Signup
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})
# ✅ Deposit money
def deposit(request):
    if request.method == "POST":
        amount = float(request.POST['amount'])
        account = Account.objects.get(user=request.user)

        account.balance += amount
        account.save()

        Transaction.objects.create(
            account=account,
            transaction_type='deposit',
            amount=amount
        )

    return redirect('dashboard')


# ✅ Withdraw money
def withdraw(request):
    if request.method == "POST":
        amount = float(request.POST['amount'])
        account = Account.objects.get(user=request.user)

        if account.balance >= amount:
            account.balance -= amount
            account.save()

            Transaction.objects.create(
                account=account,
                transaction_type='withdraw',
                amount=amount
            )

    return redirect('dashboard')