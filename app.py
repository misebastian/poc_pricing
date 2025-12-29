"""
ACERO INDUSTRIAL - Sistema de Optimización de Precios
Aplicación Streamlit con presentación y herramienta de cotización
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =============================================================================
# CONFIGURACIÓN DE PÁGINA
# =============================================================================
st.set_page_config(
    page_title="Acero Industrial - Optimización de Precios",
    page_icon="🔩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# ESTILOS CSS PERSONALIZADOS
# =============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Crimson+Pro:wght@300;600;900&display=swap');
    
    /* Fondo principal */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 3px solid #10b981;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #f1f5f9;
    }
    
    /* Títulos principales */
    .main-title {
        font-family: 'Crimson Pro', serif;
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(to right, #10b981, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        font-family: 'Space Mono', monospace;
        font-size: 1.25rem;
        color: #94a3b8;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }
    
    /* Tarjetas de métricas */
    .metric-card {
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 1rem;
    }
    
    .metric-card-green {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
    }
    
    .metric-card-blue {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
    }
    
    .metric-card-orange {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.3);
    }
    
    .metric-card-purple {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);
    }
    
    .metric-label {
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        opacity: 0.9;
        color: white;
    }
    
    .metric-value {
        font-family: 'Crimson Pro', serif;
        font-size: 2.5rem;
        font-weight: bold;
        color: white;
    }
    
    .metric-subtitle {
        font-size: 0.875rem;
        opacity: 0.8;
        color: white;
    }
    
    /* Slide container */
    .slide-container {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid #334155;
        border-radius: 1rem;
        padding: 2.5rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        margin-bottom: 2rem;
    }
    
    .slide-title {
        font-family: 'Crimson Pro', serif;
        font-size: 2.5rem;
        color: #10b981;
        font-weight: 600;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid #10b981;
        padding-bottom: 0.5rem;
    }
    
    .slide-number {
        font-family: 'Space Mono', monospace;
        font-size: 0.875rem;
        color: #94a3b8;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    
    .slide-content {
        font-family: 'Space Mono', monospace;
        color: #cbd5e1;
        line-height: 1.8;
    }
    
    .slide-content h3 {
        color: #3b82f6;
        font-family: 'Crimson Pro', serif;
        margin-top: 1.5rem;
    }
    
    .slide-content ul {
        list-style-type: none;
        padding-left: 0;
    }
    
    .slide-content li {
        padding: 0.5rem 0;
        padding-left: 1.5rem;
        position: relative;
    }
    
    .slide-content li::before {
        content: "→";
        position: absolute;
        left: 0;
        color: #10b981;
    }
    
    /* Highlight box */
    .highlight-box {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid #10b981;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .highlight-box-warning {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid #f59e0b;
    }
    
    .highlight-box-danger {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid #ef4444;
    }
    
    /* Data table styling */
    .data-table {
        background: rgba(30, 41, 59, 0.6);
        border-radius: 0.5rem;
        overflow: hidden;
    }
    
    /* Form inputs */
    .stSelectbox > div > div {
        background: #1e293b;
        border: 2px solid #475569;
        color: #f1f5f9;
    }
    
    .stNumberInput > div > div > input {
        background: #1e293b;
        border: 2px solid #475569;
        color: #f1f5f9;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        font-family: 'Space Mono', monospace;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        border: none;
        border-radius: 0.75rem;
        padding: 0.75rem 2rem;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.4);
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 40px rgba(16, 185, 129, 0.5);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom text colors */
    .text-emerald { color: #10b981; }
    .text-blue { color: #3b82f6; }
    .text-slate { color: #94a3b8; }
    .text-white { color: #f1f5f9; }
    
</style>
""", unsafe_allow_html=True)

# =============================================================================
# DATOS Y CONFIGURACIÓN
# =============================================================================

# Guardrails de precios por tier (derivados del análisis)
TIER_RULES = {
    'Standard': {'target': 5.9, 'ceiling': 9.1, 'hard_max': 14.2, 'margin_floor': 14.4},
    'Bronze': {'target': 8.5, 'ceiling': 12.1, 'hard_max': 16.0, 'margin_floor': 12.8},
    'Silver': {'target': 10.9, 'ceiling': 14.4, 'hard_max': 18.2, 'margin_floor': 10.4},
    'Gold': {'target': 14.7, 'ceiling': 17.9, 'hard_max': 23.0, 'margin_floor': 6.7},
    'Platinum': {'target': 17.9, 'ceiling': 21.0, 'hard_max': 26.5, 'margin_floor': 1.4}
}

# Ajustes por categoría
CATEGORY_ADJ = {
    'Flat': -0.1,
    'Long': 0.1,
    'Tubular': -0.15,
    'Processed': 0.0
}

# Ajustes por segmento
SEGMENT_ADJ = {
    'Manufacturing': 0.1,
    'Construction': -0.2,
    'Other': 0.15
}

