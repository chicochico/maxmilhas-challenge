from django.views.generic import TemplateView
from cpf_site.forms import CheckCPFForm
from django.shortcuts import render
from cpf.models import CPFBlacklist


class CheckCPF(TemplateView):
    """
    A view to check if CPF is in a blacklist
    """
    main_template = 'cpf_site/check_cpf.html'
    result_template = 'cpf_site/check_cpf_result.html'

    def get(self, request):
        """
        Render a form with CPF input with validation
        """
        if 'cpf' not in request.GET:
            form = CheckCPFForm()
            return render(request, self.main_template, {'form': form})

        form = CheckCPFForm(request.GET)

        if form.is_valid():
            cpf = form.cleaned_data['cpf']
            is_blacklisted = CPFBlacklist.is_blacklisted(cpf)
            args = {'form': form, 'cpf': cpf, 'blacklisted': is_blacklisted}
            return render(request, self.result_template, args)
        else:
            return render(request, self.main_template, {'form': form})

    def post(self, request):
        """
        Render a hidden form to add or remove a CPF from blacklist
        """
        cpf = request.POST['cpf']
        if CPFBlacklist.is_blacklisted(cpf):
            CPFBlacklist.remove_cpf(cpf)
            msg = 'CPF: {} removed from the blacklist.'.format(cpf)
        else:
            CPFBlacklist.add_cpf(cpf)
            msg = 'CPF: {} added to the blacklist.'.format(cpf)
        form = CheckCPFForm()
        args = {'form': form, 'msg': msg}
        return render(request, self.main_template, args)
