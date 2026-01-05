import streamlit as st
import base64
from pathlib import Path


def set_video_background(video_filename: str, overlay_opacity: float = 0.60):
    """
    Full screen video background + dark overlay.
    Put videos in: frontend/assets/
    """

    video_path = Path(__file__).parent / "assets" / video_filename

    if not video_path.exists():
        st.error(f"❌ Video not found at: {video_path}")
        return

    video_bytes = video_path.read_bytes()
    video_b64 = base64.b64encode(video_bytes).decode()

    st.markdown(
        f"""
        <style>
        html, body, [data-testid="stAppViewContainer"], .stApp {{
            background: transparent !important;
        }}

        .video-bg {{
            position: fixed;
            top: 0; left: 0;
            width: 100vw; height: 100vh;
            z-index: -100;
            overflow: hidden;
        }}

        .video-bg video {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        .video-overlay {{
            position: fixed;
            top: 0; left: 0;
            width: 100vw; height: 100vh;
            z-index: -90;
            background: rgba(0, 0, 0, {overlay_opacity});
        }}

        section[data-testid="stSidebar"] > div {{
            background: rgba(10,10,10,0.78) !important;
        }}
        section[data-testid="stSidebar"] * {{
            color: #fff !important;
        }}

        .card {{
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.18);
            border-radius: 18px;
            padding: 18px;
            margin-bottom: 18px;
            backdrop-filter: blur(10px);
        }}

        h1,h2,h3,h4,h5,h6,p,span,label,div {{
            color: rgba(255,255,255,0.92);
        }}

        div[data-testid="stMetricValue"] {{
            color: #ffffff !important;
            font-weight: 700 !important;
        }}
        div[data-testid="stMetricLabel"] {{
            color: rgba(255,255,255,0.80) !important;
        }}

        .hallmark {{
            position: fixed;
            bottom: 14px;
            left: 18px;
            z-index: 9999;
            font-size: 13px;
            color: rgba(255,255,255,0.75);
            font-style: italic;
            user-select: none;
        }}

        div[role="radiogroup"] {{
            display: flex;
            gap: 10px;
            background: rgba(255,255,255,0.10);
            padding: 8px 10px;
            border-radius: 14px;
            width: fit-content;
        }}
        div[role="radiogroup"] label {{
            background: rgba(255,255,255,0.16);
            border-radius: 12px;
            padding: 6px 12px;
            border: 1px solid rgba(255,255,255,0.20);
        }}
        </style>

        <div class="video-bg">
            <video autoplay muted loop playsinline>
                <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
            </video>
        </div>

        <div class="video-overlay"></div>

        <div class="hallmark">✨ Data Nuggets By Rishita</div>
        """,
        unsafe_allow_html=True
    )


def card_open():
    st.markdown('<div class="card">', unsafe_allow_html=True)


def card_close():
    st.markdown("</div>", unsafe_allow_html=True)
