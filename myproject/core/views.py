from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect
from django.views.generic import TemplateView
from .forms import EmailForm
from .mixins import EmailMixin


class Index(EmailMixin, TemplateView):
    template_name = 'index.html'
    email_template_name = 'email.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        form = EmailForm()
        # data example
        data = dict()
        data['email_to'] = self.request.POST.get('email_to')
        data['title'] = self.request.POST.get('title')
        data['message'] = self.request.POST.get('message')

        context['form'] = form
        context['data'] = data
        return context

    def post(self, request, *args, **kwargs):
        data = self.send_mail()
        print(data)
        return HttpResponseRedirect(reverse_lazy('core:index'))