# Ajustes regionales
REGION_ADJ = {
    'Bogota': -0.3,
    'Antioquia': -0.3,
    'Valle': 0.1,
    'Costa': 0.8,
    'Ecuador': 0.5,
    'Panama': -0.2
}

# Productos de ejemplo
PRODUCTS = {
    'P1000': {'name': 'Lámina HR A36', 'category': 'Flat', 'list_price': 2100, 'cost': 1700},
    'P1001': {'name': 'Lámina CR 1018', 'category': 'Flat', 'list_price': 2400, 'cost': 1950},
    'P1002': {'name': 'Varilla Corrugada', 'category': 'Long', 'list_price': 1500, 'cost': 1200},
    'P1003': {'name': 'Perfil Estructural', 'category': 'Long', 'list_price': 2800, 'cost': 2300},
    'P1004': {'name': 'Tubo Redondo', 'category': 'Tubular', 'list_price': 1800, 'cost': 1450},
    'P1005': {'name': 'Tubo Cuadrado', 'category': 'Tubular', 'list_price': 1950, 'cost': 1580},
    'P1006': {'name': 'Placa Cortada', 'category': 'Processed', 'list_price': 3200, 'cost': 2600}
}

# Clientes de ejemplo
CUSTOMERS = {
    'C5001': {'name': 'Construcciones Andinas S.A.', 'segment': 'Construction', 'tier': 'Gold', 'region': 'Bogota'},
    'C5002': {'name': 'Metalmecánica del Norte', 'segment': 'Manufacturing', 'tier': 'Silver', 'region': 'Antioquia'},
    'C5003': {'name': 'Estructuras Costa Caribe', 'segment': 'Construction', 'tier': 'Bronze', 'region': 'Costa'},
    'C5004': {'name': 'Industrial Pacífico', 'segment': 'Manufacturing', 'tier': 'Platinum', 'region': 'Valle'},
    'C5005': {'name': 'Ferretería El Constructor', 'segment': 'Other', 'tier': 'Standard', 'region': 'Bogota'},
    'C5006': {'name': 'Proyectos Ecuador', 'segment': 'Construction', 'tier': 'Silver', 'region': 'Ecuador'},
    'C5007': {'name': 'Panama Steel Works', 'segment': 'Manufacturing', 'tier': 'Gold', 'region': 'Panama'}
}

# =============================================================================
# FUNCIONES DE CÁLCULO
# =============================================================================

def calculate_price_guidance(customer_id, product_id, quantity):
    """Calcula la guía de precios basada en reglas."""
    customer = CUSTOMERS[customer_id]
    product = PRODUCTS[product_id]
    tier_rule = TIER_RULES[customer['tier']]
    
    # Calcular descuento objetivo ajustado
    base_target = tier_rule['target']
    cat_adj = CATEGORY_ADJ.get(product['category'], 0)
    seg_adj = SEGMENT_ADJ.get(customer['segment'], 0)
    reg_adj = REGION_ADJ.get(customer['region'], 0)
    
    adjusted_target = base_target + cat_adj + seg_adj + reg_adj
    
    # Calcular precios
    list_price = product['list_price']
    cost = product['cost']
    
    target_price = list_price * (1 - adjusted_target / 100)
    ceiling_price = list_price * (1 - tier_rule['ceiling'] / 100)
    floor_price = cost / (1 - tier_rule['margin_floor'] / 100)
    
    # Calcular métricas
    target_margin = (target_price - cost) / target_price * 100
    target_margin_total = (target_price - cost) * quantity
    
    return {
        'list_price': list_price,
        'cost': cost,
        'target_discount': adjusted_target,
        'ceiling_discount': tier_rule['ceiling'],
        'hard_max_discount': tier_rule['hard_max'],
        'margin_floor': tier_rule['margin_floor'],
        'target_price': target_price,
        'ceiling_price': ceiling_price,
        'floor_price': floor_price,
        'target_margin_pct': target_margin,
        'target_margin_total': target_margin_total,
        'customer': customer,
        'product': product,
        'tier_rule': tier_rule,
        'adjustments': {
            'category': cat_adj,
            'segment': seg_adj,
            'region': reg_adj
        }
    }


def evaluate_quote(quoted_price, guidance):
    """Evalúa una cotización contra las reglas."""
    discount = (1 - quoted_price / guidance['list_price']) * 100
    margin = (quoted_price - guidance['cost']) / quoted_price * 100
    
    if margin < guidance['margin_floor']:
        status = 'RED'
        message = 'Violación de margen mínimo - Requiere aprobación VP'
        color = '#ef4444'
    elif discount <= guidance['target_discount']:
        status = 'GREEN'
        message = 'Dentro del objetivo - Aprobación automática'
        color = '#10b981'
    elif discount <= guidance['ceiling_discount']:
        status = 'YELLOW'
        message = 'Por encima del objetivo - Notificación a gerente'
        color = '#f59e0b'
    elif discount <= guidance['hard_max_discount']:
        status = 'ORANGE'
        message = 'Por encima del techo - Requiere aprobación gerente'
        color = '#f97316'
    else:
        status = 'RED'
        message = 'Excede máximo - Requiere aprobación VP'
        color = '#ef4444'
    
    return {
        'status': status,
        'message': message,
        'color': color,
        'discount': discount,
        'margin': margin
    }


