import random
from datetime import datetime, timedelta

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
# GLOBAL STYLE
# =========================================================

st.html(
    """
    <style>
        :root {
            --ink: #3d2c35;
            --muted: #816d77;
            --plum: #824361;
            --berry: #aa587b;
            --rose: #e99db5;
            --peach: #f8ccb8;
            --lavender: #dfd2f3;
            --cream: #fff9f6;
            --line: #eadde3;
        }

        .stApp {
            background:
                radial-gradient(
                    circle at 7% 5%,
                    rgba(248, 204, 184, 0.42),
                    transparent 24%
                ),
                radial-gradient(
                    circle at 92% 8%,
                    rgba(223, 210, 243, 0.50),
                    transparent 25%
                ),
                radial-gradient(
                    circle at 82% 80%,
                    rgba(233, 157, 181, 0.20),
                    transparent 22%
                ),
                linear-gradient(
                    180deg,
                    #fffdfc 0%,
                    #fff7f9 48%,
                    #fff9f6 100%
                );
        }

        .block-container {
            max-width: 1240px;
            padding-top: 5.2rem;
            padding-bottom: 4rem;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        h1,
        h2,
        h3,
        p,
        label {
            color: var(--ink);
        }

        div.stButton > button,
        div.stDownloadButton > button {
            min-height: 46px;
            border: none;
            border-radius: 14px;
            color: white;
            font-weight: 700;
            background:
                linear-gradient(
                    135deg,
                    #8b4566,
                    #be6287
                );
            box-shadow:
                0 8px 20px rgba(139, 69, 102, 0.20);
        }

        div.stButton > button:hover,
        div.stDownloadButton > button:hover {
            color: white;
            border: none;
            background:
                linear-gradient(
                    135deg,
                    #783951,
                    #aa5277
                );
        }

        div[data-testid="stDataFrame"] {
            border-radius: 18px;
            border: 1px solid var(--line);
            overflow: hidden;
            background: white;
            box-shadow:
                0 8px 22px rgba(105, 63, 82, 0.06);
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.4rem;
            padding: 0.35rem;
            border: 1px solid var(--line);
            border-radius: 15px;
            background: rgba(255, 255, 255, 0.68);
        }

        .stTabs [data-baseweb="tab"] {
            height: 42px;
            border-radius: 11px;
            padding-left: 1rem;
            padding-right: 1rem;
            color: #735462;
            font-weight: 650;
        }

        .stTabs [aria-selected="true"] {
            color: white !important;
            background:
                linear-gradient(
                    135deg,
                    #8b4566,
                    #bd6287
                ) !important;
        }

        .stTabs [data-baseweb="tab-highlight"] {
            display: none;
        }

        @media (max-width: 800px) {
            .block-container {
                padding-top: 5rem !important;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }

            .stTabs [data-baseweb="tab-list"] {
                overflow-x: auto;
                flex-wrap: nowrap;
            }
        }
    </style>
    """
)


# =========================================================
# UI COMPONENTS
# =========================================================

