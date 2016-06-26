from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PracticaFinal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'.*', 'MyApp.views.cosa'),
    url(r'^$', 'MyApp.views.pag_principal'),
    url(r'cargar$', 'MyApp.views.cargar_datos'),
    url(r'alojam$', 'MyApp.views.pag_todos_aloj'),
    url(r'ranking$', 'MyApp.views.ordenar_maximas_visitas'),
    url(r'cambiar_titulo', 'MyApp.views.cambiar_titulo'),
    url(r'megusta/(\d+)$', 'MyApp.views.anadir_megusta'),
    url(r'templates/estilo_general\.css', 'MyApp.views.css'),
    url(r'alojamientos/templates/estilo_general\.css$', 'MyApp.views.css'),
    url(r'.*/templates/estilo_general\.css$', 'MyApp.views.css'),
    # url(r'templates/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'templates/'}),
    # url(r'alojamientos/templates/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'templates/'}),
    # url(r'.*/templates/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'templates/'}),
    url(r'.*/zenlike/images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'templates/zenlike/images/'}),
    url(r'alojamientos/(.*)$', 'MyApp.views.pag_aloj'),
    url(r'^login$', 'MyApp.views.login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^about$', 'MyApp.views.about'),
    url(r'poner_comentario/(.*)$', 'MyApp.views.poner_comentario'),
    url(r'otro_idioma/(.+)/(\d+)$', 'MyApp.views.pag_aloj_otro_idioma'),
    url(r'anadir_a_pag/(.+)$', 'MyApp.views.anadir_hotel_pag'),
    url(r'^(.+)/xml$', 'MyApp.views.crear_xml'),
    url(r'^rss/(\d+)$', 'MyApp.views.rss'),
    url(r'^ppal_xml$', 'MyApp.views.pag_ppal_xml'),
    url(r'(.+)$', 'MyApp.views.pag_usuario'),

    url(r'^admin/', include(admin.site.urls)),
)
