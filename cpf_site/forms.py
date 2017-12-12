from django import forms
from cpf.models import CPF, CPFBlacklist


class CheckCPFForm(forms.Form):
    """
    A form to get a CPF number
    with validation
    """
    cpf = forms.CharField(
        label='CPF',
        max_length=11,
        help_text='Type numbers only.',
    )

    def clean_cpf(self):
        """
        Validate the imputed CPF
        """
        data = self.cleaned_data['cpf']
        cpf_number = CPF(number=data)
        if not cpf_number.is_valid():
            raise forms.ValidationError('Invalid CPF number.')
        else:
            return data


