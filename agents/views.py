from django.shortcuts import render, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganisorAndRequiredMixin
from django.core.mail import send_mail
import random
# Create your views here.


class AgentListView(OrganisorAndRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"

    def get_queryset(self):
        organisation = self.request.user.userprofile

        return Agent.objects.filter(organisation = organisation)

class AgentCreateView(OrganisorAndRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"

    form_class = AgentModelForm

    def form_valid(self, form):
        user =form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"{random.randint(0, 100000)}")
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile

        )
        #agent.organisation = self.request.user.userprofile
        #agent.save()
        send_mail(
            subject="You are invited to be an agent",
            message="You were added as an agent in DJCRM. Please come Login",
            from_email="admin@test.com",
            recipient_list=[user.email]
        )
        return super(AgentCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("agents:agent-list")

    

class AgentDetailView(OrganisorAndRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name ="agent"
    
    def get_queryset(self):
        return Agent.objects.all()


class AgentUpdateView(OrganisorAndRequiredMixin, generic.UpdateView):

    template_name ="agents/agent_update.html"
    form_class = AgentModelForm

    def get_queryset(self):
        return Agent.objects.all()
    
    def get_success_url(self):
        return reverse("agents:agent-list")

class AgentDeleteView(OrganisorAndRequiredMixin, generic.DeleteView):

    template_name = "agents/agent_delete.html"
    context_object_name ="agent"
    
    def get_queryset(self):
        organisation = self.request.user.userprofile

        return Agent.objects.filter(organisation = organisation)
        
    def get_success_url(self):
        return reverse("agents:agent-list")
