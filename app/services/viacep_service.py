# app/services/viacep_service.py
import requests
from typing import Optional, Dict, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class ViaCepResult:
    """Encapsula resultado da consulta à API ViaCEP"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error_message: str = ""

class ViaCepService:
    """
    Serviço responsável por integração com a API ViaCEP
    Fornece métodos para buscar endereços por CEP
    """
    
    BASE_URL = "https://viacep.com.br/ws"
    
    @staticmethod
    def get_address_by_cep(cep: str) -> ViaCepResult:
        """
        Busca endereço na API ViaCEP pelo CEP
        
        Args:
            cep: CEP no formato 00000-000 ou 00000000
            
        Returns:
            ViaCepResult com os dados do endereço ou erro
        """
        try:
            # Remove formatação do CEP (hífens, espaços)
            clean_cep = ViaCepService._clean_cep(cep)
            
            # Valida formato do CEP
            if not ViaCepService._validate_cep(clean_cep):
                return ViaCepResult(
                    success=False,
                    error_message="CEP deve conter exatamente 8 dígitos"
                )
            
            # Faz requisição à API
            url = f"{ViaCepService.BASE_URL}/{clean_cep}/json/"
            response = requests.get(url, timeout=10)
            
            # Verifica se a requisição foi bem-sucedida
            response.raise_for_status()
            
            # Converte resposta para JSON
            data = response.json()
            
            # Verifica se o CEP foi encontrado
            if "erro" in data:
                return ViaCepResult(
                    success=False,
                    error_message="CEP não encontrado"
                )
            
            # Formata dados do endereço
            formatted_data = ViaCepService._format_address_data(data)
            
            return ViaCepResult(
                success=True,
                data=formatted_data
            )
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout ao consultar CEP: {cep}")
            return ViaCepResult(
                success=False,
                error_message="Tempo limite excedido ao consultar CEP"
            )
            
        except requests.exceptions.ConnectionError:
            logger.error(f"Erro de conexão ao consultar CEP: {cep}")
            return ViaCepResult(
                success=False,
                error_message="Erro de conexão com o serviço de CEP"
            )
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição para CEP {cep}: {str(e)}")
            return ViaCepResult(
                success=False,
                error_message="Erro ao consultar CEP"
            )
            
        except Exception as e:
            logger.error(f"Erro inesperado ao consultar CEP {cep}: {str(e)}")
            return ViaCepResult(
                success=False,
                error_message="Erro interno do sistema"
            )
    
    @staticmethod
    def _clean_cep(cep: str) -> str:
        """Remove formatação do CEP"""
        if not cep:
            return ""
        return "".join(char for char in cep if char.isdigit())
    
    @staticmethod
    def _validate_cep(cep: str) -> bool:
        """Valida formato do CEP"""
        return len(cep) == 8 and cep.isdigit()
    
    @staticmethod
    def _format_address_data(data: Dict[str, Any]) -> Dict[str, str]:
        """
        Formata dados do endereço retornados pela API
        
        Args:
            data: Dados retornados pela API ViaCEP
            
        Returns:
            Dicionário com dados formatados
        """
        return {
            "cep": data.get("cep", ""),
            "logradouro": data.get("logradouro", ""),
            "complemento": data.get("complemento", ""),
            "bairro": data.get("bairro", ""),
            "localidade": data.get("localidade", ""),  # cidade
            "uf": data.get("uf", ""),  # estado
            "ibge": data.get("ibge", ""),
            "gia": data.get("gia", ""),
            "ddd": data.get("ddd", ""),
            "siafi": data.get("siafi", "")
        }
    
    @staticmethod
    def format_address_string(address_data: Dict[str, str], include_number: bool = True) -> str:
        """
        Cria string de endereço formatada a partir dos dados do ViaCEP
        
        Args:
            address_data: Dados do endereço do ViaCEP
            include_number: Se deve incluir espaço para número
            
        Returns:
            String formatada do endereço
        """
        parts = []
        
        logradouro = address_data.get("logradouro", "").strip()
        if logradouro:
            parts.append(logradouro)
            if include_number:
                parts.append("(número)")
        
        complemento = address_data.get("complemento", "").strip()
        if complemento:
            parts.append(complemento)
        
        bairro = address_data.get("bairro", "").strip()
        if bairro:
            parts.append(bairro)
        
        return ", ".join(parts) if parts else ""
