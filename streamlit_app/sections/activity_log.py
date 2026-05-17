import streamlit as st


def render_log() -> None:
    log_entries = st.session_state.activity_log[-40:]
    if log_entries:
        log_html = ""
        for entry in reversed(log_entries):
            ts, tag, msg, level = entry
            level_class = f"log-{level}" if level in ("info", "error", "warn") else ""
            log_html += f"""
            <div class="log-entry {level_class}">
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
