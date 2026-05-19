# ruff: noqa: E501
import streamlit as st

from streamlit_app.components.cards import page_header


def render() -> None:
    page_header("Activity Log", "Real-time stream of platform events")

    log_entries = st.session_state.activity_log[-60:]

    st.markdown(
        '<div style="margin-bottom:12px;display:flex;gap:8px;align-items:center;">'
        '<span style="font-family:JetBrains Mono,monospace;font-size:11px;color:var(--text-muted);">'
        f'{len(log_entries)} events</span>'
        '<span style="flex:1;"></span>'
        '<button class="refresh-btn" onclick="location.reload()" style="width:auto;padding:4px 12px;font-size:12px;">'
        '↻ Refresh</button>'
        '</div>',
        unsafe_allow_html=True,
    )

    if log_entries:
        log_html = ""
        for entry in reversed(log_entries):
            ts, tag, msg, level = entry
            log_html += f"""
            <div class="log-entry">
                <span class="log-ts">{ts}</span>
                <span class="log-tag log-tag-{tag}">{tag}</span>
                <span class="log-msg">{msg}</span>
            </div>
            """
        st.markdown(f'<div class="log-panel">{log_html}</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            '<div class="log-panel">'
            '<div class="log-entry">'
            '<span class="log-ts">--:--:--</span>'
            '<span class="log-tag log-tag-SYS">SYS</span>'
            '<span class="log-msg">Awaiting events...</span>'
            "</div></div>",
            unsafe_allow_html=True,
        )


render()
