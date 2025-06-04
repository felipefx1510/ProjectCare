// app/static/js/cep.js
/**
 * Funcionalidades relacionadas à consulta de CEP via ViaCEP
 */

class CepService {
    constructor() {
        this.isLoading = false;
    }

    /**
     * Consulta CEP na API interna do projeto
     * @param {string} cep - CEP a ser consultado
     * @returns {Promise<Object>} Dados do endereço ou erro
     */
    async consultarCep(cep) {
        try {
            const cleanCep = this.limparCep(cep);
            
            if (!this.validarCep(cleanCep)) {
                throw new Error('CEP deve conter exatamente 8 dígitos');
            }

            this.isLoading = true;
            
            const response = await fetch(`/api/cep/${cleanCep}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Erro ao consultar CEP');
            }

            return data.data;

        } catch (error) {
            console.error('Erro ao consultar CEP:', error);
            throw error;
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Remove formatação do CEP
     * @param {string} cep - CEP com ou sem formatação
     * @returns {string} CEP apenas com números
     */
    limparCep(cep) {
        return cep ? cep.replace(/\D/g, '') : '';
    }

    /**
     * Valida formato do CEP
     * @param {string} cep - CEP a ser validado
     * @returns {boolean} True se válido
     */
    validarCep(cep) {
        return /^\d{8}$/.test(cep);
    }

    /**
     * Formata CEP com hífen
     * @param {string} cep - CEP sem formatação
     * @returns {string} CEP formatado
     */
    formatarCep(cep) {
        const cleanCep = this.limparCep(cep);
        if (cleanCep.length === 8) {
            return `${cleanCep.substring(0, 5)}-${cleanCep.substring(5)}`;
        }
        return cleanCep;
    }

    /**
     * Configura máscara de CEP em um campo input
     * @param {HTMLElement} input - Campo de input
     */
    aplicarMascaraCep(input) {
        input.addEventListener('input', (e) => {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 8) {
                value = value.slice(0, 8);
            }
            if (value.length > 5) {
                value = value.replace(/(\d{5})(\d)/, '$1-$2');
            }
            e.target.value = value;
        });
    }

    /**
     * Preenche campos de endereço automaticamente após consulta de CEP
     * @param {Object} enderecoData - Dados do endereço do ViaCEP
     * @param {Object} campos - Objeto com seletores dos campos
     */
    preencherEndereco(enderecoData, campos) {
        try {
            if (campos.logradouro && enderecoData.logradouro) {
                const logradouroField = document.querySelector(campos.logradouro);
                if (logradouroField) {
                    logradouroField.value = enderecoData.logradouro;
                }
            }

            if (campos.bairro && enderecoData.bairro) {
                const bairroField = document.querySelector(campos.bairro);
                if (bairroField) {
                    bairroField.value = enderecoData.bairro;
                }
            }

            if (campos.cidade && enderecoData.localidade) {
                const cidadeField = document.querySelector(campos.cidade);
                if (cidadeField) {
                    cidadeField.value = enderecoData.localidade;
                }
            }

            if (campos.estado && enderecoData.uf) {
                const estadoField = document.querySelector(campos.estado);
                if (estadoField) {
                    estadoField.value = enderecoData.uf;
                }
            }

            if (campos.endereco && enderecoData.logradouro) {
                const enderecoField = document.querySelector(campos.endereco);
                if (enderecoField) {
                    // Cria endereço completo com logradouro e bairro
                    let enderecoCompleto = enderecoData.logradouro;
                    if (enderecoData.bairro) {
                        enderecoCompleto += `, ${enderecoData.bairro}`;
                    }
                    enderecoField.value = enderecoCompleto;
                }
            }
        } catch (error) {
            console.error('Erro ao preencher campos de endereço:', error);
        }
    }

    /**
     * Mostra indicador de carregamento
     * @param {HTMLElement} button - Botão ou elemento onde mostrar loading
     */
    mostrarCarregamento(button) {
        if (button) {
            button.disabled = true;
            const originalText = button.textContent;
            button.setAttribute('data-original-text', originalText);
            button.innerHTML = '<i class="bi bi-arrow-clockwise spin"></i> Buscando...';
        }
    }

    /**
     * Esconde indicador de carregamento
     * @param {HTMLElement} button - Botão onde esconder loading
     */
    esconderCarregamento(button) {
        if (button) {
            button.disabled = false;
            const originalText = button.getAttribute('data-original-text');
            if (originalText) {
                button.textContent = originalText;
                button.removeAttribute('data-original-text');
            }
        }
    }

    /**
     * Mostra mensagem de erro
     * @param {string} message - Mensagem de erro
     * @param {HTMLElement} container - Container onde exibir erro
     */
    mostrarErro(message, container) {
        if (container) {
            container.innerHTML = `
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <i class="bi bi-exclamation-triangle-fill me-2"></i>
                    ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
        }
    }

    /**
     * Mostra mensagem de sucesso
     * @param {string} message - Mensagem de sucesso
     * @param {HTMLElement} container - Container onde exibir sucesso
     */
    mostrarSucesso(message, container) {
        if (container) {
            container.innerHTML = `
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    <i class="bi bi-check-circle-fill me-2"></i>
                    ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
        }
    }
}

// CSS para animação de loading
const style = document.createElement('style');
style.textContent = `
    .spin {
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);

// Instância global do serviço
window.cepService = new CepService();
