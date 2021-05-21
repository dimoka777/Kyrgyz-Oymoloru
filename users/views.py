from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.shortcuts import redirect, render
from .models import CustomUser, Present, OfficeRegion
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data(**kwargs)
        context['office_list'] = OfficeRegion.objects.all()
        context['by_whom'] = CustomUser.objects.filter(level=1, status=True,
                                                       is_staff=False)

        return context


class UserList(UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = 'users_list.html'
    login_url = 'registration/login.html'

    def test_func(self):
        return self.request.user.is_staff


class UserWaitList(UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = 'waiting_users.html'
    login_url = 'registration/login.html'

    def test_func(self):
        return self.request.user.is_staff


class PresentList(UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = 'present_list.html'
    context_object_name = 'list2'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super(PresentList, self).get_context_data(**kwargs)
        context['count_presents'] = Present.objects.all()
        context['gifts_list2'] = CustomUser.objects.all()

        return context


class UserUpdateView(UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'user_update.html'
    # fields = ['username', 'full_name', 'address', 'check_number', 'check_image',
    #           'passport_number', 'office_location', 'phone_number', 'by_whom', 'status',]
    success_url = reverse_lazy('users_list')

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['office_list'] = OfficeRegion.objects.all()
        context['by_whom'] = CustomUser.objects.filter(level=1, status=True,
                                                       is_staff=False)

        return context

    def test_func(self):
        return self.request.user.is_superuser


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'user_delete.html'
    success_url = reverse_lazy('users_list')


class UserDetail(UserPassesTestMixin, DetailView):
    model = CustomUser
    template_name = 'user_details.html'
    context_object_name = 'detail'

    def get_context_data(self, **kwargs):
        context = super(UserDetail, self).get_context_data(**kwargs)
        followers_second = CustomUser.objects.filter(
            by_whom=CustomUser.objects.get(pk=self.kwargs.get('pk')),
            status=True)
        context['followers'] = CustomUser.objects.filter(
            by_whom=CustomUser.objects.get(pk=self.kwargs.get('pk')),
            status=True)
        context['presents'] = Present.objects.filter(
            present_to=CustomUser.objects.get(pk=self.kwargs.get('pk')))

        if len(followers_second) == 1:
            context['third_line_one'] = CustomUser.objects.filter(
                by_whom=CustomUser.objects.get(pk=followers_second[0].pk),
                status=True)

        if len(followers_second) == 2:
            context['third_line_one'] = CustomUser.objects.filter(
                by_whom=CustomUser.objects.get(pk=followers_second[0].pk),
                status=True)
            context['third_line_two'] = CustomUser.objects.filter(
                by_whom=CustomUser.objects.get(pk=followers_second[1].pk),
                status=True)

        if len(followers_second) == 3:
            context['third_line_one'] = CustomUser.objects.filter(
                by_whom=CustomUser.objects.get(pk=followers_second[0].pk),
                status=True)
            context['third_line_two'] = CustomUser.objects.filter(
                by_whom=CustomUser.objects.get(pk=followers_second[1].pk),
                status=True)
            context['third_line_three'] = CustomUser.objects.filter(
                by_whom=CustomUser.objects.get(pk=followers_second[2].pk),
                status=True)

        return context

    def test_func(self):
        return self.request.user.is_staff or CustomUser.objects.filter(username=self.request.user)


def gift_user(request, pk):
    if request.user.is_active and request.user.is_staff:
        template = 'present_create.html'
        user_gift = CustomUser.objects.get(pk=pk)
        if request.method == 'POST':
            a = request.POST['name']
            b = request.POST['info']
            c = request.POST['date']
            data = Present.objects.create(
                present_name=a, present_info=b, present_to=user_gift, present_date=c
            )
            data.save()
            gift_counter = Present.objects.filter(present_to=user_gift)
            if len(gift_counter) == 2:
                user_gift.set_password('qwerty123')
                user_gift.save()
            return redirect('present_list')
        return render(request, template, {'user_gift': user_gift})

def change_password(request, pk):
    user_gift = CustomUser.objects.get(pk=pk)
    user_gift.set_password('password123')
    user_gift.save()
    return redirect('users_list')

def change_status(request, pk):
    todo = CustomUser.objects.get(pk=pk)
    if todo.status == False:
        todo.status = True
    todo.save()
    return redirect('waiting_users')


class OfficeListView(UserPassesTestMixin, ListView):
    model = OfficeRegion
    template_name = 'office_list.html'
    login_url = 'registration/login.html'

    def test_func(self):
        return self.request.user.is_superuser


class OfficeCreateView(UserPassesTestMixin, CreateView):
    model = OfficeRegion
    template_name = 'office_create.html'
    fields = ['office_city']
    success_url = reverse_lazy('office_list')

    def test_func(self):
        return self.request.user.is_superuser


class OfficeUpdateView(UserPassesTestMixin, UpdateView):
    model = OfficeRegion
    template_name = 'office_update.html'
    fields = ['office_city']
    success_url = reverse_lazy('office_list')

    def test_func(self):
        return self.request.user.is_superuser


class OfficeDeleteView(LoginRequiredMixin, DeleteView):
    model = OfficeRegion
    template_name = 'office_delete.html'
    success_url = reverse_lazy('office_list')

    def test_func(self):
        return self.request.user.is_superuser


def login_success(request):
    if request.user.is_staff:
        return redirect('users_list')
    else:
        return redirect('user_detail', pk=request.user.pk)


