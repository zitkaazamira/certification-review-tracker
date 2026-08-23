
import io
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Certification Review Tracker",
    page_icon="🌷",
    layout="wide",
)

# ---------- Styling ----------
st.markdown(
    """
    <style>
    :root {
        --cream: #FFF9F5;
        --rose: #E8C7CF;
        --dusty: #C98FA1;
        --plum: #6F3A4E;
        --ink: #3D2B32;
        --soft: #F8ECEF;
        --line: #EADDE1;
    }

    .stApp {
        background: var(--cream);
        color: var(--ink);
    }

    .block-container {
        max-width: 1280px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: var(--plum);
        letter-spacing: -0.02em;
    }

    .hero {
        padding: 1.6rem 1.7rem;
        border: 1px solid var(--line);
        border-radius: 20px;
        background: linear-gradient(135deg, #FFFDFC 0%, #F9EDEF 100%);
        margin-bottom: 1.2rem;
    }

    .hero h1 {
        margin: 0;
        font-size: 2.35rem;
        line-height: 1.05;
    }

    .hero p {
        margin: 0.55rem 0 0;
        font-size: 1rem;
        color: #6E5961;
        max-width: 760px;
    }

    .metric-card {
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 1rem 1.05rem;
        min-height: 104px;
    }

    .metric-label {
        font-size: 0.8rem;
        color: #8A707A;
        margin-bottom: 0.35rem;
    }

    .metric-value {
        font-size: 1.65rem;
        font-weight: 700;
        color: var(--plum);
        line-height: 1.1;
    }

    .section-card {
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 1.2rem;
        margin-top: 1rem;
    }

    .small-note {
        font-size: 0.83rem;
        color: #806A73;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        border-radius: 14px;
        overflow: hidden;
    }

    div.stButton > button,
    div.stDownloadButton > button {
        border-radius: 12px;
        border: 1px solid #C99AA8;
        background: #7A3E57;
        color: white;
        font-weight: 600;
    }

    div.stButton > button:hover,
    div.stDownloadButton > button:hover {
        background: #673247;
        border-color: #673247;
        color: white;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: #F7EAEE;
        border-radius: 10px 10px 0 0;
        color: #6F3A4E;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .stTabs [aria-selected="true"] {
        background: #7A3E57 !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- Helpers ----------
REVIEW_DATE = pd.Timestamp("2026-08-23")

REQUIRED_COLUMNS = [
    "record_id",
    "product_name",
    "vendor",
    "product_category",
    "crypto_module",
    "algorithm",
    "certificate_number",
    "certificate_status",
    "cmvp_status",
    "postel_status",
    "issue_date",
    "expiry_date",
    "last_verified",
]


@st.cache_data
def load_sample_data():
    return pd.read_excel(
        "sample_data/certification_review_sample_data.xlsx",
        sheet_name="certification_records",
    )


def read_uploaded_file(uploaded_file):
    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    if name.endswith(".xlsx") or name.endswith(".xls"):
        return pd.read_excel(uploaded_file)
    raise ValueError("Unsupported file format")


def prepare_dates(df):
    date_cols = ["issue_date", "expiry_date", "last_verified"]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def missing_required_columns(df):
    return [col for col in REQUIRED_COLUMNS if col not in df.columns]


def validate_records(df):
    checked = prepare_dates(df.copy())

    required_fields = [
        "vendor",
        "algorithm",
        "certificate_number",
        "cmvp_status",
        "postel_status",
    ]

    duplicate_mask = (
        checked["certificate_number"]
        .astype("string")
        .duplicated(keep=False)
        & checked["certificate_number"].notna()
    )

    issue_list = []
    status_list = []
    priority_list = []

    for idx, row in checked.iterrows():
        issues = []
        priority = "Low"

        missing_fields = [
            col for col in required_fields
            if pd.isna(row.get(col)) or str(row.get(col)).strip() == ""
        ]

        if missing_fields:
            issues.append("Missing: " + ", ".join(missing_fields))
            priority = "High"

        if duplicate_mask.loc[idx]:
            issues.append("Duplicate certificate number")
            priority = "High"

        expiry = row.get("expiry_date")
        cert_status = str(row.get("certificate_status", "")).strip()

        if pd.notna(expiry):
            if expiry < REVIEW_DATE:
                issues.append("Certificate expired")
                priority = "Critical"
            elif REVIEW_DATE <= expiry <= REVIEW_DATE + pd.Timedelta(days=30):
                issues.append("Certificate expires within 30 days")
                if priority == "Low":
                    priority = "Medium"

        if (
            pd.notna(expiry)
            and expiry < REVIEW_DATE
            and cert_status.lower() == "active"
        ):
            issues.append("Status and expiry date do not match")
            priority = "Critical"

        cmvp = str(row.get("cmvp_status", "")).strip().lower()
        postel = str(row.get("postel_status", "")).strip().lower()

        external_issue = False
        if cmvp in {"pending", "not found"}:
            issues.append(f"CMVP status: {row.get('cmvp_status')}")
            external_issue = True

        if postel in {"pending", "not found"}:
            issues.append(f"Postel status: {row.get('postel_status')}")
            external_issue = True

        if external_issue and priority in {"Low", "Medium"}:
            priority = "High"

        if cert_status.lower() == "revoked":
            issues.append("Certificate revoked")
            priority = "Critical"

        if issues:
            issue_list.append("; ".join(dict.fromkeys(issues)))
            status_list.append("Need Review")
        else:
            issue_list.append("No issue found")
            status_list.append("Clear")
            priority = "Low"

        priority_list.append(priority)

    checked["review_status"] = status_list
    checked["priority"] = priority_list
    checked["issue_found"] = issue_list

    return checked


def make_download(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="review_results")
    output.seek(0)
    return output


# ---------- Hero ----------
st.markdown(
    """
    <div class="hero">
        <h1>Certification Review Tracker</h1>
        <p>
            Check certification records, spot incomplete or inconsistent data,
            and keep the items that need another review in one place.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "Portfolio simulation using synthetic data. No internal or confidential BSSN records are used."
)

