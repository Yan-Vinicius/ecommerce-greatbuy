from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Account


# Register your models here.
class AccountAdmin(UserAdmin):
    #campos para listar as informações das contas
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    filter_horizontal = ()
    list_filter = ()
    #orndena as contas pelas datas que foram criadas
    ordering = ('-date_joined',)
    #campos que não podem ser editados
    readonly_fields = ('last_login', 'date_joined')
    #ao clicar em qualquer um desses campos, o usuário abrirá as infos da conta
    list_display_links = ('email', 'first_name', 'last_name')
    #campo para fazer a senha não ser editável
    fieldsets = ()


admin.site.register(Account, AccountAdmin)


