from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from leads.models import Lead, Agent, Category
from leads.forms import LeadForm, LeadModelForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorAndRequiredMixin
# Create your views here.

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

class LandingPageView(TemplateView):
    template_name = "landing.html"
    

def landing_page(request):
    return render(request, "landing.html")

class LeadListView(LoginRequiredMixin, ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
#initial queryset of leads for thr entire organisation

        if user.is_organiser:
            queryset = Lead.objects.filter(organisation= user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organisation= user.agent.organisation, agent__isnull=False)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user = user)
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organiser: 
            queryset = Lead.objects.filter(
                organisation = user.userprofile,
                agent__isnull = True
            )
            context.update({
                "unassigned_leads": queryset
            })
        return context

def lead_list(request):
    leads = Lead.objects.all()
    context ={'leads': leads}
    return render(request, "leads/lead_list.html", context)

class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
#initial queryset of leads for thr entire organisation

        if user.is_organiser:
            queryset = Lead.objects.filter(organisation= user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation= user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user = user)
        return queryset

def lead_detail(request, pk):
    lead = Lead.objects.get(id = pk)
    context={'lead':lead}
    return render(request,"leads/lead_detail.html", context)

class LeadDeleteView(OrganisorAndRequiredMixin, DeleteView):
    template_name = "leads/lead_delete.html"
    #context_object_name = "lead"
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation= user.userprofile)

def lead_delete(request, pk):
    lead = Lead.objects.get(id = pk)
    lead.delete()
    return redirect("/leads")

class AssignAgentView(OrganisorAndRequiredMixin, generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self,**kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

    def get_success_url(self):
        return reverse("leads:lead-list")

class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset =Lead.objects.filter(
                organisation = user.agent.organisation
            )            
        context.update({
            "unassigned_lead": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        #initial queryset of leads for thr entire organisation

        if user.is_organiser:
            queryset = Category.objects.filter(organisation= user.userprofile)
        else:
            queryset = Category.objects.filter(organisation= user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user = user)
        return queryset


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

#   def get_context_data(self, **kwargs):
#       context = super(CategoryDetailView, self).get_context_data(**kwargs)
#       user = self.request.user
#
#       leads= self.get_object().leads.all()
#       
#
#       context.update({
#           "leads":leads
#       })
#       return context

    def get_queryset(self):
        user = self.request.user
        #initial queryset of leads for thr entire organisation

        if user.is_organiser:
            queryset = Category.objects.filter(organisation= user.userprofile)
        else:
            queryset = Category.objects.filter(organisation= user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user = user)
        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_category_update.html" 
    
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation= user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation= user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user = user)
        return queryset
    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})      

class LeadUpdateView(OrganisorAndRequiredMixin, UpdateView):
 
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation= user.userprofile)

def lead_update(request, pk):
    lead =Lead.objects.get(id = pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/leads")

    context={
        'lead':lead,
        'form':form
    }
    return render(request,"leads/lead_update.html",context)

#def lead_create(request):
#    form =LeadForm()
#    if request.method == "POST":
#        print("Receiving a post request")
#        form = LeadForm(request.POST)
#        if form.is_valid():
#            #print("The form is valid")
#            #print(form.cleaned_data)
#            first_name = form.cleaned_data['first_name']
#            last_name =form.cleaned_data['last_name']
#            age = form.cleaned_data['age']
#            agent = Agent.objects.first()
#            Lead.objects.create(
#                first_name = first_name,
#                last_name = last_name,
#                age = age,
#                agent = agent
#            )
#            return redirect("/leads")
#            #print("Lead Has Been Created Succesfully")
#
#    print(request.POST)
#    context ={
#        'form': LeadForm()
#    }
#    return render(request, "leads/lead_create.html", context)

class LeadCreateView(OrganisorAndRequiredMixin, CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        # TODO send email
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)


def lead_create(request):
    form =LeadModelForm()
    if request.method == "POST":
        print("Receiving a post request")
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/leads")
            #print("Lead Has Been Created Succesfully")

    #print(request.POST)
    context ={
        'form': form
    }
    return render(request, "leads/lead_create.html", context)





#def home_page1(request):
#    return render(request, "home.html")
#
#def home_page2(request):
#
#    context = {
#        'name': "Chidi",
#        'age':69
#    }
#
#    return render(request, "home_page2.html", context)