# ---------- Data source ----------
st.subheader("Choose your data")

source = st.radio(
    "Data source",
    ["Use sample data", "Upload a file"],
    horizontal=True,
    label_visibility="collapsed",
)

df = None

if source == "Use sample data":
    try:
        df = load_sample_data()
        st.success("Sample data loaded.")
    except Exception:
        st.error(
            "Sample file was not found. Make sure "
            "`sample_data/certification_review_sample_data.xlsx` exists in the repository."
        )
else:
    uploaded = st.file_uploader(
        "Upload a CSV or Excel file",
        type=["csv", "xlsx", "xls"],
    )
    if uploaded is not None:
        try:
            df = read_uploaded_file(uploaded)
            st.success(f"{uploaded.name} loaded.")
        except Exception as exc:
            st.error(f"Could not read the file: {exc}")

if df is None:
    st.info("Choose the sample data or upload a file to continue.")
    st.stop()

missing_cols = missing_required_columns(df)

if missing_cols:
    st.error(
        "The file is missing these required columns: "
        + ", ".join(missing_cols)
    )
    st.stop()

# ---------- Run validation ----------
st.markdown("---")
left, right = st.columns([1, 4])

with left:
    run = st.button("Check records", use_container_width=True)

with right:
    st.markdown(
        '<div class="small-note">The checks cover required fields, duplicate certificate numbers, expiry dates, status mismatches, external verification status, and revoked certificates.</div>',
        unsafe_allow_html=True,
    )

if "checked_data" not in st.session_state:
    st.session_state.checked_data = None

if run:
    st.session_state.checked_data = validate_records(df)

if st.session_state.checked_data is None:
    st.stop()

result = st.session_state.checked_data.copy()

# ---------- Metrics ----------
total_records = len(result)
need_review = (result["review_status"] == "Need Review").sum()
clear_records = (result["review_status"] == "Clear").sum()
critical_records = (result["priority"] == "Critical").sum()
clear_rate = (clear_records / total_records * 100) if total_records else 0

st.subheader("Review summary")

metrics = [
    ("Records checked", f"{total_records:,}"),
    ("Clear", f"{clear_records:,}"),
    ("Need review", f"{need_review:,}"),
    ("Clear rate", f"{clear_rate:.1f}%"),
    ("Critical", f"{critical_records:,}"),
]

cols = st.columns(5)

for col, (label, value) in zip(cols, metrics):
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------- Tabs ----------
tab1, tab2, tab3 = st.tabs(
    ["Review queue", "All records", "Issue summary"]
)

with tab1:
    st.subheader("Records that need attention")

    review_df = result[result["review_status"] == "Need Review"].copy()

    f1, f2, f3 = st.columns(3)

    with f1:
        selected_priority = st.multiselect(
            "Priority",
            ["Critical", "High", "Medium", "Low"],
            default=["Critical", "High", "Medium"],
        )

    with f2:
        categories = sorted(
            review_df["product_category"].dropna().astype(str).unique().tolist()
        )
        selected_category = st.multiselect(
            "Product category",
            categories,
            default=[],
        )

    with f3:
        vendors = sorted(
            review_df["vendor"].dropna().astype(str).unique().tolist()
        )
        selected_vendor = st.multiselect(
            "Vendor",
            vendors,
            default=[],
        )

    filtered = review_df.copy()

    if selected_priority:
        filtered = filtered[filtered["priority"].isin(selected_priority)]

    if selected_category:
        filtered = filtered[
            filtered["product_category"].astype(str).isin(selected_category)
        ]

    if selected_vendor:
        filtered = filtered[
            filtered["vendor"].astype(str).isin(selected_vendor)
        ]

    display_cols = [
        "record_id",
        "product_name",
        "vendor",
        "product_category",
        "certificate_number",
        "certificate_status",
        "cmvp_status",
        "postel_status",
        "expiry_date",
        "priority",
        "issue_found",
    ]

    st.dataframe(
        filtered[display_cols],
        use_container_width=True,
        hide_index=True,
        height=460,
    )

    st.caption(f"{len(filtered):,} records shown.")

with tab2:
    st.subheader("Checked records")

    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True,
        height=500,
    )

    download_data = make_download(result)

    st.download_button(
        "Download checked data",
        data=download_data,
        file_name="certification_review_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=False,
    )

with tab3:
    st.subheader("What was found")

    issue_rows = (
        result.loc[result["review_status"] == "Need Review", ["priority", "issue_found"]]
        .copy()
    )

    if issue_rows.empty:
        st.success("No review issues were found.")
    else:
        priority_summary = (
            issue_rows["priority"]
            .value_counts()
            .rename_axis("priority")
            .reset_index(name="records")
        )

        st.dataframe(
            priority_summary,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("#### Most common issue notes")

        issue_summary = (
            issue_rows["issue_found"]
            .value_counts()
            .head(12)
            .rename_axis("issue")
            .reset_index(name="records")
        )

        st.dataframe(
            issue_summary,
            use_container_width=True,
            hide_index=True,
        )

st.markdown("---")
st.caption("Built as a portfolio project with synthetic certification data.")
