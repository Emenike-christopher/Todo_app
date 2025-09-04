from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from .forms import UserRegistrationForm, TaskForm 
from django.shortcuts import redirect, get_object_or_404
from django.views import View
# ----------------------------
# Task Views (CRUD)
# ----------------------------

class TaskView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'Todo_app/task_home.html'

    def get_queryset(self):
        # Start with all tasks of the user
        queryset = Task.objects.filter(user=self.request.user)

        # Filter by status if query parameter exists
        status = self.request.GET.get('status')
        if status in ['pending', 'completed']:
            queryset = queryset.filter(status=status)

        # Filter by category if query parameter exists
        category = self.request.GET.get('category')
        if category in ['morning_routine', 'career', 'personal_growth', 'recreation']:
            queryset = queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_tasks = Task.objects.filter(user=self.request.user)

        # Counts for sidebar
        context['pending_tasks'] = all_tasks.filter(status='pending')
        context['completed_tasks'] = all_tasks.filter(status='completed')

        # Active filter/category for sidebar highlighting
        context['active_status'] = self.request.GET.get('status', '')
        context['active_category'] = self.request.GET.get('category', '')

        return context
    
      # NEW: Handle "Mark as Completed"
    def post(self, request, *args, **kwargs):
        task_id = request.POST.get('task_id')  # gets hidden input from form
        task = Task.objects.filter(id=task_id, user=request.user).first()
        if task:
            task.status = 'completed'
            task.save()
        return redirect(request.path)  # refresh the page

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'Todo_app/task_detail.html'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'Todo_app/task_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user  # assign task to logged-in user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'Todo_app/task_form.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'Todo_app/task_delete.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class SignUpView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


class MarkTaskCompletedView(LoginRequiredMixin, View):
    def post(self, request, pk,):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.status = 'completed'
        task.save()
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    
class ToggleTaskStatusView(View):
    def post(self, pk,):
        task = get_object_or_404(Task, pk=pk )
        task.status = 'pending' if task.status == 'completed' else 'completed'
        task.save()
        return redirect('home')  