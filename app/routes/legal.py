from flask import Blueprint, render_template

# Criar blueprint para páginas legais
legal_bp = Blueprint('legal', __name__)

@legal_bp.route('/politica-privacidade')
def privacy_policy():
    """Página da Política de Privacidade"""
    return render_template('legal/privacy_policy.html')

@legal_bp.route('/termos-uso')
def terms_of_use():
    """Página dos Termos de Uso"""
    return render_template('legal/terms_of_use.html')

@legal_bp.route('/politica-cookies')
def cookie_policy():
    """Página da Política de Cookies"""
    return render_template('legal/cookie_policy.html')
