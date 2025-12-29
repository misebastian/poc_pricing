"""
ACERO INDUSTRIAL - Sistema de Optimización de Precios
Aplicación Streamlit con presentación ejecutiva y herramienta de cotización
8 Slides: Intro + 4 Puntos (6 slides) + Demo
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
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 3px solid #10b981;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #f1f5f9;
    }
    
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
    
    .metric-card-red {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        box-shadow: 0 10px 30px rgba(239, 68, 68, 0.3);
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
    
    .slide-container {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid #334155;
        border-radius: 1rem;
        padding: 2rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        margin-bottom: 1.5rem;
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
    
    .highlight-box {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid #10b981;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #cbd5e1;
    }
    
    .highlight-box-warning {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid #f59e0b;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #cbd5e1;
    }
    
    .highlight-box-danger {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid #ef4444;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #cbd5e1;
    }
    
    .highlight-box-blue {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid #3b82f6;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #cbd5e1;
    }
    
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
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .content-text {
        font-family: 'Space Mono', monospace;
        color: #cbd5e1;
        line-height: 1.8;
    }
    
    .section-title {
        color: #3b82f6;
        font-family: 'Crimson Pro', serif;
        font-size: 1.3rem;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }
    
    .bullet-item {
        color: #cbd5e1;
        padding: 0.4rem 0;
        padding-left: 1.5rem;
        position: relative;
        font-family: 'Space Mono', monospace;
        font-size: 0.95rem;
    }
    
    .bullet-item::before {
        content: "→";
        position: absolute;
        left: 0;
        color: #10b981;
    }
    
</style>
""", unsafe_allow_html=True)

# =============================================================================
# DATOS Y CONFIGURACIÓN
# =============================================================================

TIER_RULES = {
    'Standard': {'target': 5.9, 'ceiling': 9.1, 'hard_max': 14.2, 'margin_floor': 14.4},
    'Bronze': {'target': 8.5, 'ceiling': 12.1, 'hard_max': 16.0, 'margin_floor': 12.8},
    'Silver': {'target': 10.9, 'ceiling': 14.4, 'hard_max': 18.2, 'margin_floor': 10.4},
    'Gold': {'target': 14.7, 'ceiling': 17.9, 'hard_max': 23.0, 'margin_floor': 6.7},
    'Platinum': {'target': 17.9, 'ceiling': 21.0, 'hard_max': 26.5, 'margin_floor': 1.4}
}

CATEGORY_ADJ = {
    'Flat': -0.1,
    'Long': 0.1,
    'Tubular': -0.15,
    'Processed': 0.0
}

SEGMENT_ADJ = {
    'Manufacturing': 0.1,
    'Construction': -0.2,
    'Other': 0.15
}

REGION_ADJ = {
    'Bogota': -0.3,
    'Antioquia': -0.3,
    'Valle': 0.1,
    'Costa': 0.8,
    'Ecuador': 0.5,
    'Panama': -0.2
}

PRODUCTS = {
    'P1000': {'name': 'Lámina HR A36', 'category': 'Flat', 'list_price': 2100, 'cost': 1700},
    'P1001': {'name': 'Lámina CR 1018', 'category': 'Flat', 'list_price': 2400, 'cost': 1950},
    'P1002': {'name': 'Varilla Corrugada', 'category': 'Long', 'list_price': 1500, 'cost': 1200},
    'P1003': {'name': 'Perfil Estructural', 'category': 'Long', 'list_price': 2800, 'cost': 2300},
    'P1004': {'name': 'Tubo Redondo', 'category': 'Tubular', 'list_price': 1800, 'cost': 1450},
    'P1005': {'name': 'Tubo Cuadrado', 'category': 'Tubular', 'list_price': 1950, 'cost': 1580},
    'P1006': {'name': 'Placa Cortada', 'category': 'Processed', 'list_price': 3200, 'cost': 2600}
}

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
    customer = CUSTOMERS[customer_id]
    product = PRODUCTS[product_id]
    tier_rule = TIER_RULES[customer['tier']]
    
    base_target = tier_rule['target']
    cat_adj = CATEGORY_ADJ.get(product['category'], 0)
    seg_adj = SEGMENT_ADJ.get(customer['segment'], 0)
    reg_adj = REGION_ADJ.get(customer['region'], 0)
    
    adjusted_target = base_target + cat_adj + seg_adj + reg_adj
    
    list_price = product['list_price']
    cost = product['cost']
    
    target_price = list_price * (1 - adjusted_target / 100)
    ceiling_price = list_price * (1 - tier_rule['ceiling'] / 100)
    floor_price = cost / (1 - tier_rule['margin_floor'] / 100)
    
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
    scenarios = []
    for discount in np.arange(0, 30, 0.5):
        price = guidance['list_price'] * (1 - discount / 100)
        margin_per_unit = price - guidance['cost']
        margin_pct = margin_per_unit / price * 100 if price > 0 else 0
        
        if discount < 5:
            win_prob = 0.80
        elif discount <= 10:
            win_prob = 0.80 - (discount - 5) * 0.01
        elif discount <= 15:
            win_prob = 0.75 - (discount - 10) * 0.04
        elif discount <= 20:
            win_prob = 0.54 - (discount - 15) * 0.04
        else:
            win_prob = max(0.35, 0.35 + (discount - 20) * 0.01)
        
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
        OPTIMIZACION DE PRECIOS
    </p>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navegación",
    ["01. Resumen Ejecutivo",
     "02. Data Readiness (Parte 1)", 
     "03. Data Readiness (Parte 2)",
     "04. Enfoque de Optimización (Parte 1)",
     "05. Enfoque de Optimización (Parte 2)",
     "06. Validation & Testing",
     "07. Riesgos y Mitigación",
     "08. Demo del Sistema"],
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
# SLIDE 1: RESUMEN EJECUTIVO
# =============================================================================

