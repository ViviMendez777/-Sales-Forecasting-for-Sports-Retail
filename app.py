import streamlit as st
import pandas as pd
import numpy as np
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
import os
warnings.filterwarnings('ignore')

# ============================================================================
# GET CORRECT PATHS
# ============================================================================
# Get the directory where this script is located
APP_DIR = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (project root)
PROJECT_ROOT = os.path.dirname(APP_DIR)
# Define paths relative to project root
MODEL_PATH = os.path.join(PROJECT_ROOT, 'models', 'modelo_final.joblib')
DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'processed', 'inferencia_df_transformado.csv')

# ============================================================================
# CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Sales Forecast Simulator - November 2025",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 14px;
        opacity: 0.9;
    }
    .black-friday {
        background-color: #ffcccc !important;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD MODEL AND DATA
# ============================================================================
@st.cache_resource
def load_model():
    try:
        model = joblib.load(MODEL_PATH)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.error(f"Looking for model at: {MODEL_PATH}")
        return None

@st.cache_data
def load_inference_data():
    try:
        df = pd.read_csv(DATA_PATH)
        df['fecha'] = pd.to_datetime(df['fecha'])
        return df
    except Exception as e:
        st.error(f"Error loading inference data: {e}")
        st.error(f"Looking for data at: {DATA_PATH}")
        return None

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def get_feature_columns(model):
    """Extract feature names from trained model"""
    try:
        return list(model.feature_names_in_)
    except:
        return None

def prepare_prediction_data(df, feature_cols):
    """Prepare data for prediction with all required features"""
    # Create a copy with all required features
    df_pred = df.copy()
    
    # Add missing columns with default values
    for col in feature_cols:
        if col not in df_pred.columns:
            # For one-hot encoded categorical features, use 0 (False)
            if col.startswith(('nombre_h_', 'categoria_h_', 'subcategoria_h_')):
                df_pred[col] = 0
            # For numerical features, use 0
            else:
                df_pred[col] = 0
    
    # Select only the required features in the correct order
    return df_pred[feature_cols].copy()

def update_lags(row, previous_pred, lag_history):
    """Update lag variables for recursive prediction"""
    # Shift lags: lag_n becomes lag_n+1
    for lag in range(7, 1, -1):
        col = f'unidades_vendidas_lag{lag}'
        if f'unidades_vendidas_lag{lag-1}' in row.index:
            row[col] = row[f'unidades_vendidas_lag{lag-1}']
    
    # Set lag_1 to previous prediction
    row['unidades_vendidas_lag1'] = previous_pred
    
    # Update lag_history for MA7
    lag_history.append(previous_pred)
    if len(lag_history) > 7:
        lag_history.pop(0)
    
    # Update MA7
    row['unidades_vendidas_ma7'] = np.mean(lag_history)
    
    return row, lag_history

def simulate_recursive_predictions(df_product, model, feature_cols, 
                                   discount_pct, scenario_adjustment):
    """Generate recursive day-by-day predictions"""
    
    df_sim = df_product.copy().sort_values('fecha').reset_index(drop=True)
    predictions = []
    lag_history = []
    
    with st.spinner("🔄 Generating recursive predictions..."):
        for idx in range(len(df_sim)):
            # Prepare features with all required columns
            df_row = df_sim.iloc[[idx]].copy()
            X = prepare_prediction_data(df_row, feature_cols)
            
            # Apply discount to precio_venta if it exists
            if 'precio_venta' in X.columns and idx == 0:
                # Only apply discount once at the beginning
                pass
            
            # Make prediction
            try:
                pred = model.predict(X)[0]
                pred = max(0, pred)  # Ensure non-negative
            except Exception as e:
                st.warning(f"Prediction error at day {idx+1}: {e}")
                # Use mean of historical values if available
                if 'unidades_vendidas' in df_sim.columns and df_sim['unidades_vendidas'].notna().any():
                    pred = df_sim.loc[idx, 'unidades_vendidas'] if pd.notna(df_sim.loc[idx, 'unidades_vendidas']) else df_sim['unidades_vendidas'].mean()
                else:
                    pred = 0
            
            predictions.append(pred)
            
            # Update lags for next iteration
            if idx < len(df_sim) - 1:
                df_sim.loc[idx + 1], lag_history = update_lags(
                    df_sim.loc[idx + 1].copy(),
                    pred,
                    lag_history.copy()
                )
    
    df_sim['predicciones'] = predictions
    return df_sim

def apply_discount_to_dataframe(df, discount_pct):
    """Apply discount percentage to precio_venta"""
    df = df.copy()
    if 'precio_base' in df.columns:
        df['precio_venta'] = df['precio_base'] * (1 - discount_pct / 100)
        if 'descuento_porcentaje' in df.columns:
            df['descuento_porcentaje'] = discount_pct
        # Recalculate ratio_precio if precio_competencia exists
        if 'precio_competencia' in df.columns:
            df['ratio_precio'] = df['precio_venta'] / df['precio_competencia']
    return df

def apply_competition_scenario(df, scenario_adjustment):
    """Adjust competitor prices based on scenario"""
    df = df.copy()
    if scenario_adjustment == 0:
        return df
    
    adjustment_factor = 1 + (scenario_adjustment / 100)
    
    # If precio_competencia exists, adjust it directly
    if 'precio_competencia' in df.columns:
        df['precio_competencia'] = df['precio_competencia'] * adjustment_factor
        if 'precio_venta' in df.columns:
            df['ratio_precio'] = df['precio_venta'] / df['precio_competencia']
    
    # Otherwise try to adjust individual competitor columns if they exist
    comp_cols = ['Amazon', 'Decathlon', 'Deporvillage']
    for col in comp_cols:
        if col in df.columns:
            df[col] = df[col] * adjustment_factor
    
    return df

def calculate_metrics(df_sim):
    """Calculate KPI metrics from predictions"""
    total_units = df_sim['predicciones'].sum()
    total_revenue = (df_sim['predicciones'] * df_sim['precio_venta']).sum()
    avg_price = df_sim['precio_venta'].mean()
    avg_discount = df_sim['descuento_porcentaje'].mean() if 'descuento_porcentaje' in df_sim.columns else 0
    
    return {
        'total_units': total_units,
        'total_revenue': total_revenue,
        'avg_price': avg_price,
        'avg_discount': avg_discount
    }

# ============================================================================
# SIDEBAR CONTROLS
# ============================================================================
st.sidebar.title("⚙️ Simulation Controls")
st.sidebar.markdown("---")

# Load data
model = load_model()
df_inference = load_inference_data()

if model is None or df_inference is None:
    st.error("Could not load model or data. Please check file paths.")
    st.stop()

feature_cols = get_feature_columns(model)
if feature_cols is None:
    st.error("Could not extract feature names from model.")
    st.stop()

# Product selector
products = sorted(df_inference['nombre'].unique())
selected_product = st.sidebar.selectbox(
    "📦 Select Product",
    options=products,
    help="Choose the product to simulate"
)

# Discount slider
discount_slider = st.sidebar.slider(
    "💰 Discount Adjustment",
    min_value=-50,
    max_value=50,
    value=0,
    step=5,
    help="Adjust selling price with discount (-50% to +50%)"
)

# Competition scenario
st.sidebar.markdown("### 🏪 Competition Scenario")
scenario_option = st.sidebar.radio(
    "Select scenario:",
    options=["Actual (0%)", "Competitors -5%", "Competitors +5%"],
    help="Adjust competitor prices"
)

scenario_adjustment = {
    "Actual (0%)": 0,
    "Competitors -5%": -5,
    "Competitors +5%": 5
}[scenario_option]

# Simulate button
st.sidebar.markdown("---")
simulate_button = st.sidebar.button(
    "🚀 Simulate Sales",
    use_container_width=True,
    type="primary"
)

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================
if simulate_button:
    # Filter data for selected product
    df_product = df_inference[df_inference['nombre'] == selected_product].copy()
    
    if len(df_product) == 0:
        st.error(f"No data found for product: {selected_product}")
        st.stop()
    
    # Apply adjustments
    df_product = apply_discount_to_dataframe(df_product, discount_slider)
    df_product = apply_competition_scenario(df_product, scenario_adjustment)
    
    # Generate recursive predictions
    df_sim = simulate_recursive_predictions(
        df_product, model, feature_cols, discount_slider, scenario_adjustment
    )
    
    # Store in session state for persistence
    st.session_state.df_sim = df_sim
    st.session_state.selected_product = selected_product
    st.session_state.discount = discount_slider
    st.session_state.scenario = scenario_option

# Display results if available
if 'df_sim' in st.session_state:
    df_sim = st.session_state['df_sim']
    
    # ========================================================================
    # HEADER
    # ========================================================================
    st.markdown(f"# 📊 Sales Forecast Dashboard - November 2025")
    st.markdown(f"### Product: **{st.session_state['selected_product']}**")
    st.markdown(f"*Discount: {st.session_state['discount']:+d}% | Scenario: {st.session_state['scenario']}*")
    st.markdown("---")
    
    # ========================================================================
    # KPI METRICS
    # ========================================================================
    metrics = calculate_metrics(df_sim)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📦 Total Units",
            f"{metrics['total_units']:.0f}",
            help="Total predicted sales units"
        )
    
    with col2:
        st.metric(
            "💵 Total Revenue",
            f"${metrics['total_revenue']:,.2f}",
            help="Total projected revenue"
        )
    
    with col3:
        st.metric(
            "💲 Avg Price",
            f"${metrics['avg_price']:.2f}",
            help="Average selling price"
        )
    
    with col4:
        st.metric(
            "🏷️ Avg Discount",
            f"{metrics['avg_discount']:.1f}%",
            help="Average discount applied"
        )
    
    st.markdown("---")
    
    # ========================================================================
    # DAILY PREDICTION CHART
    # ========================================================================
    st.subheader("📈 Daily Sales Forecast")
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Plot prediction line
    ax.plot(df_sim['dia_mes'], df_sim['predicciones'], 
            linewidth=3, marker='o', markersize=6, 
            color='#667eea', label='Predicted Sales')
    
    # Highlight Black Friday (Nov 28)
    bf_data = df_sim[df_sim['dia_mes'] == 28]
    if len(bf_data) > 0:
        ax.scatter(28, bf_data['predicciones'].values[0], 
                  s=300, color='#ff6b6b', marker='*', 
                  zorder=5, label='Black Friday')
        ax.axvline(x=28, color='#ff6b6b', linestyle='--', 
                  linewidth=2, alpha=0.5)
        ax.annotate('🎯 Black Friday', 
                   xy=(28, bf_data['predicciones'].values[0]),
                   xytext=(28, bf_data['predicciones'].values[0] * 1.1),
                   ha='center', fontsize=11, fontweight='bold',
                   arrowprops=dict(arrowstyle='->', color='#ff6b6b', lw=2))
    
    ax.set_xlabel('Day of November', fontsize=12, fontweight='bold')
    ax.set_ylabel('Units Sold', fontsize=12, fontweight='bold')
    ax.set_title('November 2025 - Daily Sales Prediction', 
                fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xticks(range(1, 31, 2))
    ax.legend(loc='upper left', fontsize=10)
    
    sns.set_style("whitegrid")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # DETAILED TABLE
    # ========================================================================
    st.subheader("📋 Detailed Daily Breakdown")
    
    # Prepare table data
    table_df = df_sim[['fecha', 'dia_semana', 'precio_venta', 
                       'precio_competencia', 'descuento_porcentaje',
                       'predicciones', 'ratio_precio']].copy()
    
    table_df['fecha'] = table_df['fecha'].dt.strftime('%Y-%m-%d')
    table_df['dia_mes'] = df_sim['dia_mes'].values
    table_df['revenue'] = (df_sim['predicciones'] * df_sim['precio_venta']).values
    table_df = table_df[['dia_mes', 'fecha', 'dia_semana', 'precio_venta', 
                         'precio_competencia', 'descuento_porcentaje',
                         'predicciones', 'ratio_precio', 'revenue']]
    
    table_df.columns = ['Day', 'Date', 'Day of Week', 'Price', 'Comp Price', 
                       'Discount %', 'Units', 'Price Ratio', 'Revenue']
    
    # Format numbers
    table_df['Price'] = table_df['Price'].apply(lambda x: f"${x:.2f}")
    table_df['Comp Price'] = table_df['Comp Price'].apply(lambda x: f"${x:.2f}")
    table_df['Discount %'] = table_df['Discount %'].apply(lambda x: f"{x:.1f}%")
    table_df['Units'] = table_df['Units'].apply(lambda x: f"{x:.1f}")
    table_df['Price Ratio'] = table_df['Price Ratio'].apply(lambda x: f"{x:.2f}")
    table_df['Revenue'] = table_df['Revenue'].apply(lambda x: f"${x:.2f}")
    
    # Display with highlighting for Black Friday
    st.dataframe(table_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # ========================================================================
    # SCENARIO COMPARISON
    # ========================================================================
    st.subheader("📊 Scenario Comparison")
    
    scenarios = {
        "Actual (0%)": 0,
        "Competitors -5%": -5,
        "Competitors +5%": 5
    }
    
    comparison_results = []
    
    with st.spinner("📊 Comparing scenarios..."):
        for scenario_name, adjustment in scenarios.items():
            df_temp = apply_competition_scenario(
                apply_discount_to_dataframe(df_product.copy(), discount_slider),
                adjustment
            )
            df_temp_sim = simulate_recursive_predictions(
                df_temp, model, feature_cols, discount_slider, adjustment
            )
            metrics_temp = calculate_metrics(df_temp_sim)
            
            comparison_results.append({
                'Scenario': scenario_name,
                'Total Units': f"{metrics_temp['total_units']:.0f}",
                'Total Revenue': f"${metrics_temp['total_revenue']:,.2f}",
                'Avg Price': f"${metrics_temp['avg_price']:.2f}"
            })
    
    comparison_df = pd.DataFrame(comparison_results)
    
    col1, col2, col3 = st.columns(3)
    
    for idx, row in comparison_df.iterrows():
        with [col1, col2, col3][idx]:
            st.metric(
                row['Scenario'],
                row['Total Units'],
                f"Revenue: {row['Total Revenue']}"
            )
    
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
else:
    # Initial state - show welcome message
    st.markdown("""
    # 📊 Sales Forecast Simulator - November 2025
    
    Welcome to the interactive sales forecasting dashboard!
    
    ### How to use:
    1. **Select a product** from the dropdown in the sidebar
    2. **Adjust the discount** using the slider (-50% to +50%)
    3. **Choose a competition scenario** to see how competitor pricing affects sales
    4. **Click "Simulate Sales"** to generate predictions
    
    The simulator will:
    - Generate recursive day-by-day predictions for November 2025
    - Update lag variables and moving averages automatically
    - Highlight Black Friday (November 28) with special visualization
    - Show detailed daily metrics and scenario comparisons
    
    ---
    
    ### Features:
    - 📈 **Daily Forecast Chart** - Visualize sales trends with Black Friday highlight
    - 💾 **Detailed Breakdown** - Day-by-day metrics including price, competition, and revenue
    - 🎯 **Scenario Analysis** - Compare 3 different competition scenarios
    - 📊 **KPI Dashboard** - Track total units, revenue, pricing, and discounts
    
    Start by selecting a product and clicking "Simulate Sales"!
    """)