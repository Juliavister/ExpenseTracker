from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from .models import Category, Expense
from .forms import CategoryForm, RegisterForm, LoginForm, ExpenseForm
from django.db import IntegrityError
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import LoginView
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


try:
    Category.objects.get_or_create(name='Food')
except IntegrityError:
    pass

def WelcomePage(request):
    return render(request, 'ExpenseTracker/welcome.html')

def info_page(request):
    return render(request, 'ExpenseTracker/InfoPage.html')

def expense_tracker(request):
    return render(request, 'ExpenseTracker/tracker.html')

def add_category(request):
    if request.method == 'POST' and request.is_ajax():
        category_name = request.POST.get('name')

        if category_name:
            try:
                new_category = Category.objects.create(name=category_name)
                return JsonResponse({'message': 'Category added successfully'}, status=200)
            except Exception as e:
                return JsonResponse({'error': f'Failed to add category: {e}'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def AddExpense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  
            expense.save()

            
            new_expense_data = {
                'date': expense.date,
                'category': expense.category.name, 
                'amount': expense.amount,
                'description': expense.description
            }

            return JsonResponse({'success': True, 'new_expense': new_expense_data})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ExpenseForm()
    return render(request, 'ExpenseTracker/tracker.html', {'form': form})


"""def add_category(request):
    if request.method == 'POST' and request.is_ajax():
        category_name = request.POST.get('name')

        if category_name:
            new_category = Category.objects.create(name=category_name)
            return JsonResponse({'message': 'Category added successfully'}, status=200)

    return JsonResponse({'error': 'Failed to add category'}, status=400) """


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'ExpenseTracker/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')
        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            print(request.path) 
            return redirect(to='login')

        return render(request, self.template_name, {'form': form})
    

class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)
            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True
        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)

