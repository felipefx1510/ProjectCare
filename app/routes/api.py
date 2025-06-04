# app/routes/api.py
from flask import Blueprint, jsonify, request
from app.services.viacep_service import ViaCepService

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/cep/<cep>", methods=["GET"])
def get_cep(cep):
    """
    Endpoint para consulta de CEP via API ViaCEP
    
    Args:
        cep: CEP a ser consultado
        
    Returns:
        JSON com dados do endereço ou erro
    """
    try:
        result = ViaCepService.get_address_by_cep(cep)
        
        if result.success:
            return jsonify({
                "success": True,
                "data": result.data
            })
        else:
            return jsonify({
                "success": False,
                "error": result.error_message
            }), 400
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500

@api_bp.route("/cep", methods=["POST"])
def post_cep():
    """
    Endpoint alternativo para consulta de CEP via POST
    
    Expected JSON:
        {"cep": "00000-000"}
        
    Returns:
        JSON com dados do endereço ou erro
    """
    try:
        data = request.get_json()
        
        if not data or "cep" not in data:
            return jsonify({
                "success": False,
                "error": "CEP é obrigatório"
            }), 400
        
        cep = data["cep"]
        result = ViaCepService.get_address_by_cep(cep)
        
        if result.success:
            return jsonify({
                "success": True,
                "data": result.data
            })
        else:
            return jsonify({
                "success": False,
                "error": result.error_message
            }), 400
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500
