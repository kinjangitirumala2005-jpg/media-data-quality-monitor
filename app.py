
import streamlit as st
import pandas as pd
import great_expectations as gx

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="StreamGuard | Data Quality Monitor",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 2. SESSION STATE
# =====================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "users" not in st.session_state:
    st.session_state.users = {}

if "results" not in st.session_state:
    st.session_state.results = None

# =====================================================
# 3. COLORFUL CUSTOM CSS
# =====================================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(
        135deg,
        #0f172a,
        #172554,
        #312e81
    );
    color: white;
}

/* Main headings */
h1 {
    color: #67e8f9 !important;
    font-weight: 800 !important;
}

h2, h3 {
    color: #c4b5fd !important;
}

/* Authentication heading */
.auth-title {
    text-align: center;
    font-size: 38px;
    font-weight: 900;
    background: linear-gradient(
        90deg,
        #38bdf8,
        #a78bfa,
        #f472b6
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding: 15px;
}

.auth-subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 16px;
    line-height: 1.8;
    margin-bottom: 25px;
}

/* Authentication card */
[data-testid="stForm"] {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(167,139,250,0.4);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 10px 35px rgba(0,0,0,0.3);
}

/* Input fields */
.stTextInput input {
    background-color: #1e293b !important;
    color: white !important;
    border: 1px solid #6366f1 !important;
    border-radius: 10px !important;
}

/* Labels */
.stTextInput label {
    color: #e0e7ff !important;
    font-weight: 600;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    color: #c4b5fd;
    font-weight: bold;
    font-size: 16px;
}

.stTabs [aria-selected="true"] {
    color: #38bdf8 !important;
}

/* Buttons */
.stButton button,
.stFormSubmitButton button {
    background: linear-gradient(
        90deg,
        #2563eb,
        #7c3aed,
        #db2777
    ) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 20px !important;
    font-weight: bold !important;
    transition: 0.3s ease;
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(124,58,237,0.5);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #172554,
        #312e81
    );
}

/* Dashboard metrics */
[data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        #1e3a8a,
        #4c1d95
    );
    border: 1px solid #818cf8;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

[data-testid="stMetricLabel"] {
    color: #bfdbfe !important;
}

