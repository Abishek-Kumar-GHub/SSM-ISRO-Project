from django.urls import path
from .views import FileView, get_columns, GeneratePlotView,GenerateFITSView,index,date_selector,CorrelationView,plot_html,Prop_Plot

urlpatterns = [
    path('file/', FileView.as_view(), name='file_view'),
    path('columns/', get_columns, name='get_columns'),
    path('generate_plot/', GeneratePlotView.as_view(), name='generate_plot'),
    path('generate_fits/', GenerateFITSView.as_view(), name='generate_fits'),
    
    path('', index, name='index'),  # Home Page
    path('date_selector/', date_selector, name='date_selector'),
    
    path('correlation/', CorrelationView.as_view(), name='correlation_html'),
    path('generate_fits/', GenerateFITSView.as_view(), name='fits_creator'),
    
    path('plot/', plot_html, name='plot_html'),
    path('prop_plot/',Prop_Plot.as_view(),name='prop_plot'),

    
]



