from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


class CustomLoginView(LoginView):
    template_name = 'list/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('main')


class RegisterPage(FormView):
    template_name = 'list/register.html'
    form_class = SignUpForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('main')
    email = forms.EmailField(max_length=64, help_text='Enter a valid email address')

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'email', 'password1', 'password2']

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('main')
        return super(RegisterPage, self).get(*args, **kwargs)

    def get_success_url(self):
        template = render_to_string('list/email_template.html', {'name': self.request.user.username})
        email_message = EmailMessage(
            'Thank you for being with us.',
            template,
            settings.EMAIL_HOST_USER,
            [self.request.user.email]
        )
        email_message.fail_silently = False
        email_message.send()
        return reverse_lazy('main')


class DeskList(LoginRequiredMixin, ListView):
    model = Desk
    login_url = reverse_lazy('login')
    context_object_name = 'desks'
    template_name = 'list/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['desks'] = context['desks'].filter(user=self.request.user)
        search_input = self.request.GET.get('search-area') or ''
        context['desks2'] = context['desks']
        if search_input:
            context['desks2'] = context['desks'].filter(
                name__icontains=search_input)
        context['search_input'] = search_input
        return context


class DeskCreate(LoginRequiredMixin, CreateView, ListView):
    model = Desk
    login_url = reverse_lazy('login')
    template_name = 'list/add_desk.html'
    fields = ['name', 'image']
    success_url = reverse_lazy('main')
    context_object_name = 'desks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['desks2'] = context['desks'].filter(user=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(DeskCreate, self).form_valid(form)


class DeskUpdate(LoginRequiredMixin, UpdateView, ListView):
    model = Desk
    login_url = reverse_lazy('login')
    fields = ['name', 'image']
    template_name = 'list/add_desk.html'
    success_url = reverse_lazy('main')
    context_object_name = 'desks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['desks2'] = context['desks'].filter(user=self.request.user)
        return context


class DeleteDesk(LoginRequiredMixin, DeleteView):
    model = Desk
    login_url = reverse_lazy('login')
    context_object_name = 'desk'
    success_url = reverse_lazy('main')


@login_required(login_url='login')
def task_list(request, pk):
    desks2 = Desk.objects.filter(user=request.user)
    desk = desks2.get(id=pk)
    tasks = desk.task_set.all()
    count = tasks.filter(complete=False).count()
    context = {'desks2': desks2, 'desk': desk, 'tasks': tasks, 'count': count}
    return render(request, 'list/desk.html', context)


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    login_url = reverse_lazy('login')
    template_name = 'list/add_task.html'
    fields = ['title', 'description', 'complete']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['desks2'] = Desk.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.desk_id = self.kwargs.get('pk')
        return super(TaskCreate, self).form_valid(form)

    def get_success_url(self):
        desk_id = self.object.desk.id
        return reverse_lazy('desk', kwargs={'pk': desk_id})


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    login_url = reverse_lazy('login')
    fields = ['title', 'description', 'complete']
    template_name = 'list/add_task.html'

    def get_success_url(self):
        desk_id = self.object.desk.id
        return reverse_lazy('desk', kwargs={'pk': desk_id})


class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    login_url = reverse_lazy('login')
    context_object_name = 'task'

    def get_success_url(self):
        desk_id = self.object.desk.id
        return reverse_lazy('desk', kwargs={'pk': desk_id})


class Task(LoginRequiredMixin, DetailView):
    model = Task
    login_url = reverse_lazy('login')
    template_name = 'list/task.html'