[data-testid="stMetricValue"] {
    color: white !important;
    font-weight: bold;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #6366f1;
    border-radius: 12px;
    overflow: hidden;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(99,102,241,0.12);
    border: 1px dashed #a78bfa;
    border-radius: 12px;
    padding: 12px;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Dividers */
hr {
    border-color: #6366f1 !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# 4. LOGIN AND REGISTRATION SYSTEM
# =====================================================

if not st.session_state.authenticated:

    st.markdown("""
    <div class="auth-title">
        🎬 STREAMGUARD
    </div>

    <div class="auth-subtitle">
        Intelligent Media Streaming Data Quality Platform
        <br>
        Secure Access | Smart Validation | Data Monitoring
    </div>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([1, 1.8, 1])

    with center:

        login_tab, signup_tab = st.tabs(
            ["🔐 LOGIN", "📝 SIGN UP"]
        )

        # ---------------- LOGIN PAGE ----------------

        with login_tab:

            st.subheader("Welcome Back")

            st.write("Sign in to access your dashboard.")

            with st.form("login_form"):

                login_username = st.text_input(
                    "Username",
                    placeholder="Enter your username"
                )

                login_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password"
                )

                login_button = st.form_submit_button(
                    "Login →",
                    use_container_width=True
                )

                if login_button:

                    registered_password = (
                        st.session_state.users.get(
                            login_username.strip()
                        )
                    )

                    if (
                        registered_password is not None
                        and registered_password == login_password
                    ):

                        st.session_state.authenticated = True
                        st.success("Login successful!")
                        st.rerun()

                    else:

                        st.error(
                            "Invalid username or password. "
                            "Please register first."
                        )

        # ---------------- SIGN UP PAGE ----------------

        with signup_tab:

            st.subheader("Create Your Account")

            st.write("Register to access the monitoring platform.")

            with st.form("signup_form"):

                full_name = st.text_input(
                    "Full Name",
                    placeholder="Enter your full name"
                )

                new_username = st.text_input(
                    "Create Username",
                    placeholder="Choose a username"
                )

                new_password = st.text_input(
                    "Create Password",
                    type="password",
                    placeholder="Minimum 8 characters"
                )

                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Re-enter your password"
                )

                signup_button = st.form_submit_button(
                    "Create Account →",
                    use_container_width=True
                )

                if signup_button:

                    username = new_username.strip()

                    if not all([
                        full_name.strip(),
                        username,
                        new_password,
                        confirm_password
                    ]):

                        st.error("Please complete all fields.")

                    elif len(new_password) < 8:

                        st.error(
                            "Password must contain at least 8 characters."
                        )

                    elif new_password != confirm_password:

                        st.error("Passwords do not match.")

                    elif username in st.session_state.users:

                        st.error("Username already exists.")

                    else:

                        st.session_state.users[username] = new_password

                        st.success(
                            "Account created successfully! "
                            "Please login."
                        )

    st.stop()

# =====================================================
# 5. DASHBOARD
# =====================================================

st.title("🎬 STREAMGUARD")
st.subheader("Media Streaming Data Quality Monitor")

st.caption(
    "Data Quality Validation and Monitoring "
    "| Python | Pandas | Great Expectations"
)

# =====================================================
# 6. SIDEBAR
# =====================================================

with st.sidebar:

    st.title("⚙️ Dashboard Controls")

    st.success("Logged in successfully")

    if st.button("🚪 Logout", use_container_width=True):

        st.session_state.authenticated = False
        st.session_state.results = None
        st.rerun()

    st.divider()

    st.subheader("Upload Dataset")

    uploaded_file = st.file_uploader(
        "Upload Streaming Event CSV",
        type=["csv"]
    )

    st.info(
        "Upload media streaming event logs "
        "to perform data quality checks."
    )

# =====================================================
# 7. DATA LOADING
# =====================================================

if uploaded_file is not None:

    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Unable to read CSV: {e}")
        st.stop()

else:

    try:
        df = pd.read_csv("streaming_events.csv")

    except FileNotFoundError:

        st.warning(
            "No dataset available. Please upload a CSV file."
        )
        st.stop()

required_columns = [
    "event_id",
    "user_id",
    "event_type",
    "watch_duration",
    "device",
    "timestamp"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    st.error(
        f"Required columns missing: {missing_columns}"
    )
    st.stop()

# =====================================================
# 8. DATASET OVERVIEW
# =====================================================

st.divider()
st.header("📊 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Records",
    f"{len(df):,}"
)

col2.metric(
    "Total Columns",
    len(df.columns)
)

col3.metric(
    "Missing Values",
    int(df.isnull().sum().sum())
)

col4.metric(
    "Duplicate Event IDs",
    int(df["event_id"].duplicated().sum())
)

# =====================================================
# 9. EVENT DATA PREVIEW
# =====================================================

st.header("📁 Streaming Event Data")

st.dataframe(
    df.head(20),
    use_container_width=True,
    hide_index=True
)

# =====================================================
# 10. DATA QUALITY VALIDATION
# =====================================================

st.divider()
st.header("🔍 Data Quality Validation")

if st.button(
    "🚀 Run Pipeline Validation",
    type="primary",
    use_container_width=True
):

    results = []

    def check(rule, condition):

        results.append({
            "Validation Rule": rule,
            "Status": "PASS" if bool(condition) else "FAIL"
        })

    with st.spinner("Validating streaming event data..."):

        # Rule 1: Null user IDs

        check(
            "User ID should not contain null values",
            df["user_id"].notna().all()
        )

        # Rule 2: Unique event IDs

        check(
            "Event ID should be unique",
            df["event_id"].is_unique
        )

        # Rule 3: Valid event types

        check(
            "Event type should be valid",
            df["event_type"].isin([
                "play",
                "pause",
                "login",
                "subscription"
            ]).all()
        )

        # Rule 4: Watch duration validation

        duration = pd.to_numeric(
            df["watch_duration"],
            errors="coerce"
        )

        check(
            "Watch duration must be between 0 and 1440",
            duration.notna().all()
            and duration.between(0, 1440).all()
        )

        # Rule 5: Device validation

        check(
            "Device type should be valid",
            df["device"].isin([
                "mobile",
                "desktop",
                "smart_tv",
                "tablet"
            ]).all()
        )

        # Rule 6: Timestamp validation

        timestamps = pd.to_datetime(
            df["timestamp"],
            errors="coerce"
        )

        check(
            "Event timestamp should be valid",
            timestamps.notna().all()
        )

        result_df = pd.DataFrame(results)

        passed = sum(
            item["Status"] == "PASS"
            for item in results
        )

        failed = len(results) - passed

        # ---------------- GREAT EXPECTATIONS ----------------

        gx_status = "NOT RUN"
        gx_error = None

        try:

            context = gx.get_context(
                mode="ephemeral"
            )

            datasource = (
                context.data_sources.add_pandas(
                    name="media_streaming_datasource"
                )
            )

            asset = datasource.add_dataframe_asset(
                name="streaming_event_logs"
            )

            batch_definition = (
                asset.add_batch_definition_whole_dataframe(
                    "streaming_batch"
                )
            )

            batch = batch_definition.get_batch(
                batch_parameters={
                    "dataframe": df
                }
            )

            expectation = (
                gx.expectations.ExpectTableRowCountToBeBetween(
                    min_value=1
                )
            )

            gx_result = batch.validate(expectation)

            gx_status = (
                "PASS" if gx_result.success else "FAIL"
            )

        except Exception as e:

            gx_error = str(e)

        st.session_state.results = result_df
        st.session_state.passed = passed
        st.session_state.failed = failed
        st.session_state.gx_status = gx_status
        st.session_state.gx_error = gx_error

# =====================================================
# 11. VALIDATION RESULTS
# =====================================================

if st.session_state.results is not None:

    st.divider()

    st.header("📈 Validation Results")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Rules", 6)

    col2.metric(
        "Passed Rules",
        st.session_state.passed
    )

    col3.metric(
        "Failed Rules",
        st.session_state.failed
    )

    st.dataframe(
        st.session_state.results,
        use_container_width=True,
        hide_index=True
    )

    # ---------------- GREAT EXPECTATIONS ----------------

    st.subheader("🧪 Great Expectations Engine")

    if st.session_state.gx_status == "PASS":

        st.success(
            "Great Expectations row-count validation passed."
        )

    elif st.session_state.gx_status == "FAIL":

        st.error(
            "Great Expectations row-count validation failed."
        )

    else:

        st.warning(
            "Great Expectations validation could not run."
        )

    if st.session_state.gx_error:

        st.code(st.session_state.gx_error)

    # ---------------- MONITORING CHART ----------------

    st.subheader("📊 Data Quality Monitoring")

    chart_data = (
        st.session_state.results["Status"]
        .value_counts()
    )

    st.bar_chart(chart_data)

    # ---------------- QUALITY GATE ----------------

    st.subheader("🚦 Pipeline Quality Gate")

    if (
        st.session_state.failed == 0
        and st.session_state.gx_status == "PASS"
    ):

        st.success(
            "QUALITY GATE PASSED - Pipeline can proceed."
        )

    else:

        st.error(
            "QUALITY GATE FAILED - Pipeline execution blocked."
        )

    # ---------------- DOWNLOAD REPORT ----------------

    st.download_button(
        label="⬇️ Download Validation Report",
        data=st.session_state.results.to_csv(index=False),
        file_name="data_quality_report.csv",
        mime="text/csv"
    )

# =====================================================
# 12. FOOTER
# =====================================================

st.divider()

st.markdown("""
<div style="
    text-align:center;
    color:#a5b4fc;
    padding:15px;
">
    🎬 <b>STREAMGUARD</b><br>
    Media Streaming Data Quality Monitoring System<br>
    Python | Pandas | Great Expectations | Streamlit
</div>
""", unsafe_allow_html=True)
