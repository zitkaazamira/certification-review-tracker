import random
import textwrap
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Certification Review Tracker",
    page_icon="🌷",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# HELPERS
# =========================================================

def html(content):
    st.markdown(
        textwrap.dedent(content).strip(),
        unsafe_allow_html=True,
    )


def metric_card(label, value, note):
    return textwrap.dedent(
        f"""
        <div class="metric-box">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{note}</div>
        </div>
        """
    ).strip()


def issue_bar(label, value, max_value):
    width = 0 if max_value == 0 else value / max_value * 100

    return textwrap.dedent(
        f"""
        <div class="insight-card">
            <div class="insight-head">
                <div class="insight-name">{label}</div>
                <div class="insight-value">{value:,}</div>
            </div>

            <div class="bar-track">
                <div
                    class="bar-fill"
                    style="width:{width:.1f}%"
                ></div>
            </div>
        </div>
        """
    ).strip()


def to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8-sig")


def percent(part, total):
    if total == 0:
        return 0
    return part / total * 100


# =========================================================
# STYLING
# =========================================================

st.markdown(
    """
    <style>

    :root {
        --ink: #402E38;
        --muted: #806A75;
        --plum: #7A3E61;
        --berry: #AA557B;
        --rose: #EFA8BC;
        --peach: #F7C4AE;
        --lavender: #DCCAF4;
        --cream: #FFF9F6;
        --line: rgba(122,62,97,0.13);
        --white: rgba(255,255,255,0.88);
    }

    .stApp {
        background:
            radial-gradient(
                circle at 8% 8%,
                rgba(247,196,174,0.34),
                transparent 24%
            ),
            radial-gradient(
                circle at 90% 12%,
                rgba(220,202,244,0.34),
                transparent 25%
            ),
            radial-gradient(
                circle at 80% 80%,
                rgba(239,168,188,0.20),
                transparent 24%
            ),
            linear-gradient(
                180deg,
                #FFFDFC 0%,
                #FFF7F9 48%,
                #FFF9F6 100%
            );

        color: var(--ink);
    }

    .block-container {
        max-width: 1240px;
        padding-top: 5.4rem;
        padding-bottom: 4rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    h1, h2, h3 {
        color: var(--ink);
    }

    .hero-shell {
        position: relative;
        overflow: hidden;
        border-radius: 28px;
        border: 1px solid var(--line);

        padding: 2.25rem;

        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.96),
                rgba(255,239,244,0.90)
            );

        box-shadow:
            0 18px 42px rgba(113,62,86,0.10);

        margin-bottom: 1rem;
    }

    .hero-shell::after {
        content: "";
        position: absolute;

        width: 230px;
        height: 230px;

        right: -70px;
        top: -75px;

        border-radius: 50%;

        background:
            linear-gradient(
                135deg,
                rgba(239,168,188,0.45),
                rgba(220,202,244,0.42)
            );
    }

    .hero-kicker {
        position: relative;
        z-index: 2;

        display: inline-block;

        padding: 0.42rem 0.72rem;

        border-radius: 999px;

        background: rgba(122,62,97,0.08);

        color: var(--plum);

        font-size: 0.78rem;
        font-weight: 700;

        margin-bottom: 0.9rem;
    }

    .hero-title {
        position: relative;
        z-index: 2;

        margin: 0;

        max-width: 760px;

        color: var(--ink);

        font-size: clamp(
            2.45rem,
            5vw,
            4.2rem
        );

        line-height: 1;
        letter-spacing: -0.035em;
        font-weight: 800;
    }

    .hero-copy {
        position: relative;
        z-index: 2;

        margin-top: 1rem;

        max-width: 760px;

        color: var(--muted);

        font-size: 1.02rem;
        line-height: 1.7;
    }

    .hero-tags {
        position: relative;
        z-index: 2;

        display: flex;
        flex-wrap: wrap;

        gap: 0.55rem;

        margin-top: 1.15rem;
    }

    .hero-tag {
        display: inline-block;

        padding: 0.45rem 0.72rem;

        border-radius: 999px;

        background: rgba(255,255,255,0.82);

        border: 1px solid var(--line);

        color: #674C59;

        font-size: 0.82rem;
        font-weight: 600;
    }

    .soft-note {
        color: #8A7480;

        font-size: 0.86rem;
        line-height: 1.5;

        margin: 0.8rem 0 1.6rem;
    }

    .section-label {
        color: var(--berry);

        font-size: 0.76rem;
        font-weight: 800;

        text-transform: uppercase;
        letter-spacing: 0.1em;

        margin-bottom: 0.25rem;
    }

    .section-title {
        color: var(--ink);

        margin: 0;

        font-size: 2rem;
        line-height: 1.15;

        letter-spacing: -0.025em;
    }

    .section-copy {
        color: var(--muted);

        line-height: 1.65;

        margin-top: 0.45rem;
        margin-bottom: 1.1rem;
    }

    .step-grid {
        display: grid;

        grid-template-columns:
            repeat(4, minmax(0, 1fr));

        gap: 0.85rem;

        margin: 1rem 0 1.6rem;
    }

    .step-card {
        padding: 1rem 1.05rem;

        min-height: 112px;

        border-radius: 20px;

        border: 1px solid var(--line);

        background:
            rgba(255,255,255,0.87);

        box-shadow:
            0 9px 22px rgba(113,62,86,0.06);
    }

    .step-num {
        color: var(--berry);

        font-size: 0.75rem;
        font-weight: 800;

        margin-bottom: 0.45rem;
    }

    .step-name {
        color: var(--ink);

        font-size: 0.96rem;
        font-weight: 750;
    }

    .step-desc {
        color: var(--muted);

        margin-top: 0.25rem;

        font-size: 0.8rem;
        line-height: 1.45;
    }

    .status-row {
        display: flex;
        flex-wrap: wrap;

        gap: 0.55rem;

        margin: 0.6rem 0 0.9rem;
    }

    .status-pill {
        display: inline-block;

        padding: 0.45rem 0.7rem;

        border-radius: 999px;

        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.9),
                rgba(252,235,241,0.82)
            );

        border: 1px solid var(--line);

        color: #6B5160;

        font-size: 0.78rem;
        font-weight: 700;
    }

    .metric-grid {
        display: grid;

        grid-template-columns:
            repeat(5, minmax(0, 1fr));

        gap: 0.85rem;

        margin: 1rem 0 1.4rem;
    }

    .metric-box {
        position: relative;
        overflow: hidden;

        min-height: 118px;

        padding: 1rem 1.05rem;

        border-radius: 22px;

        border: 1px solid var(--line);

        background:
            rgba(255,255,255,0.9);

        box-shadow:
            0 10px 24px rgba(113,62,86,0.07);
    }

    .metric-box::before {
        content: "";

        position: absolute;

        width: 62px;
        height: 62px;

        right: -16px;
        top: -15px;

        border-radius: 50%;

        background:
            linear-gradient(
                135deg,
                rgba(239,168,188,0.43),
                rgba(220,202,244,0.42)
            );
    }

    .metric-label {
        position: relative;
        z-index: 2;

        color: #8A7480;

        font-size: 0.78rem;
        font-weight: 650;
    }

    .metric-value {
        position: relative;
        z-index: 2;

        margin-top: 0.35rem;

        color: var(--plum);

        font-size: 2rem;
        font-weight: 800;

        line-height: 1;
    }

    .metric-sub {
        position: relative;
        z-index: 2;

        margin-top: 0.5rem;

        color: #99828D;

        font-size: 0.72rem;
    }

    .insight-card {
        padding: 1rem 1.05rem;

        border-radius: 20px;

        border: 1px solid var(--line);

        background:
            rgba(255,255,255,0.86);

        box-shadow:
            0 8px 21px rgba(113,62,86,0.055);

        margin-bottom: 0.7rem;
    }

    .insight-head {
        display: flex;

        justify-content:
            space-between;

        align-items: center;

        gap: 1rem;

        margin-bottom: 0.55rem;
    }

    .insight-name {
        color: var(--ink);

        font-size: 0.87rem;
        font-weight: 700;
    }

    .insight-value {
        color: var(--plum);

        font-size: 0.83rem;
        font-weight: 800;
    }

    .bar-track {
        width: 100%;
        height: 9px;

        border-radius: 999px;

        background: #F1E8EC;

        overflow: hidden;
    }

    .bar-fill {
        height: 100%;

        border-radius: 999px;

        background:
            linear-gradient(
                90deg,
                #B75D84,
                #E9A3B7,
                #D6B9EE
            );
    }

    div[data-testid="stDataFrame"] {
        border-radius: 18px;

        border: 1px solid var(--line);

        overflow: hidden;

        background: white;

        box-shadow:
            0 8px 20px rgba(113,62,86,0.05);
    }

    div.stButton > button,
    div.stDownloadButton > button {
        min-height: 46px;

        border: 0;

        border-radius: 14px;

        color: white;

        font-weight: 750;

        background:
            linear-gradient(
                135deg,
                #8E4669,
                #B95D86
            );

        box-shadow:
            0 7px 18px rgba(142,70,105,0.22);
    }

    div.stButton > button:hover,
    div.stDownloadButton > button:hover {
        color: white;

        background:
            linear-gradient(
                135deg,
                #7C3A5A,
                #A95076
            );
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.45rem;

        background:
            rgba(255,255,255,0.65);

        padding: 0.35rem;

        border-radius: 16px;

        border: 1px solid var(--line);

        width: fit-content;
    }

    .stTabs [data-baseweb="tab"] {
        height: 42px;

        padding: 0 1rem;

        border-radius: 12px;

        color: #755665;

        font-weight: 650;
    }

    .stTabs [aria-selected="true"] {
        color: white !important;

        background:
            linear-gradient(
                135deg,
                #8E4669,
                #B95D86
            ) !important;
    }

    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }

    @media (max-width: 900px) {

        .block-container {
            padding-top: 5.3rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        .hero-shell {
            padding: 1.45rem 1.25rem;
            border-radius: 22px;
        }

        .hero-title {
            font-size: 2.5rem;
        }

        .hero-copy {
            font-size: 0.95rem;
        }

        .step-grid {
            grid-template-columns:
                repeat(2, minmax(0, 1fr));
        }

        .metric-grid {
            grid-template-columns:
                repeat(2, minmax(0, 1fr));
        }

        .metric-box:last-child {
            grid-column: 1 / -1;
        }

        .stTabs [data-baseweb="tab-list"] {
            width: 100%;
            overflow-x: auto;
            flex-wrap: nowrap;
        }
    }

    @media (max-width: 520px) {

        .hero-title {
            font-size: 2.2rem;
        }

        .step-grid {
            grid-template-columns: 1fr;
        }

        .metric-grid {
            gap: 0.65rem;

            grid-template-columns:
                repeat(2, minmax(0, 1fr));
        }

        .metric-box {
            min-height: 104px;
        }

        .metric-value {
            font-size: 1.7rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DATA CONFIG
# =========================================================

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

REVIEW_DATE = pd.Timestamp.today().normalize()


# =========================================================
# SAMPLE DATA
# =========================================================

@st.cache_data
def build_sample_data(n=1200):

    random.seed(42)

    vendors = [
        "Nusantara Secure Systems",
        "Arunika Digital",
        "Sentra Teknologi",
        "Kirana Networks",
        "Aster Dataworks",
        "Langit Cyberindo",
        "Prima Integrasi",
        "Cakra Devices",
    ]

    categories = [
        "Network Security",
        "Cryptographic Module",
        "Secure Storage",
        "Authentication Device",
        "Communication Equipment",
        "Access Control",
    ]

    modules = [
        "Software Module",
        "Hardware Module",
        "Firmware Module",
        "Hybrid Module",
        "Embedded Module",
    ]

    algorithms = [
        "AES-256",
        "AES-128",
        "RSA-2048",
        "SHA-256",
        "ECC P-256",
        "HMAC-SHA256",
    ]

    product_prefixes = [
        "SecureGate",
        "CipherBox",
        "NetShield",
        "AuthKey",
        "DataVault",
        "LinkGuard",
    ]

    base_start = (
        datetime.now()
        - timedelta(days=1100)
    )

    review_date = datetime.now()

    rows = []
    certificate_pool = []

    for i in range(1, n + 1):

        vendor = random.choice(vendors)
        category = random.choice(categories)
        module = random.choice(modules)
        algorithm = random.choice(algorithms)

        issue_date = (
            base_start
            + timedelta(
                days=random.randint(
                    0,
                    900,
                )
            )
        )

        expiry_date = (
            issue_date
            + timedelta(
                days=random.randint(
                    420,
                    950,
                )
            )
        )

        possible_verify_days = max(
            30,
            min(
                500,
                max(
                    30,
                    (
                        review_date
                        - issue_date
                    ).days,
                ),
            ),
        )

        last_verified = (
            issue_date
            + timedelta(
                days=random.randint(
                    20,
                    possible_verify_days,
                )
            )
        )

        certificate_number = (
            f"CERT-{issue_date.year}-{i:05d}"
        )

        certificate_pool.append(
            certificate_number
        )

        cmvp_status = random.choices(
            [
                "Verified",
                "Pending",
                "Not Found",
            ],
            weights=[
                88,
                8,
                4,
            ],
        )[0]

        postel_status = random.choices(
            [
                "Verified",
                "Pending",
                "Not Found",
            ],
            weights=[
                87,
                9,
                4,
            ],
        )[0]

        certificate_status = (
            "Active"
            if expiry_date >= review_date
            else "Expired"
        )

        issue_roll = random.random()

        if issue_roll < 0.025 and i > 15:

            certificate_number = (
                random.choice(
                    certificate_pool[:-1]
                )
            )

        elif issue_roll < 0.050:

            cmvp_status = None

        elif issue_roll < 0.075:

            postel_status = None

        elif issue_roll < 0.095:

            expiry_date = (
                review_date
                - timedelta(
                    days=random.randint(
                        1,
                        180,
                    )
                )
            )

            certificate_status = "Active"

        elif issue_roll < 0.110:

            certificate_status = "Revoked"

        elif issue_roll < 0.125:

            vendor = None

        elif issue_roll < 0.140:

            algorithm = None

        product_name = (
            f"{random.choice(product_prefixes)} "
            f"{random.randint(100, 999)}"
        )

        rows.append(
            {
                "record_id":
                    f"REC-{i:05d}",

                "product_name":
                    product_name,

                "vendor":
                    vendor,

                "product_category":
                    category,

                "crypto_module":
                    module,

                "algorithm":
                    algorithm,

                "certificate_number":
                    certificate_number,

                "certificate_status":
                    certificate_status,

                "cmvp_status":
                    cmvp_status,

                "postel_status":
                    postel_status,

                "issue_date":
                    issue_date,

                "expiry_date":
                    expiry_date,

                "last_verified":
                    last_verified,
            }
        )

    return pd.DataFrame(rows)


@st.cache_data
def load_sample_data():

    possible_paths = [
        Path(
            "certification_review_sample_data.xlsx"
        ),
        Path(
            "sample_data/"
            "certification_review_sample_data.xlsx"
        ),
    ]

    for path in possible_paths:

        if path.exists():

            try:

                return pd.read_excel(
                    path,
                    sheet_name=
                    "certification_records",
                )

            except Exception:

                pass

    return build_sample_data()


# =========================================================
# FILE INPUT
# =========================================================

def read_uploaded_file(uploaded_file):

    file_name = (
        uploaded_file.name.lower()
    )

    if file_name.endswith(".csv"):

        return pd.read_csv(
            uploaded_file
        )

    if (
        file_name.endswith(".xlsx")
        or
        file_name.endswith(".xls")
    ):

        return pd.read_excel(
            uploaded_file
        )

    raise ValueError(
        "Please upload a CSV or Excel file."
    )


# =========================================================
# VALIDATION LOGIC
# =========================================================

def prepare_dates(df):

    result = df.copy()

    for column in [
        "issue_date",
        "expiry_date",
        "last_verified",
    ]:

        if column in result.columns:

            result[column] = pd.to_datetime(
                result[column],
                errors="coerce",
            )

    return result


def validate_records(df):

    checked = prepare_dates(df)

    duplicate_mask = (
        checked[
            "certificate_number"
        ]
        .astype("string")
        .duplicated(
            keep=False
        )
        &
        checked[
            "certificate_number"
        ].notna()
    )

    issue_texts = []
    review_statuses = []
    priorities = []

    required_fields = [
        "vendor",
        "algorithm",
        "certificate_number",
        "cmvp_status",
        "postel_status",
    ]

    priority_rank = {
        "Low": 0,
        "Medium": 1,
        "High": 2,
        "Critical": 3,
    }

    for index, row in checked.iterrows():

        issues = []
        priority = "Low"

        def raise_priority(
            new_priority
        ):

            nonlocal priority

            if (
                priority_rank[
                    new_priority
                ]
                >
                priority_rank[
                    priority
                ]
            ):

                priority = new_priority

        missing_fields = []

        for field in required_fields:

            value = row.get(field)

            if (
                pd.isna(value)
                or
                str(value).strip() == ""
            ):

                missing_fields.append(
                    field
                )

        if missing_fields:

            issues.append(
                "Missing "
                + ", ".join(
                    missing_fields
                )
            )

            raise_priority(
                "High"
            )

        if duplicate_mask.loc[index]:

            issues.append(
                "Duplicate certificate number"
            )

            raise_priority(
                "High"
            )

        expiry = row.get(
            "expiry_date"
        )

        certificate_status = str(
            row.get(
                "certificate_status",
                "",
            )
        ).strip()

        if pd.notna(expiry):

            if expiry < REVIEW_DATE:

                issues.append(
                    "Certificate expired"
                )

                raise_priority(
                    "Critical"
                )

            elif (
                expiry
                <=
                REVIEW_DATE
                + pd.Timedelta(
                    days=30
                )
            ):

                issues.append(
                    "Certificate expires within 30 days"
                )

                raise_priority(
                    "Medium"
                )

        if (
            pd.notna(expiry)
            and
            expiry < REVIEW_DATE
            and
            certificate_status.lower()
            == "active"
        ):

            issues.append(
                "Status does not match expiry date"
            )

            raise_priority(
                "Critical"
            )

        cmvp_status = str(
            row.get(
                "cmvp_status",
                "",
            )
        ).strip()

        postel_status = str(
            row.get(
                "postel_status",
                "",
            )
        ).strip()

        if (
            cmvp_status.lower()
            in {
                "pending",
                "not found",
            }
        ):

            issues.append(
                f"CMVP {cmvp_status}"
            )

            raise_priority(
                "High"
            )

        if (
            postel_status.lower()
            in {
                "pending",
                "not found",
            }
        ):

            issues.append(
                f"Postel {postel_status}"
            )

            raise_priority(
                "High"
            )

        if (
            certificate_status.lower()
            == "revoked"
        ):

            issues.append(
                "Certificate revoked"
            )

            raise_priority(
                "Critical"
            )

        if issues:

            issue_texts.append(
                "; ".join(
                    dict.fromkeys(
                        issues
                    )
                )
            )

            review_statuses.append(
                "Need Review"
            )

        else:

            issue_texts.append(
                "No issue found"
            )

            review_statuses.append(
                "Clear"
            )

        priorities.append(
            priority
        )

    checked[
        "review_status"
    ] = review_statuses

    checked[
        "priority"
    ] = priorities

    checked[
        "issue_found"
    ] = issue_texts

    return checked


# =========================================================
# HERO
# =========================================================

html(
    """
    <div class="hero-shell">

        <div class="hero-kicker">
            🌷 Portfolio Project
        </div>

        <div class="hero-title">
            Certification Review Tracker
        </div>

        <div class="hero-copy">
            A practical tool for checking certification records,
            finding data that needs attention,
            and keeping review work easier to follow.
        </div>

        <div class="hero-tags">

            <span class="hero-tag">
                Data validation
            </span>

            <span class="hero-tag">
                Compliance review
            </span>

            <span class="hero-tag">
                Administrative workflow
            </span>

            <span class="hero-tag">
                Python + Streamlit
            </span>

        </div>

    </div>
    """
)


html(
    """
    <div class="soft-note">
        This portfolio demo uses synthetic records.
        It does not contain internal or confidential BSSN data.
    </div>
    """
)


# =========================================================
# WORKFLOW
# =========================================================

html(
    """
    <div class="section-label">
        Workflow
    </div>

    <div class="section-title">
        From raw records to a review queue
    </div>

    <div class="section-copy">
        The app checks common data issues first,
        then groups the records that may need another look.
    </div>

    <div class="step-grid">

        <div class="step-card">
            <div class="step-num">
                01
            </div>

            <div class="step-name">
                Load records
            </div>

            <div class="step-desc">
                Use the built in sample
                or upload your own file.
            </div>
        </div>

        <div class="step-card">
            <div class="step-num">
                02
            </div>

            <div class="step-name">
                Check data
            </div>

            <div class="step-desc">
                Check missing,
                duplicate,
                and inconsistent values.
            </div>
        </div>

        <div class="step-card">
            <div class="step-num">
                03
            </div>

            <div class="step-name">
                Review issues
            </div>

            <div class="step-desc">
                Focus on the records
                that may need another look.
            </div>
        </div>

        <div class="step-card">
            <div class="step-num">
                04
            </div>

            <div class="step-name">
                Export results
            </div>

            <div class="step-desc">
                Download the checked
                records as CSV.
            </div>
        </div>

    </div>
    """
)


# =========================================================
# INPUT SECTION
# =========================================================

html(
    """
    <div class="section-label">
        Input
    </div>

    <div class="section-title">
        Choose your data
    </div>

    <div class="section-copy">
        The sample data is ready to use,
        so visitors can try the app
        without uploading anything.
    </div>
    """
)


source = st.radio(
    "Data source",
    [
        "Use sample data",
        "Upload a file",
    ],
    horizontal=True,
    label_visibility="collapsed",
)


data = None


if source == "Use sample data":

    data = load_sample_data()

    st.success(
        f"Sample data ready. "
        f"{len(data):,} records loaded."
    )


else:

    uploaded_file = (
        st.file_uploader(
            "Upload CSV or Excel",
            type=[
                "csv",
                "xlsx",
                "xls",
            ],
        )
    )

    if uploaded_file is not None:

        try:

            data = read_uploaded_file(
                uploaded_file
            )

            st.success(
                f"{uploaded_file.name} loaded."
            )

        except Exception as error:

            st.error(
                str(error)
            )


if data is None:

    st.info(
        "Choose the sample data "
        "or upload a file to continue."
    )

    st.stop()


# =========================================================
# COLUMN CHECK
# =========================================================

missing_columns = [
    column
    for column in REQUIRED_COLUMNS
    if column not in data.columns
]


if missing_columns:

    st.error(
        "These columns are missing: "
        + ", ".join(
            missing_columns
        )
    )

    st.stop()


# =========================================================
# PREVIEW
# =========================================================

preview_left, preview_right = st.columns(
    [1.3, 1]
)


with preview_left:

    st.markdown(
        "### Quick preview"
    )

    st.dataframe(
        data.head(8),
        use_container_width=True,
        hide_index=True,
        height=310,
    )


with preview_right:

    st.markdown(
        "### What will be checked"
    )

    html(
        """
        <div class="status-row">

            <span class="status-pill">
                Missing fields
            </span>

            <span class="status-pill">
                Duplicate certificate
            </span>

            <span class="status-pill">
                Expired records
            </span>

            <span class="status-pill">
                Status mismatch
            </span>

            <span class="status-pill">
                CMVP status
            </span>

            <span class="status-pill">
                Postel status
            </span>

            <span class="status-pill">
                Revoked certificate
            </span>

        </div>
        """
    )

    st.caption(
        "The result is only a portfolio simulation "
        "and is not an official compliance decision."
    )


# =========================================================
# RUN CHECK
# =========================================================

st.markdown("")


if st.button(
    "Check records",
    use_container_width=True,
):

    st.session_state[
        "checked_data"
    ] = validate_records(
        data
    )


if (
    "checked_data"
    not in st.session_state
):

    st.stop()


result = (
    st.session_state[
        "checked_data"
    ]
    .copy()
)


# =========================================================
# METRICS
# =========================================================

total_records = len(result)

clear_records = int(
    (
        result[
            "review_status"
        ]
        == "Clear"
    ).sum()
)

need_review = int(
    (
        result[
            "review_status"
        ]
        == "Need Review"
    ).sum()
)

critical_records = int(
    (
        result[
            "priority"
        ]
        == "Critical"
    ).sum()
)

high_records = int(
    (
        result[
            "priority"
        ]
        == "High"
    ).sum()
)

clear_rate = percent(
    clear_records,
    total_records,
)


html(
    """
    <div class="section-label">
        Output
    </div>

    <div class="section-title">
        Review summary
    </div>

    <div class="section-copy">
        A quick look at what passed the checks
        and what still needs attention.
    </div>
    """
)


metric_html = (
    '<div class="metric-grid">'
    +
    metric_card(
        "Records checked",
        f"{total_records:,}",
        "All loaded records",
    )
    +
    metric_card(
        "Clear",
        f"{clear_records:,}",
        "No issue detected",
    )
    +
    metric_card(
        "Need review",
        f"{need_review:,}",
        "At least one issue",
    )
    +
    metric_card(
        "Clear rate",
        f"{clear_rate:.1f}%",
        "Share of clear records",
    )
    +
    metric_card(
        "Critical",
        f"{critical_records:,}",
        "Highest review priority",
    )
    +
    "</div>"
)


html(metric_html)


# =========================================================
# TABS
# =========================================================

tab_overview, tab_queue, tab_all = st.tabs(
    [
        "Overview",
        "Review queue",
        "All records",
    ]
)


# =========================================================
# OVERVIEW TAB
# =========================================================

with tab_overview:

    left, right = st.columns(
        [1, 1]
    )

    with left:

        st.markdown(
            "### Priority mix"
        )

        priority_order = [
            "Critical",
            "High",
            "Medium",
            "Low",
        ]

        priority_counts = (
            result[
                "priority"
            ]
            .value_counts()
            .reindex(
                priority_order,
                fill_value=0,
            )
        )

        maximum = int(
            priority_counts.max()
        )

        for label, value in (
            priority_counts.items()
        ):

            html(
                issue_bar(
                    label,
                    int(value),
                    maximum,
                )
            )

    with right:

        st.markdown(
            "### Common review notes"
        )

        issue_series = (
            result.loc[
                result[
                    "review_status"
                ]
                == "Need Review",
                "issue_found",
            ]
            .value_counts()
            .head(6)
        )

        if issue_series.empty:

            st.success(
                "No review notes found."
            )

        else:

            maximum_issue = int(
                issue_series.max()
            )

            for label, value in (
                issue_series.items()
            ):

                html(
                    issue_bar(
                        label,
                        int(value),
                        maximum_issue,
                    )
                )

    st.caption(
        f"{high_records:,} records "
        "are currently marked High priority."
    )


# =========================================================
# REVIEW QUEUE TAB
# =========================================================

with tab_queue:

    st.markdown(
        "### Records that need attention"
    )

    review_data = (
        result[
            result[
                "review_status"
            ]
            == "Need Review"
        ]
        .copy()
    )


    filter_a, filter_b, filter_c = (
        st.columns(3)
    )


    with filter_a:

        priority_filter = (
            st.multiselect(
                "Priority",
                [
                    "Critical",
                    "High",
                    "Medium",
                    "Low",
                ],
                default=[
                    "Critical",
                    "High",
                    "Medium",
                ],
            )
        )


    with filter_b:

        category_options = sorted(
            review_data[
                "product_category"
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        category_filter = (
            st.multiselect(
                "Product category",
                category_options,
            )
        )


    with filter_c:

        vendor_options = sorted(
            review_data[
                "vendor"
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        vendor_filter = (
            st.multiselect(
                "Vendor",
                vendor_options,
            )
        )


    filtered = (
        review_data.copy()
    )


    if priority_filter:

        filtered = filtered[
            filtered[
                "priority"
            ]
            .isin(
                priority_filter
            )
        ]


    if category_filter:

        filtered = filtered[
            filtered[
                "product_category"
            ]
            .astype(str)
            .isin(
                category_filter
            )
        ]


    if vendor_filter:

        filtered = filtered[
            filtered[
                "vendor"
            ]
            .astype(str)
            .isin(
                vendor_filter
            )
        ]


    queue_columns = [
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
        filtered[
            queue_columns
        ],
        use_container_width=True,
        hide_index=True,
        height=500,
    )


    st.caption(
        f"{len(filtered):,} records shown."
    )


# =========================================================
# ALL RECORDS TAB
# =========================================================

with tab_all:

    st.markdown(
        "### Checked records"
    )


    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True,
        height=520,
    )


    csv_data = (
        to_csv_bytes(
            result
        )
    )


    st.download_button(
        "Download checked data",
        data=csv_data,
        file_name=
        "certification_review_results.csv",
        mime="text/csv",
        use_container_width=True,
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("")

st.caption(
    "Built as a portfolio project "
    "using synthetic certification data."
)
