import streamlit as st
import pandas as pd
import datetime

# Set page configuration
st.set_page_config(
    page_title="Weight Loss Planner",
    page_icon="📊",
    layout="wide"
)

# Modern, minimalist CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;600;800&display=swap');

    .stApp {
        background-color: #ffffff;
        font-family: 'Manrope', sans-serif;
        color: #1a1a2e;
    }

    .main-header {
        text-align: center;
        font-weight: 800;
        margin-bottom: 30px;
        color: #16213e;
        font-size: 2.5rem;
        border-bottom: 3px solid #e94560;
        padding-bottom: 15px;
    }

    .stMetric {
        background-color: #f4f4f4;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .stMetric:hover {
        background-color: #e9e9e9;
        transform: scale(1.02);
    }
    .stMetric div:first-child {
        color: #495057;
        font-size: 0.85rem;
        text-transform: uppercase;
        margin-bottom: 5px;
        font-weight: 600;
    }
    .stMetric div:last-child {
        color: #0f3460;
        font-weight: 700;
        font-size: 1.3rem;
    }

    .projection-metrics {
        display: flex;
        justify-content: center;
        gap: 40px;
        margin-bottom: 30px;
    }
    .projection-metric {
        background-color: #f4f4f4;
        border-radius: 10px;
        padding: 15px;
        min-width: 250px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin: 10px 0;
    }
    .projection-metric .metric-label {
        color: #495057;
        font-size: 0.9rem;
        text-transform: uppercase;
        margin-bottom: 8px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .projection-metric .metric-value {
        color: #0f3460;
        font-weight: 800;
        font-size: 1.2rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f4f4f4;
        border-radius: 10px;
        margin: 0 10px;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e9e9e9;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #e94560;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for tracking
if 'weight_log' not in st.session_state:
    st.session_state.weight_log = []
if 'current_weight' not in st.session_state:
    st.session_state.current_weight = 150.0
if 'goal_weight' not in st.session_state:
    st.session_state.goal_weight = 120.0
if 'bmr' not in st.session_state:
    st.session_state.bmr = 0

# Custom function to render metrics
def render_projection_metric(label, value):
    st.markdown(f'''
    <div class="projection-metric">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    ''', unsafe_allow_html=True)

# Title 
st.markdown('<h1 class="main-header">📊 Weight Loss Journey Planner</h1>', unsafe_allow_html=True)

# Sidebar Inputs
with st.sidebar:
    st.header("User Information")
    age = st.number_input("Age", 18, 100, 30, step=1)
    sex = st.radio("Sex", ('Male', 'Female'), index=1)
    height_inches = st.number_input("Height (inches)", 55.0, 85.0, 66.0, step=0.1)
    st.session_state.goal_weight = st.number_input(
        "Target Weight (lbs)", 
        min_value=50.0, 
        max_value=500.0, 
        value=st.session_state.goal_weight, 
        step=0.5
    )

    st.markdown("---")
    st.header("Progress Parameters")
    calorie_intake = st.slider("Daily Calorie Intake", 500, 2500, 1500, step=50)
    fasting_days = st.slider("Fasting Days Per Week", 0, 5, 0)
    barre_sessions = st.slider("Barre Sessions Per Week", 0, 7, 0)
    additional_steps = st.slider("Additional Daily Steps", 0, 20000, 500, step=500)

# BMR Calculation Function
def calculate_bmr(weight, age, height_inches, sex):
    height_cm = height_inches * 2.54
    weight_kg = weight * 0.453592
    if sex == 'Male':
        return ((10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5) * 1.1
    else:
        return ((10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161) * 1.1

# Function to calculate weight loss timeline
def calculate_weight_loss_timeline():
    weight = st.session_state.current_weight
    goal_weight = st.session_state.goal_weight
    bmr = calculate_bmr(weight, age, height_inches, sex)
    st.session_state.bmr = bmr

    calories_per_lb = 3500
    barre_calories = 210
    calories_per_1000_steps = 30
    typical_daily_activity = 200
    daily_deficit_list = []
    weight_list = []
    date_list = []
    start_date = datetime.date.today()
    days = 0

    while weight > goal_weight:
        days += 1
        daily_burn = bmr + activity_calories
        if days % 7 < barre_sessions:
            daily_burn += barre_calories
        daily_intake = 500 if days % 7 < fasting_days else calorie_intake
        weight -= (daily_burn - daily_intake) / calories_per_lb
        weight_list.append(round(weight, 1))
        date_list.append(start_date + datetime.timedelta(days=days))

    return date_list, weight_list, days

# Tabs for different functionalities
tab1, tab2 = st.tabs(["Weight Projection 📊", "Log Your Weight 📈"])

bmr_value = calculate_bmr(st.session_state.current_weight, age, height_inches, sex)
typical_daily_activity = 200
activity_calories = (additional_steps / 1000 * 30) + (barre_sessions * 210 / 7) + typical_daily_activity
total_burn = bmr_value + activity_calories
net_deficit = total_burn - calorie_intake

# Main metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Resting BMR", f"{round(bmr_value, 2)} kcal/day")
with col2:
    st.metric("Total Calories Burned", f"{round(total_burn, 2)} kcal/day")
with col3:
    st.metric("Net Caloric Deficit", f"{round(net_deficit, 2)} kcal/day")

with tab1:
    daily_dates, daily_weights, days = calculate_weight_loss_timeline()
    projected_end_date = datetime.date.today() + datetime.timedelta(days=days)
    
    # Custom metrics rendering
    st.markdown('<div class="projection-metrics">', unsafe_allow_html=True)
    render_projection_metric("Projected Duration", f"{days} days ({round(days/7, 1)} weeks)")
    render_projection_metric("Projected End Date", projected_end_date.strftime("%B %d, %Y"))
    st.markdown('</div>', unsafe_allow_html=True)
    
    weight_df = pd.DataFrame({'Date': daily_dates, 'Weight (lbs)': daily_weights})
    
    # Modify line chart with custom configuration
    st.line_chart(
        data=weight_df.set_index('Date'),
        use_container_width=True,
    )

with tab2:
    st.subheader("Log Your Progress")
    log_weight = st.number_input("Today's Weight (lbs)", 50.0, 500.0, st.session_state.current_weight, step=0.1)
    if st.button("Log Weight"):
        st.session_state.current_weight = log_weight
        st.session_state.weight_log.append({'date': datetime.date.today().isoformat(), 'weight': log_weight})
        st.success("Weight logged successfully!")
        st.rerun()
    
    if st.session_state.weight_log:
        weight_history = pd.DataFrame(st.session_state.weight_log)
        weight_history['date'] = pd.to_datetime(weight_history['date'])
        st.line_chart(weight_history.set_index('date'))
