'''from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django import forms
from Empresas.models import Empresa
from django.contrib.auth import get_user_model
import logging


logger = logging.getLogger(__name__)



class CustomAuthenticationForm(AuthenticationForm):
    document = forms.CharField(max_length=18, required=True) 

    def confirm_login_allowed(self, user):
        document = self.cleaned_data.get('document')

        # Verificar se o usuário é superusuário, e permitir login sem validação de documento
        if user.is_superuser:
            return  # Superusuário pode logar em qualquer documento

        # Logando o documento recebido e o documento da empresa
        logger.info(f"Validando documento: {document} para o usuário {user.username}, documento da empresa: {user.empresa.document}")

        # Validar se o documento informado corresponde ao da empresa associada ao usuário
        if user.empresa.document != document:
            raise forms.ValidationError("Documento incorreto para este usuário.", code='invalid_login')





class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['name', 'document', 'database']



User = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput)
    empresa = forms.ModelChoiceField(queryset=Empresa.objects.all(), required=False)  # Somente para superusuários

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'empresa']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
'''