def render_hero():
    st.html(
        """
        <div style="
            position: relative;
            overflow: hidden;
            padding: 32px;
            border-radius: 28px;
            border: 1px solid rgba(130, 67, 97, 0.13);
            background:
                linear-gradient(
                    135deg,
                    rgba(255,255,255,0.97),
                    rgba(255,239,244,0.92)
                );
            box-shadow:
                0 18px 42px rgba(110, 62, 84, 0.10);
            margin-bottom: 14px;
        ">

            <div style="
                position: absolute;
                width: 240px;
                height: 240px;
                border-radius: 50%;
                right: -75px;
                top: -80px;
                background:
                    linear-gradient(
                        135deg,
                        rgba(235,157,181,0.42),
                        rgba(216,196,241,0.48)
                    );
            "></div>

            <div style="
                position: relative;
                z-index: 2;
                display: inline-block;
                padding: 7px 12px;
                border-radius: 999px;
                background: rgba(130,67,97,0.09);
                color: #824361;
                font-size: 12px;
                font-weight: 800;
                margin-bottom: 16px;
            ">
                🌷 PORTFOLIO PROJECT
            </div>

            <div style="
                position: relative;
                z-index: 2;
                max-width: 800px;
                color: #3d2c35;
                font-size: clamp(38px, 6vw, 64px);
                line-height: 1.02;
                font-weight: 800;
                letter-spacing: -2px;
            ">
                Certification Review Tracker
            </div>

            <div style="
                position: relative;
                z-index: 2;
                max-width: 760px;
                margin-top: 17px;
                color: #816d77;
                font-size: 16px;
                line-height: 1.7;
            ">
                A practical tool for checking certification records,
                finding data that needs attention,
                and organizing records for further review.
            </div>

            <div style="
                position: relative;
                z-index: 2;
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-top: 18px;
            ">

                <span style="
                    padding: 7px 11px;
                    border-radius: 999px;
                    background: white;
                    border: 1px solid #eadde3;
                    color: #674d59;
                    font-size: 13px;
                    font-weight: 650;
                ">
                    Data validation
                </span>

                <span style="
                    padding: 7px 11px;
                    border-radius: 999px;
                    background: white;
                    border: 1px solid #eadde3;
                    color: #674d59;
                    font-size: 13px;
                    font-weight: 650;
                ">
                    Compliance review
                </span>

                <span style="
                    padding: 7px 11px;
                    border-radius: 999px;
                    background: white;
                    border: 1px solid #eadde3;
                    color: #674d59;
                    font-size: 13px;
                    font-weight: 650;
                ">
                    Administrative workflow
                </span>

                <span style="
                    padding: 7px 11px;
                    border-radius: 999px;
                    background: white;
                    border: 1px solid #eadde3;
                    color: #674d59;
                    font-size: 13px;
                    font-weight: 650;
                ">
                    Python + Streamlit
                </span>

            </div>
        </div>
        """
    )


def render_section(kicker, title, description):
    st.html(
        f"""
        <div style="
            margin-top: 25px;
            margin-bottom: 13px;
        ">

            <div style="
                color: #aa587b;
                font-size: 12px;
                font-weight: 800;
                letter-spacing: 1.4px;
                margin-bottom: 7px;
            ">
                {kicker.upper()}
            </div>

            <div style="
                color: #3d2c35;
                font-size: 31px;
                line-height: 1.15;
                font-weight: 800;
                letter-spacing: -0.8px;
            ">
                {title}
            </div>

            <div style="
                margin-top: 8px;
                color: #816d77;
                font-size: 15px;
                line-height: 1.65;
                max-width: 850px;
            ">
                {description}
            </div>

        </div>
        """
    )