if page == "01. Resumen Ejecutivo":
    st.markdown('<p class="main-title">Acero Industrial</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Evaluacion de Preparacion de Datos para Optimizacion de Precios</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<p class="slide-number">Slide 01 / 08</p>', unsafe_allow_html=True)
        st.markdown('<h2 class="slide-title">Resumen Ejecutivo</h2>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<p class="section-title">Contexto del Proyecto</p>', unsafe_allow_html=True)
            st.markdown("""
            <p class="bullet-item">Distribuidor de acero colombiano con <strong style="color: #10b981;">$185M</strong> en ingresos</p>
            <p class="bullet-item">Margen actual: <strong style="color: #f59e0b;">18.2%</strong> vs objetivo: <strong style="color: #10b981;">20%</strong></p>
            <p class="bullet-item">823 clientes, 4,847 SKUs, 42 representantes de ventas</p>
            <p class="bullet-item">Sistema PriceFx implementado pero sin optimización efectiva</p>
            """, unsafe_allow_html=True)
            
            st.markdown('<p class="section-title">Hallazgo Principal</p>', unsafe_allow_html=True)
            st.markdown("""
            <div class="highlight-box">
                <strong style="color: #10b981;">Los datos reflejan comportamiento PRE-OPTIMIZACION.</strong><br><br>
                Entrenar un modelo ML replicaria las ineficiencias actuales, no las corregiria.
                Un enfoque de guardrails + reglas es mas efectivo para este contexto.
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<p class="section-title">Resultado del Sistema Propuesto</p>', unsafe_allow_html=True)
            st.markdown("""
            <p class="bullet-item">GM Invoice: <strong style="color: #10b981;">~22%</strong> (vs target 20%)</p>
            <p class="bullet-item">Aprobaciones humanas: solo <strong style="color: #3b82f6;">5%</strong> de deals</p>
            <p class="bullet-item">Reduccion de erosion: <strong style="color: #f59e0b;">~70%</strong></p>
            <p class="bullet-item">22% de deals sin descuento (antes: descuento "por defecto")</p>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card metric-card-green">
            <p class="metric-label">GM Invoice Final</p>
            <p class="metric-value">22.17%</p>
            <p class="metric-subtitle">Target: 20%</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card metric-card-blue">
            <p class="metric-label">Aprobaciones Humanas</p>
            <p class="metric-value">5%</p>
            <p class="metric-subtitle">Solo deals de alto riesgo</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card metric-card-orange">
            <p class="metric-label">Reduccion de Drift</p>
            <p class="metric-value">-70%</p>
            <p class="metric-subtitle">De -3.8% a -1.1%</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card metric-card-purple">
            <p class="metric-label">Deals Sin Descuento</p>
            <p class="metric-value">22.5%</p>
            <p class="metric-subtitle">1 de cada 4 deals</p>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# SLIDE 2: DATA READINESS (PARTE 1)
# =============================================================================

elif page == "02. Data Readiness (Parte 1)":
    st.markdown('<p class="slide-number">Slide 02 / 08</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="slide-title">1. Data Readiness Assessment (Parte 1)</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle" style="font-size: 1rem;">Que datos son usables y que falta</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="slide-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #10b981; font-family: Crimson Pro, serif;">Datos Usables (Para Empezar Ya)</h3>', unsafe_allow_html=True)
        
        st.markdown('<p class="section-title">A. Integridad y Consistencia Aritmetica</p>', unsafe_allow_html=True)
        st.markdown("""
        <p class="bullet-item">0 nulos en columnas clave (customer/product/price/cost/outcome)</p>
        <p class="bullet-item">Identidades contables consistentes</p>
        <p class="bullet-item"><code style="color: #10b981;">extended_amount = quantity x unit_price</code></p>
        <p class="bullet-item"><code style="color: #10b981;">margin_dollars = extended_amount - total_cost</code></p>
        """, unsafe_allow_html=True)
        
        st.markdown('<p class="section-title">B. Senal Suficiente para Segmentacion</p>', unsafe_allow_html=True)
        st.markdown("""
        <p class="bullet-item">200 clientes, 24 productos en el extracto</p>
        <p class="bullet-item">Segmentos y tiers bien poblados</p>
        <p class="bullet-item">Permite arrancar con pricing por segmentos</p>
        """, unsafe_allow_html=True)
        
        st.markdown('<p class="section-title">C. Variacion Real en Descuentos</p>', unsafe_allow_html=True)
        st.markdown("""
        <p class="bullet-item">Rango de descuento: <strong style="color: #10b981;">0% a 29.2%</strong></p>
        <p class="bullet-item">12 deals con descuento 0% - confirma que NO siempre debe haber descuento</p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="slide-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #f59e0b; font-family: Crimson Pro, serif;">Que Falta o Preocupa</h3>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="highlight-box-warning">
            <h4 style="color: #f59e0b; margin-top: 0;">A. Endogeneidad (Core)</h4>
            <p>Los datos reflejan comportamiento <strong>pre-optimizacion</strong>. 
            Un ML naive imitara patrones, no los corregira.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="highlight-box-danger">
            <h4 style="color: #ef4444; margin-top: 0;">B. Outcome Ruidoso</h4>
            <p class="bullet-item">Win/Loss inconsistente entre sistemas</p>
            <p class="bullet-item">~40% de expirados terminan ganados bajo otro quote_id</p>
            <p class="bullet-item">Re-quoted = 15.84% de outcomes</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="highlight-box-warning">
            <h4 style="color: #f59e0b; margin-top: 0;">C. Quote-to-Invoice Drift</h4>
            <p class="bullet-item">Drift promedio: <strong>-3.87%</strong></p>
            <p class="bullet-item">87.78% de deals con |drift| mayor a 1%</p>
            <p class="bullet-item">El precio facturado siempre menor que quoted</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Gráfico de inconsistencia
    st.markdown('<div class="slide-container">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #3b82f6; font-family: Crimson Pro, serif;">Evidencia de Variabilidad Injustificada</h3>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col3, col4 = st.columns([1, 1])
    
    with col3:
        inconsistency_data = pd.DataFrame({
            'Métrica': ['Rango Precio > 5%', 'Std Descuento > 2pp', 'Margen Negativo', 'Descuento > 25%'],
            'Porcentaje': [71.74, 76.81, 0.48, 0.44]
        })
        
        fig = go.Figure(go.Bar(
            x=inconsistency_data['Porcentaje'],
            y=inconsistency_data['Métrica'],
            orientation='h',
            marker_color=['#ef4444', '#ef4444', '#f59e0b', '#f59e0b'],
            text=[f"{p:.1f}%" for p in inconsistency_data['Porcentaje']],
            textposition='inside',
            textfont=dict(size=14, color='white')
        ))
        
        fig.update_layout(
            title=dict(
                text='Inconsistencia en Pares Cliente-Producto',
                font=dict(size=16, color='#10b981', family='Crimson Pro')
            ),
            xaxis_title='% de Pares',
            plot_bgcolor='rgba(30, 41, 59, 0.6)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1', family='Space Mono'),
            xaxis=dict(range=[0, 100], gridcolor='#334155'),
            yaxis=dict(gridcolor='#334155'),
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col4:
        st.markdown("""
        <div class="highlight-box">
            <h4 style="color: #10b981; margin-top: 0;">Implicacion Practica</h4>
            <p>La alta variabilidad confirma "ruido humano" fuerte en los precios.</p>
            <p><strong>Para optimizacion, primero hay que:</strong></p>
            <p class="bullet-item">Reducir variabilidad injustificada</p>
            <p class="bullet-item">Implementar guardrails + guidance</p>
            <p class="bullet-item">No modelos sofisticados hasta tener datos limpios</p>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# SLIDE 3: DATA READINESS (PARTE 2)
# =============================================================================

elif page == "03. Data Readiness (Parte 2)":
    st.markdown('<p class="slide-number">Slide 03 / 08</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="slide-title">1. Data Readiness Assessment (Parte 2)</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle" style="font-size: 1rem;">Que segmentos tienen data suficiente y donde enfocar</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="slide-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #10b981; font-family: Crimson Pro, serif;">Data Suficiente por Segmento</h3>', unsafe_allow_html=True)
        
        st.markdown('<p class="section-title">Productos (Suficiente)</p>', unsafe_allow_html=True)
        st.markdown('<p style="color: #cbd5e1;">Cada producto tiene ~188-249 transacciones - suficiente para analisis.</p>', unsafe_allow_html=True)
        
        st.markdown('<p class="section-title">Producto x Segmento</p>', unsafe_allow_html=True)
        st.markdown("""
        <p class="bullet-item">30+ transacciones: <strong style="color: #10b981;">100%</strong> cumplen</p>
        <p class="bullet-item">50+ transacciones: <strong style="color: #f59e0b;">~68%</strong> cumplen</p>
        <p class="bullet-item">Zonas "thin" concentradas en segmento <strong>"Other"</strong></p>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="highlight-box">
            <strong style="color: #10b981;">Implicacion:</strong><br>
            <p class="bullet-item">Manufacturing y Construction: modelar por segmento con estabilidad</p>
            <p class="bullet-item">Other: usar pooling/hierarchical, reglas mas agregadas</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="slide-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #ef4444; font-family: Crimson Pro, serif;">Segmentos que Mas Erosionan Margen</h3>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        critical_segments = pd.DataFrame({
            'Segmento + Tier': ['Manufacturing + Platinum', 'Construction + Gold', 'Manufacturing + Gold'],
            'GM%': ['7.69%', '~11%', '~12%'],
            'Descuento Medio': ['18.74%', '~15%', '~15%'],
            'Win Rate': ['48.9%', '~52%', '~55%']
        })
        
        st.dataframe(critical_segments, use_container_width=True, hide_index=True)
        
        st.markdown("""
        <div class="highlight-box-warning" style="margin-top: 1rem;">
            <strong style="color: #f59e0b;">Foco de Optimizacion:</strong><br>
            Estos segmentos tienen descuento "habitual" pero win-rate que no lo justifica.
            Es donde puedes subir margen hacia 20% sin matar volumen.
        </div>
        """, unsafe_allow_html=True)
    
    # Conclusión
    st.markdown("""
    <div class="slide-container">
        <h3 style="color: #3b82f6; font-family: Crimson Pro, serif;">Conclusion de Data Readiness</h3>
        <div class="highlight-box" style="border-width: 2px;">
            <p style="font-size: 1.1rem; margin: 0; color: #cbd5e1;">
                <strong style="color: #10b981;">SI hay data usable</strong> para empezar con reglas + guidance + modelos simples y explicables.
            </p>
            <p style="font-size: 1.1rem; margin: 1rem 0 0; color: #cbd5e1;">
                <strong style="color: #ef4444;">NO hay condiciones</strong> para "full ML optimization" sin antes resolver:
            </p>
            <p class="bullet-item">Outcome noise (Re-quoted, inconsistencia Win/Loss)</p>
            <p class="bullet-item">Linking de oportunidades (quote_id != opportunity_id)</p>
            <p class="bullet-item">Control de quote a invoice erosion</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# SLIDE 4: ENFOQUE DE OPTIMIZACIÓN (PARTE 1)
# =============================================================================

elif page == "04. Enfoque de Optimización (Parte 1)":
    st.markdown('<p class="slide-number">Slide 04 / 08</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="slide-title">2. Recommended Optimization Approach (Parte 1)</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle" style="font-size: 1rem;">Lo que SI recomendamos implementar</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="slide-container">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #10b981; margin-bottom: 1rem;">1. Segmented Pricing + Guardrails</h4>', unsafe_allow_html=True)
        st.markdown('<p style="color: #94a3b8; font-size: 0.9rem;"><strong>Fase 0-1 (Quick Win)</strong></p>', unsafe_allow_html=True)
        st.markdown("""
        <p class="bullet-item">Bandas de precio/descuento por segmento + tier + categoria</p>
        <p class="bullet-item">Piso de margen por categoria</p>
        <p class="bullet-item">Cap de descuento por tier</p>
        <p class="bullet-item">Thin data - reglas agregadas (pooling)</p>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="highlight-box" style="padding: 1rem;">
            <strong>Justificacion:</strong> 71.74% de pares tienen rango mayor a 5%<br>
            Primero estandarizar, luego optimizar
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="slide-container">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #f59e0b; margin-bottom: 1rem;">3. Margin-Constrained Price Recommendation</h4>', unsafe_allow_html=True)
        st.markdown('<p style="color: #94a3b8; font-size: 0.9rem;"><strong>Optimizacion "safe" con restricciones</strong></p>', unsafe_allow_html=True)
        st.markdown("""
        <p class="bullet-item">Funcion objetivo: Expected Profit = (p - c) x q x P(win | p)</p>
        <p class="bullet-item">Grid search sobre descuentos candidatos</p>
        <p class="bullet-item">Restriccion: margen minimo por categoria/tier</p>
        <p class="bullet-item">No recomendar descuento si win-prob no mejora</p>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="highlight-box-warning" style="padding: 1rem;">
            <strong>Resultado:</strong> Si a 0-5% ya ganas ~80%,<br>
            la recomendacion puede ser 0% descuento
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="slide-container">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #3b82f6; margin-bottom: 1rem;">2. Deal Scoring (Win Probability)</h4>', unsafe_allow_html=True)
        st.markdown('<p style="color: #94a3b8; font-size: 0.9rem;"><strong>Modelo explicable con Won/Lost</strong></p>', unsafe_allow_html=True)
        st.markdown("""
        <p class="bullet-item">Features: discount_pct, days_to_close, segment, tier, category, region</p>
        <p class="bullet-item">Entrenar SOLO con Won/Lost</p>
        <p class="bullet-item">Excluir Re-quoted (tratarlo como workflow)</p>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="highlight-box-blue" style="padding: 1rem;">
            <strong>Insight clave:</strong><br>
            0-10% descuento: ~80% win-rate<br>
            15-20% descuento: 54% win-rate<br>
            <strong style="color: #ef4444;">Mas descuento NO compra win-rate</strong>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="slide-container">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #8b5cf6; margin-bottom: 1rem;">4. Erosion Control (Quote a Invoice)</h4>', unsafe_allow_html=True)
        st.markdown('<p style="color: #94a3b8; font-size: 0.9rem;"><strong>Guardrail critico para proteger margen</strong></p>', unsafe_allow_html=True)
        st.markdown("""
        <p class="bullet-item">Monitorear diferencia quoted_price a unit_price</p>
        <p class="bullet-item">Alertas si drift excede umbral</p>
        <p class="bullet-item">Reason codes para ajustes</p>
        <p class="bullet-item">Aprobacion si ajuste rompe guardrail</p>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="highlight-box-danger" style="padding: 1rem;">
            <strong>Problema actual:</strong> Drift -3.87%, 100% termina<br>
            por debajo del quote. Sin control no llegas a 20% GM
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================
# SLIDE 5: ENFOQUE DE OPTIMIZACIÓN (PARTE 2) - RESULTADOS
# =============================================================================

elif page == "05. Enfoque de Optimización (Parte 2)":
    st.markdown('<p class="slide-number">Slide 05 / 08</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="slide-title">2. Recommended Optimization Approach (Parte 2)</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle" style="font-size: 1rem;">Resultados del Sistema y Lo que NO Recomendamos</p>', unsafe_allow_html=True)
    
    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card metric-card-green">
            <p class="metric-label">Approval Rate</p>
            <p class="metric-value">5.0%</p>
            <p class="metric-subtitle">Solo el 5% mas riesgoso</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card metric-card-blue">
            <p class="metric-label">GM Quote</p>
            <p class="metric-value">23.24%</p>
            <p class="metric-subtitle">Lo que controla pricing</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card metric-card-orange">
            <p class="metric-label">GM Invoice</p>
            <p class="metric-value">22.17%</p>
            <p class="metric-subtitle">+2.2pp sobre target 20%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card metric-card-purple">
            <p class="metric-label">Drift After</p>
            <p class="metric-value">-1.08%</p>
            <p class="metric-subtitle">Antes: -3.83%</p>
        </div>
        """, unsafe_allow_html=True)
    
    col5, col6 = st.columns([1, 1])
    
    with col5:
        st.markdown('<div class="slide-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #10b981; font-family: Crimson Pro, serif;">Monte Carlo: Estabilidad Confirmada</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #cbd5e1;"><strong>20 runs x 2000 deals cada uno:</strong></p>', unsafe_allow_html=True)
        
        monte_carlo_df = pd.DataFrame({
            'Metrica': ['Approval Rate', 'GM Invoice', 'Drift After'],
            'Mean': ['4.80%', '22.20%', '-1.07%'],
            'Std': ['0.51%', '0.08%', '0.02%']
        })
        st.dataframe(monte_carlo_df, use_container_width=True, hide_index=True)
        
        st.markdown("""
        <div class="highlight-box" style="margin-top: 1rem;">
            <strong style="color: #10b981;">Sistema production-ready:</strong><br>
            No depende del mix, no es fragil, escala.
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col6:
        st.markdown('<div class="slide-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #ef4444; font-family: Crimson Pro, serif;">Lo que NO Recomendamos (Aun)</h3>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="highlight-box-danger">
            <h4 style="color: #ef4444; margin-top: 0;">1. Elasticity Modeling "Puro" por SKU</h4>
            <p style="margin-bottom: 0; color: #cbd5e1;">Precios contaminados por decisiones humanas, outcomes con Re-quoted, post-quote erosion.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="highlight-box-danger">
            <h4 style="color: #ef4444; margin-top: 0;">2. Tratar Re-quoted como Lost</h4>
            <p style="margin-bottom: 0; color: #cbd5e1;">Es una clase propia (15.84%). Distorsiona la relacion descuento a win.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="highlight-box-danger">
            <h4 style="color: #ef4444; margin-top: 0;">3. "Siempre Dar Descuento"</h4>
            <p style="margin-bottom: 0; color: #cbd5e1;">0-10% ya tiene ~80% win-rate. Dar mas descuento ahi es quemar margen.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Quote final
    st.markdown("""
    <div class="slide-container" style="text-align: center; border: 2px solid #10b981;">
        <p style="font-size: 1.1rem; font-style: italic; color: #cbd5e1; margin: 0;">
            "We replaced heuristic discounting with a risk-ranked pricing policy. Instead of approving 
            everything above a threshold, we approve only the riskiest 5% of deals. This increased 
            invoice GM from ~18.5% to ~22%, while reducing price erosion by ~70%."
        </p>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# SLIDE 6: VALIDATION & TESTING
# =============================================================================

elif page == "06. Validation & Testing":
    st.markdown('<p class="slide-number">Slide 06 / 08</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="slide-title">3. Validation & Testing Framework</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle" style="font-size: 1rem;">Como validamos antes de desplegar en toda la empresa</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="slide-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #3b82f6; font-family: Crimson Pro, serif;">Fase 1: Validacion Offline</h3>', unsafe_allow_html=True)
        
        st.markdown('<p class="section-title">Backtesting: "Que habria pasado si...?"</p>', unsafe_allow_html=True)
        st.markdown('<p style="color: #cbd5e1;">Simular el nuevo sistema usando datos historicos, sin afectar operaciones.</p>', unsafe_allow_html=True)
        st.markdown("""
        <p class="bullet-item">Tomar deals historicos</p>
        <p class="bullet-item">Aplicar precio recomendado por el sistema</p>
        <p class="bullet-item">Simular erosion real</p>
        <p class="bullet-item">Medir margen resultante</p>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="highlight-box" style="margin-top: 1rem;">
            <strong>Resultados del Backtest:</strong><br>
            Margen sube de ~18.5% a ~22%<br>
            Solo 5/100 deals requieren aprobacion
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<p class="section-title">Monte Carlo: "Es suerte o es estable?"</p>', unsafe_allow_html=True)
        st.markdown('<p style="color: #cbd5e1;">Miles de combinaciones aleatorias para validar que no depende del mix especifico.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="slide-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #f59e0b; font-family: Crimson Pro, serif;">Fase 2: Champion / Challenger</h3>', unsafe_allow_html=True)
        
        st.markdown('<p class="section-title">Que es?</p>', unsafe_allow_html=True)
        st.markdown("""
        <p style="color: #cbd5e1;"><strong style="color: #10b981;">Champion</strong> = proceso actual de precios<br>
        <strong style="color: #3b82f6;">Challenger</strong> = nuevo sistema</p>
        <p style="color: #cbd5e1;">Ambos conviven al mismo tiempo, en una parte del negocio, durante tiempo limitado.</p>
        """, unsafe_allow_html=True)
        
        st.markdown('<p class="section-title">Implementacion Practica</p>', unsafe_allow_html=True)
        st.markdown("""
        <p class="bullet-item">De cada 10 cotizaciones: 8 Champion, 2 Challenger</p>
        <p class="bullet-item">Asignacion aleatoria, balanceando segmentos</p>
        <p class="bullet-item">Comparacion manzanas con manzanas</p>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="highlight-box-warning" style="margin-top: 1rem;">
            <strong>NO es un "big bang".</strong><br>
            Probamos en pequeno, medimos con dinero real.
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Métricas a medir
    st.markdown('<h3 style="color: #10b981; font-family: Crimson Pro, serif; margin-top: 1rem;">Metricas Durante el Test</h3>', unsafe_allow_html=True)
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.markdown("""
        <div class="highlight-box-blue" style="height: 180px;">
            <h4 style="color: #3b82f6; margin-bottom: 1rem;">Metricas de Dinero</h4>
            <p class="bullet-item">Margen real facturado (invoice GM)</p>
            <p class="bullet-item">Erosion quote a invoice</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="highlight-box" style="height: 180px;">
            <h4 style="color: #10b981; margin-bottom: 1rem;">Metricas Comerciales</h4>
            <p class="bullet-item">Win rate</p>
            <p class="bullet-item">Tiempo de cierre</p>
            <p class="bullet-item">% deals sin descuento</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class="highlight-box-warning" style="height: 180px;">
            <h4 style="color: #f59e0b; margin-bottom: 1rem;">Metricas Operativas</h4>
            <p class="bullet-item">% deals que requieren aprobacion</p>
            <p class="bullet-item">Tiempo de aprobacion</p>
            <p class="bullet-item">Excepciones solicitadas</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Criterios
    col6, col7 = st.columns([1, 1])
    
    with col6:
        st.markdown('<div class="slide-container">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #10b981;">Criterios de Exito (Pre-definidos)</h4>', unsafe_allow_html=True)
        st.markdown("""
        <p class="bullet-item">Margen sube al menos <strong style="color: #10b981;">1 punto porcentual</strong></p>
        <p class="bullet-item">Erosion baja al menos <strong style="color: #10b981;">50%</strong></p>
        <p class="bullet-item">Win rate no cae mas de <strong style="color: #f59e0b;">1-2 puntos</strong></p>
        <p class="bullet-item">Aprobaciones cerca del <strong style="color: #3b82f6;">5%</strong></p>
        """, unsafe_allow_html=True)
        st.markdown('<p style="margin-top: 1rem; color: #10b981;"><strong>Si se cumple: nuevo sistema reemplaza al actual. Sin discusion subjetiva.</strong></p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col7:
        st.markdown('<div class="slide-container">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #ef4444;">Guardrails Activos</h4>', unsafe_allow_html=True)
        st.markdown("""
        <p class="bullet-item">Sistema no puede recomendar margen negativo</p>
        <p class="bullet-item">Descuentos extremos bloqueados</p>
        <p class="bullet-item">5% mas riesgoso pasa por aprobacion humana</p>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="highlight-box-danger" style="margin-top: 1rem;">
            <strong>Kill Switch:</strong> Si metrica clave sale de rango, 
            se apaga challenger inmediatamente.
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================
# SLIDE 7: RIESGOS Y MITIGACIÓN
# =============================================================================

elif page == "07. Riesgos y Mitigación":
    st.markdown('<p class="slide-number">Slide 07 / 08</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="slide-title">4. Key Risks & Mitigation</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle" style="font-size: 1rem;">Cuales son los riesgos principales? Como abordamos la resistencia de ventas?</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="slide-container">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #ef4444; margin-bottom: 1rem;">Riesgo #1: "El sistema no entiende el contexto humano"</h4>', unsafe_allow_html=True)
        st.markdown('<p style="color: #94a3b8; font-size: 0.9rem;"><strong>Lo que Carlos (VP Sales) teme:</strong> Que el algoritmo reemplace su criterio.</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="highlight-box" style="padding: 1rem;">
            <strong style="color: #10b981;">Mitigacion:</strong><br>
            <p class="bullet-item">El sistema NO bloquea decisiones humanas</p>
            <p class="bullet-item">Solo envia a aprobacion el 5% mas riesgoso</p>
            <p class="bullet-item">95% de deals: vendedor cotiza rapido</p>
            <p class="bullet-item">"Es un copiloto, no piloto automatico"</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="slide-container">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #ef4444; margin-bottom: 1rem;">Riesgo #3: "Protege margen en deals que ya ibamos a perder"</h4>', unsafe_allow_html=True)
        st.markdown('<p style="color: #94a3b8; font-size: 0.9rem;"><strong>Objecion clasica de ventas.</strong></p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="highlight-box" style="padding: 1rem;">
            <strong style="color: #10b981;">Mitigacion (con datos):</strong><br>
            <p style="color: #cbd5e1; margin: 0.5rem 0;">0-10% descuento: <strong>~80% win-rate</strong></p>
            <p style="color: #cbd5e1; margin: 0.5rem 0;">15-20% descuento: 54% win-rate</p>
            <p style="color: #cbd5e1; margin: 0.5rem 0;">20-25% descuento: 35% win-rate</p>
            <p style="margin-top: 0.5rem; color: #f59e0b;">"No te quito armas. Te quito balas desperdiciadas."</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="slide-container">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #ef4444; margin-bottom: 1rem;">Riesgo #2: "Esto nos va a volver mas lentos"</h4>', unsafe_allow_html=True)
        st.markdown('<p style="color: #94a3b8; font-size: 0.9rem;"><strong>Trauma previo:</strong> PriceFx aumento tiempo de cotizacion.</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="highlight-box" style="padding: 1rem;">
            <strong style="color: #10b981;">Mitigacion:</strong><br>
            <p class="bullet-item">Aprobaciones historicas: difusas, frecuentes</p>
            <p class="bullet-item">Nuevo sistema: <strong>5% fijo</strong>, predecible</p>
            <p class="bullet-item">"Hoy no sabes cuantos van a aprobacion. Con esto lo sabes: 5 de cada 100."</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="slide-container">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #ef4444; margin-bottom: 1rem;">Riesgo #4: "La data esta sucia"</h4>', unsafe_allow_html=True)
        st.markdown('<p style="color: #94a3b8; font-size: 0.9rem;"><strong>Preocupacion legitima de Maria (Pricing Manager).</strong></p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="highlight-box" style="padding: 1rem;">
            <strong style="color: #10b981;">Mitigacion por diseno:</strong><br>
            <p class="bullet-item">NO elasticidad por SKU (requiere data limpia)</p>
            <p class="bullet-item">Pooling por segmento/tier/categoria</p>
            <p class="bullet-item">Re-quotes excluidos del win-model</p>
            <p class="bullet-item">Thin data: reglas agregadas</p>
            <p style="margin-top: 0.5rem; color: #10b981;">"Este sistema asume data real, no perfecta"</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Incentivo y conclusión
    col3, col4 = st.columns([1, 1])
    
    with col3:
        st.markdown("""
        <div class="slide-container" style="border: 2px solid #10b981;">
            <h4 style="color: #10b981;">Convertir Resistencia en Alianza</h4>
            <p style="color: #cbd5e1;"><strong>Palanca final: Comisiones</strong></p>
            <p class="bullet-item">Menos descuentos innecesarios</p>
            <p class="bullet-item">Mas margen por deal</p>
            <p class="bullet-item">Mejores comisiones para el equipo</p>
            <div class="highlight-box" style="margin-top: 1rem;">
                <strong>"Si el equipo gana el mismo numero de deals con menos descuento, todos ganan mas."</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="slide-container" style="border: 2px solid #3b82f6;">
            <h4 style="color: #3b82f6;">Mensaje para Stakeholders</h4>
            <p style="font-style: italic; font-size: 0.9rem; color: #cbd5e1;">
                "The main risks are sales resistance, data quality concerns, and operational friction. 
                We mitigate these by design: the system does not replace sales judgment, limits approvals 
                to the riskiest 5% of deals, and is robust to imperfect data."
            </p>
            <p style="font-style: italic; font-size: 0.9rem; margin-top: 1rem; color: #cbd5e1;">
                "It reduces price erosion, protects margin, and preserves sales velocity."
            </p>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# SLIDE 8: DEMO DEL SISTEMA
# =============================================================================

elif page == "08. Demo del Sistema":
    st.markdown('<p class="slide-number">Slide 08 / 08</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="slide-title">Demo: Sistema de Cotizacion Inteligente</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="slide-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #10b981; font-family: Crimson Pro, serif; font-size: 1.25rem;">Datos de la Cotizacion</h3>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        customer_id = st.selectbox(
            "Cliente",
            options=list(CUSTOMERS.keys()),
            format_func=lambda x: f"{x} - {CUSTOMERS[x]['name']}"
        )
        
        customer = CUSTOMERS[customer_id]
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.6); padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
            <p style="margin: 0; font-size: 0.875rem; color: #94a3b8;">
                <strong>Segmento:</strong> {customer['segment']}<br>
                <strong>Tier:</strong> {customer['tier']}<br>
                <strong>Region:</strong> {customer['region']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        product_id = st.selectbox(
            "Producto",
            options=list(PRODUCTS.keys()),
            format_func=lambda x: f"{x} - {PRODUCTS[x]['name']}"
        )
        
        product = PRODUCTS[product_id]
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.6); padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
            <p style="margin: 0; font-size: 0.875rem; color: #94a3b8;">
                <strong>Categoria:</strong> {product['category']}<br>
                <strong>Precio Lista:</strong> ${product['list_price']:,.2f}<br>
                <strong>Costo:</strong> ${product['cost']:,.2f}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        quantity = st.number_input("Cantidad", min_value=1, value=100, step=10)
        
        if st.button("Calcular Guia de Precios", type="primary", use_container_width=True):
            st.session_state.guidance = calculate_price_guidance(customer_id, product_id, quantity)
            st.session_state.scenarios = simulate_scenarios(st.session_state.guidance, quantity)
    
    with col2:
        if 'guidance' in st.session_state:
            guidance = st.session_state.guidance
            scenarios = st.session_state.scenarios
            
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
                    <p class="metric-label">Margen Minimo</p>
                    <p class="metric-value">{guidance['margin_floor']:.1f}%</p>
                    <p class="metric-subtitle">Piso requerido</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Gráfico
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
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
            
            fig.add_trace(
                go.Scatter(
                    x=scenarios['discount'],
                    y=scenarios['win_prob'],
                    line=dict(color='#3b82f6', width=2, dash='dash'),
                    name='Prob. de Ganar (%)'
                ),
                secondary_y=True
            )
            
            fig.add_vline(x=guidance['target_discount'], line_dash="solid", line_color="#10b981", 
                         annotation_text="Target", annotation_position="top")
            fig.add_vline(x=guidance['ceiling_discount'], line_dash="dash", line_color="#f59e0b",
                         annotation_text="Techo", annotation_position="top")
            
            fig.update_layout(
                title=dict(
                    text='Analisis de Elasticidad: Descuento vs Margen Esperado',
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
            
            # Evaluador
            st.markdown('<div class="slide-container">', unsafe_allow_html=True)
            st.markdown('<h3 style="color: #f59e0b; font-family: Crimson Pro, serif; font-size: 1.25rem;">Evaluar Cotizacion</h3>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
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
            
            # Explicación
            st.markdown("""
            <div class="slide-container" style="margin-top: 1rem;">
                <h4 style="color: #3b82f6;">Como funciona este sistema?</h4>
                <p class="bullet-item"><strong>Precio Objetivo:</strong> Descuento base por tier + ajustes por categoria, segmento y region</p>
                <p class="bullet-item"><strong>Precio Techo:</strong> Maximo antes de requerir aprobacion de gerente</p>
                <p class="bullet-item"><strong>Margen Minimo:</strong> Piso absoluto que protege rentabilidad</p>
                <p class="bullet-item"><strong>Curva Win-Prob:</strong> Basada en datos historicos, muestra que mas descuento NO siempre mejora win-rate</p>
            </div>
            """, unsafe_allow_html=True)
        
        else:
            st.markdown("""
            <div class="slide-container" style="text-align: center; padding: 4rem;">
                <p style="font-size: 1.25rem; color: #94a3b8;">
                    Seleccione un cliente, producto y cantidad, luego haga clic en 
                    <strong style="color: #10b981;">"Calcular Guia de Precios"</strong>
                </p>
                <p style="font-size: 1rem; color: #64748b; margin-top: 1rem;">
                    Este demo muestra como el sistema de guardrails recomienda precios y evalua cotizaciones en tiempo real.
                </p>
            </div>
            """, unsafe_allow_html=True)


# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: #64748b; font-family: 'Space Mono', monospace; font-size: 0.75rem;">
    <p>Acero Industrial - Sistema de Optimizacion de Precios</p>
    <p>Desarrollado para RevSeekr Case Study</p>
</div>
""", unsafe_allow_html=True)
