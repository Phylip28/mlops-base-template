import streamlit as st


def render_overview(log_count: int) -> None:
    cols = st.columns(5)
    metrics = [
        ("5", "Services", "primary"),
        ("2", "Containers", "accent"),
        (str(log_count), "Log Events", "success"),
        ("30", "Retrain Threshold", "warning"),
        ("8000", "API Port", "danger"),
    ]
    for col, (val, lbl, color) in zip(cols, metrics):
        border_class = f"{color}-top"
        with col:
            st.markdown(
                f"""
            <div class="metric-card {border_class}">
                <div class="metric-value">{val}</div>
                <div class="metric-label">{lbl}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