def simulate_scenarios(guidance, quantity):
    """Simula escenarios de precio para el gráfico."""
    scenarios = []
    for discount in np.arange(0, 30, 0.5):
        price = guidance['list_price'] * (1 - discount / 100)
        margin_per_unit = price - guidance['cost']
        margin_pct = margin_per_unit / price * 100 if price > 0 else 0
        
        # Simular probabilidad de ganar (simplificada)
        if discount < 5:
            win_prob = 0.65 + (5 - discount) * 0.02
        elif discount <= 15:
            win_prob = 0.85 - (discount - 5) * 0.01
        else:
            win_prob = max(0.35, 0.85 - (discount - 5) * 0.03)
        
        win_prob = max(0.15, min(0.95, win_prob))
        
        total_margin = margin_per_unit * quantity
        expected_margin = win_prob * total_margin
        
        scenarios.append({
            'discount': discount,
            'price': price,
            'margin_pct': margin_pct,
            'win_prob': win_prob * 100,
            'total_margin': total_margin,
            'expected_margin': expected_margin
        })
    
    return pd.DataFrame(scenarios)


# =============================================================================
# SIDEBAR - NAVEGACIÓN
# =============================================================================

st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem 0; border-bottom: 2px solid #10b981; margin-bottom: 2rem;">
    <h1 style="font-family: 'Crimson Pro', serif; font-size: 2rem; color: #10b981; margin: 0;">
        Acero Industrial
    </h1>
    <p style="font-family: 'Space Mono', monospace; font-size: 0.75rem; color: #94a3b8; margin: 0.5rem 0 0; letter-spacing: 0.1em;">
        OPTIMIZACIÓN DE PRECIOS
    </p>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navegación",
    ["01. Presentación", "02. Problema de Endogeneidad", "03. Confiabilidad del Outcome", 
     "04. Reglas vs ML", "05. Sistema de Guardrails", "06. Herramienta de Cotización"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-family: 'Space Mono', monospace; font-size: 0.75rem; color: #64748b; padding: 1rem 0;">
    <p><strong style="color: #10b981;">RevSeekr</strong></p>
    <p>Case Study: Acero Industrial</p>
    <p>Pricing Optimization Assessment</p>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# PÁGINA 1: PRESENTACIÓN
# =============================================================================

if page == "01. Presentación":
    st.markdown('<p class="main-title">Acero Industrial</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Evaluación de Preparación de Datos para Optimización de Precios</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="slide-container">
            <p class="slide-number">Slide 01 / 06</p>
            <h2 class="slide-title">Resumen Ejecutivo</h2>
            <div class="slide-content">
                <h3>Contexto del Proyecto</h3>
                <ul>
                    <li>Distribuidor de acero colombiano con $185M en ingresos</li>
                    <li>Margen actual: 18.2% vs objetivo: 20%</li>
                    <li>823 clientes, 4,847 SKUs, 42 representantes de ventas</li>
                    <li>Sistema PriceFx implementado pero sin optimización</li>
                </ul>
                
                <h3>Hallazgo Principal</h3>
                <div class="highlight-box">
                    <strong style="color: #10b981;">Los datos reflejan comportamiento PRE-OPTIMIZACIÓN.</strong><br>
                    Entrenar un modelo ML replicaría las ineficiencias actuales, no las corregiría.
                </div>
                
                <h3>Recomendación</h3>
                <ul>
                    <li>Implementar guardrails basados en reglas (no ML)</li>
                    <li>Validar con pruebas A/B controladas</li>
                    <li>Reconsiderar ML solo después de datos limpios experimentales</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Métricas clave
        st.markdown("""
        <div class="metric-card metric-card-green">
            <p class="metric-label">Transacciones Analizadas</p>
            <p class="metric-value">5,000</p>
            <p class="metric-subtitle">12 meses de datos</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card metric-card-blue">
            <p class="metric-label">Segmentos de Cliente</p>
            <p class="metric-value">52</p>
            <p class="metric-subtitle">Combinaciones únicas</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card metric-card-orange">
            <p class="metric-label">Discrepancia Win Rate</p>
            <p class="metric-value">40pp</p>
            <p class="metric-subtitle">75% observado vs 35% reportado</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card metric-card-purple">
            <p class="metric-label">Score de Preparación</p>
            <p class="metric-value">76%</p>
            <p class="metric-subtitle">Grado C - Limitaciones para ML</p>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# PÁGINA 2: ENDOGENEIDAD
# =============================================================================

elif page == "02. Problema de Endogeneidad":
    st.markdown('<p class="slide-number">Slide 02 / 06</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="slide-title">El Problema de Endogeneidad</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="slide-container">
            <h3 style="color: #3b82f6; font-family: 'Crimson Pro', serif;">¿Qué es la Endogeneidad?</h3>
            <div class="slide-content">
                <p>La endogeneidad ocurre cuando la variable explicativa (descuento) está correlacionada 
                con el término de error en la ecuación de resultado.</p>
                
                <div class="highlight-box-warning">
                    <strong style="color: #f59e0b;">Observación Clave:</strong><br>
                    Los deals perdidos tienen descuentos MÁS ALTOS que los ganados.
                </div>
                
                <h4 style="color: #10b981;">Evidencia Estadística:</h4>
                <ul>
                    <li>Descuento promedio en deals ganados: <strong>8.31%</strong></li>
                    <li>Descuento promedio en deals perdidos: <strong>10.87%</strong></li>
                    <li>Diferencia: <strong>2.56pp</strong></li>
                    <li>T-test: t=-12.0, p < 10⁻³¹</li>
                    <li>Cohen's d: 0.457 (efecto medio)</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Gráfico de win rate por cuartil de descuento
        quartile_data = pd.DataFrame({
            'Cuartil': ['Q1 (Bajo)', 'Q2', 'Q3', 'Q4 (Alto)'],
            'Descuento Promedio': [2.8, 6.7, 10.0, 16.3],
            'Win Rate': [80.5, 80.5, 78.9, 61.1]
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Win Rate %',
            x=quartile_data['Cuartil'],
            y=quartile_data['Win Rate'],
            marker_color=['#10b981', '#10b981', '#f59e0b', '#ef4444'],
            text=[f"{v:.1f}%" for v in quartile_data['Win Rate']],
            textposition='outside',
            textfont=dict(size=14, color='white')
        ))
        
        fig.update_layout(
            title=dict(
                text='Win Rate por Cuartil de Descuento',
                font=dict(size=20, color='#10b981', family='Crimson Pro')
            ),
            xaxis_title='Cuartil de Descuento',
            yaxis_title='Win Rate (%)',
            plot_bgcolor='rgba(30, 41, 59, 0.6)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1', family='Space Mono'),
            yaxis=dict(range=[0, 100], gridcolor='#334155'),
            xaxis=dict(gridcolor='#334155'),
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="slide-container">
        <h3 style="color: #ef4444; font-family: 'Crimson Pro', serif;">El Mecanismo de Selección</h3>
        <div class="slide-content">
            <div class="highlight-box-danger">
                <strong>Modelo de Decisión del Representante:</strong>
                <ol style="padding-left: 1.5rem; margin-top: 1rem;">
                    <li><strong>Observa señales</strong> sobre dificultad del deal (competencia, urgencia, relación)</li>
                    <li><strong>Forma creencia</strong> sobre probabilidad de ganar: P(Win | señales)</li>
                    <li><strong>Ajusta descuento</strong>: Si P(Win) es BAJA → Mayor descuento para "salvar" el deal</li>
                    <li><strong>Resultado determinado</strong> por dificultad real + precio + factores aleatorios</li>
                </ol>
                
                <p style="margin-top: 1rem;"><strong>Consecuencia:</strong></p>
                <p>Observamos: Alto descuento → Bajo win rate</p>
                <p>Pero la causalidad es: Alta dificultad → Alto descuento Y Bajo win rate</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# PÁGINA 3: CONFIABILIDAD DEL OUTCOME
# =============================================================================

elif page == "03. Confiabilidad del Outcome":
    st.markdown('<p class="slide-number">Slide 03 / 06</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="slide-title">Confiabilidad de la Variable de Resultado</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="slide-container">
            <h3 style="color: #ef4444; font-family: 'Crimson Pro', serif;">Discrepancia Crítica</h3>
            <div class="slide-content">
                <div class="highlight-box-danger">
                    <table style="width: 100%; color: white;">
                        <tr>
                            <td><strong>Win Rate Observado:</strong></td>
                            <td style="text-align: right; font-size: 1.5rem;">75.3%</td>
                        </tr>
                        <tr>
                            <td><strong>Win Rate Case Brief:</strong></td>
                            <td style="text-align: right; font-size: 1.5rem;">35%</td>
                        </tr>
                        <tr style="border-top: 2px solid #ef4444;">
                            <td><strong>Discrepancia:</strong></td>
                            <td style="text-align: right; font-size: 1.5rem; color: #ef4444;">40.3pp</td>
                        </tr>
                    </table>
                </div>
                
                <h4 style="color: #f59e0b; margin-top: 1.5rem;">Posibles Explicaciones:</h4>
                <ul>
                    <li><strong>Quote vs Opportunity:</strong> Múltiples cotizaciones por oportunidad</li>
                    <li><strong>Re-quoted ambiguo:</strong> 15.8% de datos sin clasificar claramente</li>
                    <li><strong>Sesgo de selección:</strong> Datos pueden excluir pérdidas históricas</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Gráfico de distribución de outcomes
        outcome_data = pd.DataFrame({
            'Resultado': ['Won', 'Lost', 'Re-quoted'],
            'Cantidad': [3167, 1041, 792],
            'Porcentaje': [63.3, 20.8, 15.8]
        })
        
        fig = go.Figure(data=[go.Pie(
            labels=outcome_data['Resultado'],
            values=outcome_data['Cantidad'],
            hole=0.5,
            marker_colors=['#10b981', '#ef4444', '#f59e0b'],
            textinfo='label+percent',
            textfont=dict(size=14, color='white')
        )])
        
        fig.update_layout(
            title=dict(
                text='Distribución de Resultados',
                font=dict(size=20, color='#10b981', family='Crimson Pro')
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1', family='Space Mono'),
            height=350,
            showlegend=True,
            legend=dict(
                font=dict(color='#cbd5e1'),
                bgcolor='rgba(0,0,0,0)'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="slide-container">
        <h3 style="color: #3b82f6; font-family: 'Crimson Pro', serif;">Análisis de Transacciones Re-quoted</h3>
        <div class="slide-content">
            <p>Las transacciones Re-quoted (15.8%) son más similares a <strong style="color: #10b981;">Won</strong> que a <strong style="color: #ef4444;">Lost</strong>:</p>
            
            <table style="width: 100%; margin-top: 1rem; border-collapse: collapse;">
                <tr style="border-bottom: 2px solid #334155;">
                    <th style="text-align: left; padding: 0.75rem; color: #94a3b8;">Métrica</th>
                    <th style="text-align: center; padding: 0.75rem; color: #10b981;">Won</th>
                    <th style="text-align: center; padding: 0.75rem; color: #ef4444;">Lost</th>
                    <th style="text-align: center; padding: 0.75rem; color: #f59e0b;">Re-quoted</th>
                </tr>
                <tr style="border-bottom: 1px solid #334155;">
                    <td style="padding: 0.75rem;">Descuento Promedio</td>
                    <td style="text-align: center; padding: 0.75rem;">8.31%</td>
                    <td style="text-align: center; padding: 0.75rem;">10.87%</td>
                    <td style="text-align: center; padding: 0.75rem;">7.74%</td>
                </tr>
                <tr>
                    <td style="padding: 0.75rem;">Margen Promedio</td>
                    <td style="text-align: center; padding: 0.75rem;">18.26%</td>
                    <td style="text-align: center; padding: 0.75rem;">15.33%</td>
                    <td style="text-align: center; padding: 0.75rem;">18.82%</td>
                </tr>
            </table>
            
            <div class="highlight-box" style="margin-top: 1.5rem;">
                <strong style="color: #10b981;">Implicación:</strong> No se puede entrenar un modelo confiable de probabilidad de ganar 
                hasta resolver la definición de outcome y la discrepancia de 40pp.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# PÁGINA 4: REGLAS VS ML
# =============================================================================

elif page == "04. Reglas vs ML":
    st.markdown('<p class="slide-number">Slide 04 / 06</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="slide-title">Enfoque Basado en Reglas vs Machine Learning</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="slide-container">
            <h3 style="color: #10b981; font-family: 'Crimson Pro', serif;">Scores de Factibilidad</h3>
            <div class="slide-content">
                <table style="width: 100%; border-collapse: collapse;">
                    <tr style="border-bottom: 2px solid #10b981;">
                        <th style="text-align: left; padding: 0.75rem; color: #94a3b8;">Enfoque</th>
                        <th style="text-align: center; padding: 0.75rem; color: #94a3b8;">Score</th>
                        <th style="text-align: center; padding: 0.75rem; color: #94a3b8;">Status</th>
                    </tr>
                    <tr style="border-bottom: 1px solid #334155;">
                        <td style="padding: 0.75rem;">Basado en Reglas</td>
                        <td style="text-align: center; padding: 0.75rem; font-size: 1.25rem; color: #10b981;"><strong>90/100</strong></td>
                        <td style="text-align: center; padding: 0.75rem;">✅ Recomendado</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #334155;">
                        <td style="padding: 0.75rem;">ML Tradicional</td>
                        <td style="text-align: center; padding: 0.75rem; font-size: 1.25rem; color: #f59e0b;"><strong>47/100</strong></td>
                        <td style="text-align: center; padding: 0.75rem;">⚠️ No recomendado</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #334155;">
                        <td style="padding: 0.75rem;">Reinforcement Learning</td>
                        <td style="text-align: center; padding: 0.75rem; font-size: 1.25rem; color: #ef4444;"><strong>40/100</strong></td>
                        <td style="text-align: center; padding: 0.75rem;">❌ No factible</td>
                    </tr>
                    <tr>
                        <td style="padding: 0.75rem;">ML Causal</td>
                        <td style="text-align: center; padding: 0.75rem; font-size: 1.25rem; color: #ef4444;"><strong>25/100</strong></td>
                        <td style="text-align: center; padding: 0.75rem;">❌ No factible</td>
                    </tr>
                </table>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Gráfico de barras horizontal para scores
        score_data = pd.DataFrame({
            'Enfoque': ['Basado en Reglas', 'ML Tradicional', 'Reinforcement Learning', 'ML Causal'],
            'Score': [90, 47, 40, 25]
        })
        
        fig = go.Figure(go.Bar(
            x=score_data['Score'],
            y=score_data['Enfoque'],
            orientation='h',
            marker_color=['#10b981', '#f59e0b', '#ef4444', '#ef4444'],
            text=[f"{s}/100" for s in score_data['Score']],
            textposition='inside',
            textfont=dict(size=16, color='white')
        ))
        
        fig.update_layout(
            title=dict(
                text='Factibilidad por Enfoque',
                font=dict(size=20, color='#10b981', family='Crimson Pro')
            ),
            xaxis_title='Score de Factibilidad',
            plot_bgcolor='rgba(30, 41, 59, 0.6)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1', family='Space Mono'),
            xaxis=dict(range=[0, 100], gridcolor='#334155'),
            yaxis=dict(gridcolor='#334155'),
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="slide-container">
        <h3 style="color: #3b82f6; font-family: 'Crimson Pro', serif;">¿Por qué ML no Puede Resolver la Endogeneidad?</h3>
        <div class="slide-content">
            <div class="highlight-box-warning">
                <strong style="color: #f59e0b;">Concepto Erróneo Común:</strong> "ML puede capturar patrones complejos que OLS pierde"
                
                <p style="margin-top: 1rem;"><strong>Realidad:</strong> Los algoritmos de ML son máquinas de correlación sofisticadas. NO pueden:</p>
                <ul style="margin-top: 0.5rem;">
                    <li>Distinguir correlación de causalidad</li>
                    <li>Estimar efectos de tratamiento de datos observacionales</li>
                    <li>Corregir sesgo por variable omitida</li>
                    <li>Identificar la dirección de causalidad</li>
                </ul>
            </div>
            
            <h4 style="color: #10b981; margin-top: 1.5rem;">Lo que un Modelo ML Aprendería:</h4>
            <p>"Cuando descuento > 15%, predecir pérdida"</p>
            <p>"Cuando descuento < 8%, predecir ganancia"</p>
            
            <p style="margin-top: 1rem;"><strong style="color: #ef4444;">Esto es CORRECTO para predicción pero INCORRECTO para optimización:</strong></p>
            <ul>
                <li>El modelo predice LO QUE PASÓ, no LO QUE PASARÍA</li>
                <li>Reducir descuento en un deal difícil no lo hace más fácil</li>
                <li>La dificultad es la CAUSA, el descuento es el SÍNTOMA</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# PÁGINA 5: SISTEMA DE GUARDRAILS
# =============================================================================

elif page == "05. Sistema de Guardrails":
    st.markdown('<p class="slide-number">Slide 05 / 06</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="slide-title">Arquitectura del Sistema de Guardrails</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="slide-container">
        <h3 style="color: #10b981; font-family: 'Crimson Pro', serif;">Diseño de Tres Capas</h3>
        <div class="slide-content" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem;">
            <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; border-radius: 0.75rem; padding: 1.5rem;">
                <h4 style="color: #10b981; margin-bottom: 1rem;">Capa 1: Matriz por Tier</h4>
                <p>Proporciona targets y guardrails base por tier de volumen del cliente.</p>
                <ul style="font-size: 0.9rem;">
                    <li>Descuento objetivo</li>
                    <li>Techo de descuento</li>
                    <li>Máximo absoluto</li>
                    <li>Piso de margen</li>
                </ul>
            </div>
            <div style="background: rgba(59, 130, 246, 0.1); border: 1px solid #3b82f6; border-radius: 0.75rem; padding: 1.5rem;">
                <h4 style="color: #3b82f6; margin-bottom: 1rem;">Capa 2: Ajustes Contextuales</h4>
                <p>Modifica targets basado en factores del deal.</p>
                <ul style="font-size: 0.9rem;">
                    <li>Categoría de producto</li>
                    <li>Segmento de cliente</li>
                    <li>Región geográfica</li>
                    <li>Situación competitiva</li>
                </ul>
            </div>
            <div style="background: rgba(139, 92, 246, 0.1); border: 1px solid #8b5cf6; border-radius: 0.75rem; padding: 1.5rem;">
                <h4 style="color: #8b5cf6; margin-bottom: 1rem;">Capa 3: Flujo de Aprobación</h4>
                <p>Lógica de escalación basada en desviación.</p>
                <ul style="font-size: 0.9rem;">
                    <li>🟢 GREEN: Auto-aprobación</li>
                    <li>🟡 YELLOW: Notificación</li>
                    <li>🟠 ORANGE: Aprobación gerente</li>
                    <li>🔴 RED: Aprobación VP</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabla de guardrails por tier
    st.markdown("""
    <div class="slide-container">
        <h3 style="color: #3b82f6; font-family: 'Crimson Pro', serif;">Guardrails por Tier de Volumen</h3>
    </div>
    """, unsafe_allow_html=True)
    
    guardrails_df = pd.DataFrame([
        {'Tier': 'Standard', 'N': 1689, 'Target': '5.9%', 'Techo': '9.1%', 'Máximo': '14.2%', 'Margen Mín': '14.4%'},
        {'Tier': 'Bronze', 'N': 748, 'Target': '8.5%', 'Techo': '12.1%', 'Máximo': '16.0%', 'Margen Mín': '12.8%'},
        {'Tier': 'Silver', 'N': 494, 'Target': '10.9%', 'Techo': '14.4%', 'Máximo': '18.2%', 'Margen Mín': '10.4%'},
        {'Tier': 'Gold', 'N': 191, 'Target': '14.7%', 'Techo': '17.9%', 'Máximo': '23.0%', 'Margen Mín': '6.7%'},
        {'Tier': 'Platinum', 'N': 45, 'Target': '17.9%', 'Techo': '21.0%', 'Máximo': '26.5%', 'Margen Mín': '1.4%'}
    ])
    
    st.dataframe(
        guardrails_df,
        use_container_width=True,
        hide_index=True
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="slide-container">
            <h4 style="color: #10b981;">Ajustes por Categoría</h4>
            <table style="width: 100%; border-collapse: collapse;">
                <tr><td style="padding: 0.5rem;">Flat</td><td style="text-align: right;">-0.10%</td></tr>
                <tr><td style="padding: 0.5rem;">Long</td><td style="text-align: right;">+0.10%</td></tr>
                <tr><td style="padding: 0.5rem;">Tubular</td><td style="text-align: right;">-0.15%</td></tr>
                <tr><td style="padding: 0.5rem;">Processed</td><td style="text-align: right;">+0.00%</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="slide-container">
            <h4 style="color: #3b82f6;">Ajustes por Segmento</h4>
            <table style="width: 100%; border-collapse: collapse;">
                <tr><td style="padding: 0.5rem;">Manufacturing</td><td style="text-align: right;">+0.10%</td></tr>
                <tr><td style="padding: 0.5rem;">Construction</td><td style="text-align: right;">-0.20%</td></tr>
                <tr><td style="padding: 0.5rem;">Other</td><td style="text-align: right;">+0.15%</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# PÁGINA 6: HERRAMIENTA DE COTIZACIÓN
# =============================================================================

elif page == "06. Herramienta de Cotización":
    st.markdown('<p class="slide-number">Slide 06 / 06</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="slide-title">Sistema de Cotización Inteligente</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div class="slide-container">
            <h3 style="color: #10b981; font-family: 'Crimson Pro', serif; font-size: 1.25rem;">Datos de la Cotización</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Selección de cliente
        customer_id = st.selectbox(
            "Cliente",
            options=list(CUSTOMERS.keys()),
            format_func=lambda x: f"{x} - {CUSTOMERS[x]['name']}"
        )
        
        # Mostrar info del cliente
        customer = CUSTOMERS[customer_id]
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.6); padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
            <p style="margin: 0; font-size: 0.875rem; color: #94a3b8;">
                <strong>Segmento:</strong> {customer['segment']}<br>
                <strong>Tier:</strong> {customer['tier']}<br>
                <strong>Región:</strong> {customer['region']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Selección de producto
        product_id = st.selectbox(
            "Producto",
            options=list(PRODUCTS.keys()),
            format_func=lambda x: f"{x} - {PRODUCTS[x]['name']}"
        )
        
        # Mostrar info del producto
        product = PRODUCTS[product_id]
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.6); padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
            <p style="margin: 0; font-size: 0.875rem; color: #94a3b8;">
                <strong>Categoría:</strong> {product['category']}<br>
                <strong>Precio Lista:</strong> ${product['list_price']:,.2f}<br>
                <strong>Costo:</strong> ${product['cost']:,.2f}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Cantidad
        quantity = st.number_input("Cantidad", min_value=1, value=100, step=10)
        
        # Botón para calcular
        if st.button("Calcular Guía de Precios", type="primary", use_container_width=True):
            st.session_state.guidance = calculate_price_guidance(customer_id, product_id, quantity)
            st.session_state.scenarios = simulate_scenarios(st.session_state.guidance, quantity)
    
    with col2:
        if 'guidance' in st.session_state:
            guidance = st.session_state.guidance
            scenarios = st.session_state.scenarios
            
            # Métricas principales
            metric_cols = st.columns(4)
            
            with metric_cols[0]:
                st.markdown(f"""
                <div class="metric-card metric-card-green">
                    <p class="metric-label">Precio Objetivo</p>
                    <p class="metric-value">${guidance['target_price']:,.0f}</p>
                    <p class="metric-subtitle">Descuento: {guidance['target_discount']:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_cols[1]:
                st.markdown(f"""
                <div class="metric-card metric-card-blue">
                    <p class="metric-label">Precio Techo</p>
                    <p class="metric-value">${guidance['ceiling_price']:,.0f}</p>
                    <p class="metric-subtitle">Descuento: {guidance['ceiling_discount']:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_cols[2]:
                st.markdown(f"""
                <div class="metric-card metric-card-orange">
                    <p class="metric-label">Margen Objetivo</p>
                    <p class="metric-value">{guidance['target_margin_pct']:.1f}%</p>
                    <p class="metric-subtitle">${guidance['target_margin_total']:,.0f} total</p>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_cols[3]:
                st.markdown(f"""
                <div class="metric-card metric-card-purple">
                    <p class="metric-label">Margen Mínimo</p>
                    <p class="metric-value">{guidance['margin_floor']:.1f}%</p>
                    <p class="metric-subtitle">Piso requerido</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Gráfico de elasticidad
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Área de margen esperado
            fig.add_trace(
                go.Scatter(
                    x=scenarios['discount'],
                    y=scenarios['expected_margin'],
                    fill='tozeroy',
                    fillcolor='rgba(16, 185, 129, 0.3)',
                    line=dict(color='#10b981', width=3),
                    name='Margen Esperado'
                ),
                secondary_y=False
            )
            
            # Línea de probabilidad de ganar
            fig.add_trace(
                go.Scatter(
                    x=scenarios['discount'],
                    y=scenarios['win_prob'],
                    line=dict(color='#3b82f6', width=2, dash='dash'),
                    name='Prob. de Ganar (%)'
                ),
                secondary_y=True
            )
            
            # Líneas verticales para targets
            fig.add_vline(x=guidance['target_discount'], line_dash="solid", line_color="#10b981", 
                         annotation_text="Target", annotation_position="top")
            fig.add_vline(x=guidance['ceiling_discount'], line_dash="dash", line_color="#f59e0b",
                         annotation_text="Techo", annotation_position="top")
            
            fig.update_layout(
                title=dict(
                    text='Análisis de Elasticidad: Descuento vs Margen Esperado',
                    font=dict(size=18, color='#10b981', family='Crimson Pro')
                ),
                xaxis_title='Descuento (%)',
                plot_bgcolor='rgba(30, 41, 59, 0.6)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1', family='Space Mono'),
                xaxis=dict(gridcolor='#334155'),
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='right',
                    x=1,
                    font=dict(color='#cbd5e1')
                ),
                height=350
            )
            
            fig.update_yaxes(title_text="Margen Esperado ($)", secondary_y=False, gridcolor='#334155')
            fig.update_yaxes(title_text="Prob. Ganar (%)", secondary_y=True, gridcolor='#334155')
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Evaluador de cotización
            st.markdown("""
            <div class="slide-container">
                <h3 style="color: #f59e0b; font-family: 'Crimson Pro', serif; font-size: 1.25rem;">Evaluar Cotización</h3>
            </div>
            """, unsafe_allow_html=True)
            
            eval_cols = st.columns([2, 1])
            
            with eval_cols[0]:
                quoted_price = st.slider(
                    "Precio Cotizado",
                    min_value=int(guidance['cost'] * 0.9),
                    max_value=int(guidance['list_price']),
                    value=int(guidance['target_price']),
                    step=10
                )
            
            evaluation = evaluate_quote(quoted_price, guidance)
            
            with eval_cols[1]:
                st.markdown(f"""
                <div style="background: {evaluation['color']}20; border: 2px solid {evaluation['color']}; 
                            border-radius: 0.75rem; padding: 1.5rem; text-align: center;">
                    <p style="font-size: 2rem; font-weight: bold; color: {evaluation['color']}; margin: 0;">
                        {evaluation['status']}
                    </p>
                    <p style="font-size: 0.875rem; color: #cbd5e1; margin: 0.5rem 0 0;">
                        Descuento: {evaluation['discount']:.1f}% | Margen: {evaluation['margin']:.1f}%
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="highlight-box" style="margin-top: 1rem;">
                <strong style="color: {evaluation['color']};">{evaluation['message']}</strong>
            </div>
            """, unsafe_allow_html=True)
        
        else:
            st.markdown("""
            <div class="slide-container" style="text-align: center; padding: 4rem;">
                <p style="font-size: 1.25rem; color: #94a3b8;">
                    Seleccione un cliente, producto y cantidad, luego haga clic en 
                    <strong style="color: #10b981;">"Calcular Guía de Precios"</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)


# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: #64748b; font-family: 'Space Mono', monospace; font-size: 0.75rem;">
    <p>Acero Industrial - Sistema de Optimización de Precios</p>
    <p>Desarrollado para RevSeekr Case Study</p>
</div>
""", unsafe_allow_html=True)