def render_workflow():
    st.html(
        """
        <div style="
            display: grid;
            grid-template-columns:
                repeat(auto-fit, minmax(210px, 1fr));
            gap: 12px;
            margin: 16px 0 24px 0;
        ">

            <div style="
                padding: 18px;
                border-radius: 20px;
                background: rgba(255,255,255,0.88);
                border: 1px solid #eadde3;
                box-shadow: 0 8px 22px rgba(104,64,82,0.06);
            ">
                <div style="
                    color: #b45d82;
                    font-size: 12px;
                    font-weight: 800;
                ">
                    01
                </div>

                <div style="
                    margin-top: 7px;
                    color: #3d2c35;
                    font-size: 16px;
                    font-weight: 750;
                ">
                    Load records
                </div>

                <div style="
                    margin-top: 5px;
                    color: #816d77;
                    font-size: 13px;
                    line-height: 1.5;
                ">
                    Use the sample data or upload another file.
                </div>
            </div>

            <div style="
                padding: 18px;
                border-radius: 20px;
                background: rgba(255,255,255,0.88);
                border: 1px solid #eadde3;
                box-shadow: 0 8px 22px rgba(104,64,82,0.06);
            ">
                <div style="
                    color: #b45d82;
                    font-size: 12px;
                    font-weight: 800;
                ">
                    02
                </div>

                <div style="
                    margin-top: 7px;
                    color: #3d2c35;
                    font-size: 16px;
                    font-weight: 750;
                ">
                    Check data
                </div>

                <div style="
                    margin-top: 5px;
                    color: #816d77;
                    font-size: 13px;
                    line-height: 1.5;
                ">
                    Find missing, duplicate, and inconsistent values.
                </div>
            </div>

            <div style="
                padding: 18px;
                border-radius: 20px;
                background: rgba(255,255,255,0.88);
                border: 1px solid #eadde3;
                box-shadow: 0 8px 22px rgba(104,64,82,0.06);
            ">
                <div style="
                    color: #b45d82;
                    font-size: 12px;
                    font-weight: 800;
                ">
                    03
                </div>

                <div style="
                    margin-top: 7px;
                    color: #3d2c35;
                    font-size: 16px;
                    font-weight: 750;
                ">
                    Review issues
                </div>

                <div style="
                    margin-top: 5px;
                    color: #816d77;
                    font-size: 13px;
                    line-height: 1.5;
                ">
                    Focus on records that may need another review.
                </div>
            </div>

            <div style="
                padding: 18px;
                border-radius: 20px;
                background: rgba(255,255,255,0.88);
                border: 1px solid #eadde3;
                box-shadow: 0 8px 22px rgba(104,64,82,0.06);
            ">
                <div style="
                    color: #b45d82;
                    font-size: 12px;
                    font-weight: 800;
                ">
                    04
                </div>

                <div style="
                    margin-top: 7px;
                    color: #3d2c35;
                    font-size: 16px;
                    font-weight: 750;
                ">
                    Export results
                </div>

                <div style="
                    margin-top: 5px;
                    color: #816d77;
                    font-size: 13px;
                    line-height: 1.5;
                ">
                    Download the checked records as a CSV file.
                </div>
            </div>

        </div>
        """
    )


def render_check_pills():
    st.html(
        """
        <div style="
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 10px 0 12px 0;
        ">

            <span style="
                padding: 7px 10px;
                border-radius: 999px;
                background: #fff0f5;
                border: 1px solid #f1d7df;
                color: #795462;
                font-size: 12px;
                font-weight: 700;
            ">
                Missing fields
            </span>

            <span style="
                padding: 7px 10px;
                border-radius: 999px;
                background: #fff6ef;
                border: 1px solid #f1dfd2;
                color: #795462;
                font-size: 12px;
                font-weight: 700;
            ">
                Duplicate certificate
            </span>

            <span style="
                padding: 7px 10px;
                border-radius: 999px;
                background: #f4effc;
                border: 1px solid #e3d8f4;
                color: #795462;
                font-size: 12px;
                font-weight: 700;
            ">
                Expired record
            </span>

            <span style="
                padding: 7px 10px;
                border-radius: 999px;
                background: #fff0f5;
                border: 1px solid #f1d7df;
                color: #795462;
                font-size: 12px;
                font-weight: 700;
            ">
                Status mismatch
            </span>

            <span style="
                padding: 7px 10px;
                border-radius: 999px;
                background: #fff6ef;
                border: 1px solid #f1dfd2;
                color: #795462;
                font-size: 12px;
                font-weight: 700;
            ">
                CMVP status
            </span>

            <span style="
                padding: 7px 10px;
                border-radius: 999px;
                background: #f4effc;
                border: 1px solid #e3d8f4;
                color: #795462;
                font-size: 12px;
                font-weight: 700;
            ">
                Postel status
            </span>

            <span style="
                padding: 7px 10px;
                border-radius: 999px;
                background: #fff0f5;
                border: 1px solid #f1d7df;
                color: #795462;
                font-size: 12px;
                font-weight: 700;
            ">
                Revoked certificate
            </span>

        </div>
        """
    )


