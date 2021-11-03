from django.urls import path
from leads.views import lead_list, lead_detail, lead_create, lead_update, lead_delete, LeadListView, LeadCreateView, LeadUpdateView, LeadDeleteView, LeadDetailView, AssignAgentView, CategoryListView, CategoryDetailView, LeadCategoryUpdateView

app_name = "leads"

urlpatterns = [
    path('', LeadListView.as_view(), name='lead-list'), 
    path('detail/<int:pk>', LeadDetailView.as_view(), name='lead-detail'),
    path('update/<int:pk>', LeadUpdateView.as_view(), name='lead-update'),
    path('delete/<int:pk>', LeadDeleteView.as_view(), name='lead-delete'),
    path('create/', LeadCreateView.as_view(), name='lead-create'),
    path('assign-agent/<int:pk>', AssignAgentView.as_view(), name='assign-agent'),
    path('categories', CategoryListView.as_view(), name = 'category-list'),
    path('categories_detail/<int:pk>', CategoryDetailView.as_view(), name='category-detail'),
    path('<int:pk>/category', LeadCategoryUpdateView.as_view(), name='lead-category-update')
]