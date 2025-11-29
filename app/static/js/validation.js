const ValidationService = {
    // Validação de CPF
    validarCPF(cpf) {
        cpf = cpf.replace(/\D/g, '');
        
        if (cpf.length !== 11) return false;
        if (/^(\d)\1+$/.test(cpf)) return false; // Verifica se todos os dígitos são iguais
        
        let soma = 0;
        let resto;
        
        // Validação do primeiro dígito verificador
        for (let i = 1; i <= 9; i++) {
            soma += parseInt(cpf.substring(i - 1, i)) * (11 - i);
        }
        resto = (soma * 10) % 11;
        if (resto === 10 || resto === 11) resto = 0;
        if (resto !== parseInt(cpf.substring(9, 10))) return false;
        
        // Validação do segundo dígito verificador
        soma = 0;
        for (let i = 1; i <= 10; i++) {
            soma += parseInt(cpf.substring(i - 1, i)) * (12 - i);
        }
        resto = (soma * 10) % 11;
        if (resto === 10 || resto === 11) resto = 0;
        if (resto !== parseInt(cpf.substring(10, 11))) return false;
        
        return true;
    },

  
    validarEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    },

    validarTelefone(telefone) {
        const cleaned = telefone.replace(/\D/g, '');
        return cleaned.length === 10 || cleaned.length === 11;
    },

 
    validarDataNascimento(data) {
        if (!data) return false;
        const dataObj = new Date(data);
        const hoje = new Date();
        hoje.setHours(0, 0, 0, 0);
        
        return dataObj <= hoje && dataObj.getFullYear() > 1900;
    },


    validarIdadeMinima(data, idadeMinima) {
        if (!data) return false;
        const dataNasc = new Date(data);
        const hoje = new Date();
        let idade = hoje.getFullYear() - dataNasc.getFullYear();
        const mes = hoje.getMonth() - dataNasc.getMonth();
        
        if (mes < 0 || (mes === 0 && hoje.getDate() < dataNasc.getDate())) {
            idade--;
        }
        
        return idade >= idadeMinima;
    },

    // Validação de senha forte
    validarSenhaForte(senha) {
        if (senha.length < 8) return false;
        // Verifica se tem pelo menos uma letra e um número
        const temLetra = /[a-zA-Z]/.test(senha);
        const temNumero = /[0-9]/.test(senha);
        return temLetra && temNumero;
    },

    validarCampoObrigatorio(valor) {
        return valor && valor.trim().length > 0;
    },


    validarNumeroPositivo(valor) {
        const numero = parseFloat(valor);
        return !isNaN(numero) && numero >= 0;
    },

    validarTamanhoString(valor, min, max) {
        if (!valor) return false;
        const tamanho = valor.trim().length;
        return tamanho >= min && tamanho <= max;
    },

    // Máscara para CPF
    aplicarMascaraCPF(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 11) {
                value = value.slice(0, 11);
            }
            if (value.length > 3) {
                value = value.replace(/(\d{3})(\d)/, '$1.$2');
            }
            if (value.length > 7) {
                value = value.replace(/(\d{3})\.(\d{3})(\d)/, '$1.$2.$3');
            }
            if (value.length > 11) {
                value = value.replace(/(\d{3})\.(\d{3})\.(\d{3})(\d)/, '$1.$2.$3-$4');
            }
            e.target.value = value;
        });
    },


    aplicarMascaraTelefone(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 11) {
                value = value.slice(0, 11);
            }
            if (value.length > 2) {
                value = value.replace(/^(\d{2})(\d)/, '($1) $2');
            }
            if (value.length > 10) {
                value = value.replace(/(\d{5})(\d)/, '$1-$2');
            } else if (value.length > 6) {
                value = value.replace(/(\d{4})(\d)/, '$1-$2');
            }
            e.target.value = value;
        });
    },

// validação em tempo real
    adicionarValidacaoTemporal(input, funcaoValidacao, mensagemErro) {
        input.addEventListener('blur', function() {
            const valor = this.value;
            if (valor && !funcaoValidacao(valor)) {
                this.setCustomValidity(mensagemErro);
                this.classList.add('is-invalid');
                this.classList.remove('is-valid');
            } else if (valor) {
                this.setCustomValidity('');
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            } else {
                this.setCustomValidity('');
                this.classList.remove('is-invalid', 'is-valid');
            }
        });
        
        input.addEventListener('input', function() {
            if (this.classList.contains('is-invalid') || this.classList.contains('is-valid')) {
                const valor = this.value;
                if (valor && !funcaoValidacao(valor)) {
                    this.setCustomValidity(mensagemErro);
                    this.classList.add('is-invalid');
                    this.classList.remove('is-valid');
                } else if (valor) {
                    this.setCustomValidity('');
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                } else {
                    this.setCustomValidity('');
                    this.classList.remove('is-invalid', 'is-valid');
                }
            }
        });
    },


    configurarValidacaoFormulario(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    }
};

// uso global
if (typeof window !== 'undefined') {
    window.ValidationService = ValidationService;
}