def make_metric_card(label, value, caption, accent):
    return f"""
        <div style="
            position: relative;
            overflow: hidden;
            min-height: 118px;
            padding: 18px;
            border-radius: 21px;
            background: rgba(255,255,255,0.91);
            border: 1px solid #eadde3;
            box-shadow: 0 9px 22px rgba(104,64,82,0.065);
        ">

            <div style="
                position: absolute;
                width: 64px;
                height: 64px;
                border-radius: 50%;
                right: -18px;
                top: -18px;
                background: {accent};
                opacity: 0.55;
            "></div>

            <div style="
                position: relative;
                z-index: 2;
                color: #8b7580;
                font-size: 12px;
                font-weight: 650;
            ">
                {label}
            </div>

            <div style="
                position: relative;
                z-index: 2;
                margin-top: 8px;
                color: #7b4061;
                font-size: 31px;
                line-height: 1;
                font-weight: 800;
            ">
                {value}
            </div>

            <div style="
                position: relative;
                z-index: 2;
                margin-top: 9px;
                color: #9a8590;
                font-size: 11px;
            ">
                {caption}
            </div>

        </div>
    """


def render_insight_bar(label, value, maximum):
    width = 0 if maximum == 0 else value / maximum * 100

    st.html(
        f"""
        <div style="
            padding: 16px;
            border-radius: 18px;
            border: 1px solid #eadde3;
            background: rgba(255,255,255,0.88);
            margin-bottom: 9px;
            box-shadow: 0 7px 18px rgba(104,64,82,0.045);
        ">

            <div style="
                display: flex;
                justify-content: space-between;
                gap: 10px;
                margin-bottom: 8px;
            ">

                <div style="
                    color: #49363f;
                    font-size: 13px;
                    font-weight: 700;
                ">
                    {label}
                </div>

                <div style="
                    color: #934c70;
                    font-size: 13px;
                    font-weight: 800;
                ">
                    {value:,}
                </div>

            </div>

            <div style="
                height: 9px;
                border-radius: 999px;
                background: #f0e6eb;
                overflow: hidden;
            ">

                <div style="
                    width: {width:.1f}%;
                    height: 100%;
                    border-radius: 999px;
                    background:
                        linear-gradient(
                            90deg,
                            #ad587d,
                            #e58eab,
                            #ccb3ec
                        );
                "></div>

            </div>

        </div>
        """
    )


# =========================================================
# SAMPLE DATA
# =========================================================

@st.cache_data
def build_sample_data(total_rows=1200):

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

    today = datetime.now()
    start_date = today - timedelta(days=1000)

    rows = []
    certificate_pool = []

    for i in range(1, total_rows + 1):

        vendor = random.choice(vendors)
        category = random.choice(categories)
        module = random.choice(modules)
        algorithm = random.choice(algorithms)

        issue_date = (
            start_date
            + timedelta(
                days=random.randint(0, 820)
            )
        )

        expiry_date = (
            issue_date
            + timedelta(
                days=random.randint(550, 1050)
            )
        )

        max_verify_days = max(
            30,
            min(
                430,
                max(
                    30,
                    (today - issue_date).days,
                ),
            ),
        )

        last_verified = (
            issue_date
            + timedelta(
                days=random.randint(
                    20,
                    max_verify_days,
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
                91,
                6,
                3,
            ],
        )[0]

        postel_status = random.choices(
            [
                "Verified",
                "Pending",
                "Not Found",
            ],
            weights=[
                90,
                7,
                3,
            ],
        )[0]

        certificate_status = (
            "Active"
            if expiry_date >= today
            else "Expired"
        )

        problem = random.random()

        if problem < 0.020 and i > 20:

            certificate_number = random.choice(
                certificate_pool[:-1]
            )

        elif problem < 0.040:

            vendor = None

        elif problem < 0.060:

            algorithm = None

        elif problem < 0.080:

            cmvp_status = None

        elif problem < 0.100:

            postel_status = None

        elif problem < 0.120:

            expiry_date = (
                today
                - timedelta(
                    days=random.randint(
                        1,
                        150,
                    )
                )
            )

            certificate_status = "Active"

        elif problem < 0.135:

            certificate_status = "Revoked"

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


# =========================================================
# FILE INPUT
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


def read_uploaded_file(uploaded_file):

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".csv"):

        return pd.read_csv(
            uploaded_file
        )

    if (
        file_name.endswith(".xlsx")
        or file_name.endswith(".xls")
    ):

        return pd.read_excel(
            uploaded_file
        )

    raise ValueError(
        "Please upload a CSV or Excel file."
    )


# =========================================================
# VALIDATION ENGINE
# =========================================================

def validate_records(df):

    checked = df.copy()

    for column in [
        "issue_date",
        "expiry_date",
        "last_verified",
    ]:

        checked[column] = pd.to_datetime(
            checked[column],
            errors="coerce",
        )

    review_date = (
        pd.Timestamp.today().normalize()
    )

    duplicate_mask = (
        checked["certificate_number"]
        .astype("string")
        .duplicated(keep=False)
        &
        checked[
            "certificate_number"
        ].notna()
    )

    issue_results = []
    status_results = []
    priority_results = []

    priority_rank = {
        "Low": 0,
        "Medium": 1,
        "High": 2,
        "Critical": 3,
    }

    required_fields = [
        "vendor",
        "algorithm",
        "certificate_number",
        "cmvp_status",
        "postel_status",
    ]

    for index, row in checked.iterrows():

        issues = []
        current_priority = "Low"

        def upgrade(target):
            nonlocal current_priority

            if (
                priority_rank[target]
                >
                priority_rank[
                    current_priority
                ]
            ):
                current_priority = target

        missing_fields = []

        for field in required_fields:

            value = row.get(field)

            if (
                pd.isna(value)
                or str(value).strip() == ""
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

            upgrade("High")

        if duplicate_mask.loc[index]:

            issues.append(
                "Duplicate certificate number"
            )

            upgrade("High")

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

            if expiry < review_date:

                issues.append(
                    "Certificate expired"
                )

                upgrade("Critical")

            elif (
                expiry
                <=
                review_date
                + pd.Timedelta(days=30)
            ):

                issues.append(
                    "Certificate expires within 30 days"
                )

                upgrade("Medium")

        if (
            pd.notna(expiry)
            and expiry < review_date
            and certificate_status.lower()
            == "active"
        ):

            issues.append(
                "Status does not match expiry date"
            )

            upgrade("Critical")

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

            upgrade("High")

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

            upgrade("High")

        if (
            certificate_status.lower()
            == "revoked"
        ):

            issues.append(
                "Certificate revoked"
            )

            upgrade("Critical")

        if issues:

            issue_results.append(
                "; ".join(
                    dict.fromkeys(
                        issues
                    )
                )
            )

            status_results.append(
                "Need Review"
            )

        else:

            issue_results.append(
                "No issue found"
            )

            status_results.append(
                "Clear"
            )

        priority_results.append(
            current_priority
        )

    checked[
        "review_status"
    ] = status_results

    checked[
        "priority"
    ] = priority_results

    checked[
        "issue_found"
    ] = issue_results

    return checked


# =========================================================
# HERO
# =========================================================

render_hero()

st.caption(
    "This portfolio demo uses synthetic records. "
    "It does not contain internal or confidential BSSN data."
)


# =========================================================
# WORKFLOW
# =========================================================

render_section(
    "Workflow",
    "From raw records to a review queue",
    (
        "The app checks common data issues first, "
        "then organizes records that may need another look."
    ),
)

render_workflow()


# =========================================================
# INPUT
# =========================================================

render_section(
    "Input",
    "Choose your data",
    (
        "Use the built in sample data or upload another dataset "
        "with the same column structure."
    ),
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

    data = build_sample_data()

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
        "Missing required columns: "
        + ", ".join(
            missing_columns
        )
    )

    st.stop()


# =========================================================
# PREVIEW
# =========================================================

preview_left, preview_right = (
    st.columns(
        [1.35, 1]
    )
)


with preview_left:

    st.subheader(
        "Quick preview"
    )

    st.dataframe(
        data.head(7),
        use_container_width=True,
        hide_index=True,
        height=300,
    )


with preview_right:

    st.subheader(
        "What will be checked"
    )

    render_check_pills()

    st.caption(
        "The result is a portfolio simulation "
        "and is not an official compliance decision."
    )


st.write("")


# =========================================================
# CHECK BUTTON
# =========================================================

if st.button(
    "Check records",
    use_container_width=True,
):

    st.session_state[
        "checked_results"
    ] = validate_records(
        data
    )


if (
    "checked_results"
    not in st.session_state
):

    st.stop()


result = (
    st.session_state[
        "checked_results"
    ].copy()
)


# =========================================================
# SUMMARY METRICS
# =========================================================

total_records = len(
    result
)

clear_records = int(
    (
        result[
            "review_status"
        ]
        == "Clear"
    ).sum()
)

review_records = int(
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

if total_records > 0:

    clear_rate = (
        clear_records
        / total_records
        * 100
    )

else:

    clear_rate = 0


render_section(
    "Output",
    "Review summary",
    (
        "A quick look at what passed the checks "
        "and what still needs attention."
    ),
)


metric_cards = (
    """
    <div style="
        display: grid;
        grid-template-columns:
            repeat(auto-fit, minmax(170px, 1fr));
        gap: 11px;
        margin: 16px 0 22px 0;
    ">
    """
    +
    make_metric_card(
        "Records checked",
        f"{total_records:,}",
        "All loaded records",
        "#f6c5d6",
    )
    +
    make_metric_card(
        "Clear",
        f"{clear_records:,}",
        "No issue detected",
        "#dad2f3",
    )
    +
    make_metric_card(
        "Need review",
        f"{review_records:,}",
        "At least one issue",
        "#f7cab6",
    )
    +
    make_metric_card(
        "Clear rate",
        f"{clear_rate:.1f}%",
        "Share of clear records",
        "#f3bfd0",
    )
    +
    make_metric_card(
        "Critical",
        f"{critical_records:,}",
        "Highest review priority",
        "#dabfea",
    )
    +
    "</div>"
)

st.html(
    metric_cards
)


# =========================================================
# RESULT TABS
# =========================================================

overview_tab, queue_tab, all_tab = (
    st.tabs(
        [
            "Overview",
            "Review queue",
            "All records",
        ]
    )
)


# =========================================================
# OVERVIEW
# =========================================================

with overview_tab:

    overview_left, overview_right = (
        st.columns(2)
    )


    with overview_left:

        st.subheader(
            "Priority mix"
        )

        priority_counts = (
            result[
                "priority"
            ]
            .value_counts()
            .reindex(
                [
                    "Critical",
                    "High",
                    "Medium",
                    "Low",
                ],
                fill_value=0,
            )
        )

        maximum_priority = int(
            priority_counts.max()
        )

        for label, value in (
            priority_counts.items()
        ):

            render_insight_bar(
                label,
                int(value),
                maximum_priority,
            )


    with overview_right:

        st.subheader(
            "Common review notes"
        )

        issue_counts = (
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

        if issue_counts.empty:

            st.success(
                "No review notes found."
            )

        else:

            maximum_issue = int(
                issue_counts.max()
            )

            for label, value in (
                issue_counts.items()
            ):

                render_insight_bar(
                    label,
                    int(value),
                    maximum_issue,
                )


    st.caption(
        f"{high_records:,} records are currently "
        "marked High priority."
    )


# =========================================================
# REVIEW QUEUE
# =========================================================

with queue_tab:

    st.subheader(
        "Records that need attention"
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


    filter_one, filter_two, filter_three = (
        st.columns(3)
    )


    with filter_one:

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


    with filter_two:

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


    with filter_three:

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
        height=520,
    )


    st.caption(
        f"{len(filtered):,} records shown."
    )


# =========================================================
# ALL RECORDS
# =========================================================

with all_tab:

    st.subheader(
        "Checked records"
    )

    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True,
        height=540,
    )


    csv_data = (
        result
        .to_csv(
            index=False
        )
        .encode(
            "utf-8-sig"
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

st.write("")

st.caption(
    "Portfolio project using synthetic certification data."
)
