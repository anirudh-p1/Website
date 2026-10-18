"""A file-driven Streamlit portfolio for essays, projects, and research notes.

Run locally with: streamlit run main.py
Add content by dropping Markdown or plain-text files into the posts/ directory.
The first line is the title, the second line is the subtitle, and the remaining
text is rendered as the article body.
"""

from dataclasses import dataclass
from pathlib import Path
import re

import numpy as np
import plotly.graph_objects as go
import streamlit as st


# Edit this block to change the identity of the whole site.
SITE_CONFIG = {
    "AUTHOR_NAME": "Anirudh P",
    "SUBTITLE": "",
}

POSTS_DIR = Path(__file__).parent / "posts"
PLOT_TOKEN = "[INSERT_PLOT_SUPERPOSITION]"


@dataclass(frozen=True)
class Post:
    """The small, predictable content contract used by the site."""

    slug: str
    title: str
    subtitle: str
    body: str
    path: Path


def load_posts() -> list[Post]:
    """Load every .md/.txt post, ordered by its filename for stable navigation."""
    POSTS_DIR.mkdir(exist_ok=True)
    posts: list[Post] = []

    for path in sorted(POSTS_DIR.glob("*")):
        if path.suffix.lower() not in {".md", ".txt"}:
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        if len(lines) < 2:
            continue
        posts.append(
            Post(
                slug=path.stem,
                title=lines[0].strip(),
                subtitle=lines[1].strip(),
                body="\n".join(lines[2:]).strip(),
                path=path,
            )
        )
    return posts


def inject_styles() -> None:
    """Keep layout and typography in one place so the visual system is easy to tune."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;700&family=Libre+Baskerville:wght@400;700&display=swap');

        :root { --paper: #FAF9F6; --ink: #1E1E1E; --muted: #6B6963; --line: #D9D6CE; --accent: #B45635; }
        .stApp { background: var(--paper); color: var(--ink); }
        [data-testid="stHeader"] { background: rgba(250, 249, 246, .94); }
        [data-testid="stSidebar"] { background: #F1EFE9; border-right: 1px solid var(--line); }
        [data-testid="stSidebar"] > div:first-child { padding-top: 3rem; }
        .block-container { max-width: 1180px; padding: 4rem 4rem 6rem; }
        .site-kicker, .post-meta, .eyebrow { color: var(--accent); font: 500 .72rem/1.4 'DM Mono', monospace; letter-spacing: .08em; text-transform: uppercase; }
        .site-name { color: var(--ink); font: 700 1.05rem/1.2 'DM Sans', sans-serif; margin: 0 0 .45rem; }
        .site-subtitle { color: var(--muted); font: .88rem/1.55 'Libre Baskerville', serif; max-width: 18rem; }
        .post-title { color: var(--ink); font: 700 clamp(2.3rem, 5vw, 4.5rem)/1.04 'Libre Baskerville', serif; letter-spacing: -.03em; margin: .8rem 0 1rem; max-width: 900px; }
        .post-subtitle { color: var(--muted); font: 1.12rem/1.65 'Libre Baskerville', serif; max-width: 720px; }
        .rule { border-top: 1px solid var(--line); margin: 2.2rem 0; }
        .article-copy { max-width: 730px; color: var(--ink); font: 1.02rem/1.85 'Libre Baskerville', serif; }
        [data-testid="stMarkdownContainer"] { color: var(--ink); font-family: 'Libre Baskerville', serif; line-height: 1.85; }
        [data-testid="stMarkdownContainer"] h1, [data-testid="stMarkdownContainer"] h2, [data-testid="stMarkdownContainer"] h3 { font-family: 'DM Sans', sans-serif; line-height: 1.2; }
        [data-testid="stMarkdownContainer"] code, [data-testid="stMarkdownContainer"] pre { font-family: 'DM Mono', monospace; }
        .article-copy h1, .article-copy h2, .article-copy h3 { font-family: 'DM Sans', sans-serif; line-height: 1.2; margin-top: 2.5rem; }
        .article-copy h2 { font-size: 1.55rem; }
        .article-copy a { color: var(--accent); }
        .article-copy blockquote { border-left: 2px solid var(--accent); color: var(--muted); margin-left: 0; padding-left: 1.2rem; }
        .article-copy code, .article-copy pre { font-family: 'DM Mono', monospace; font-size: .86em; }
        .article-copy pre { background: #EEECE6; border: 1px solid var(--line); border-radius: 2px; padding: 1.2rem; overflow-x: auto; }
        .footer { border-top: 1px solid var(--line); color: var(--muted); font: .78rem/1.6 'DM Mono', monospace; margin-top: 5rem; padding-top: 1rem; }
        @media (max-width: 700px) { .block-container { padding: 2.5rem 1.25rem 4rem; } .post-title { font-size: 2.5rem; } }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_superposition_plot() -> None:
    """Render an interactive 3D feature-space sketch for the special content token."""
    density = st.slider("Feature density", min_value=2, max_value=10, value=5, key="feature_density")
    angles = np.linspace(0, 2 * np.pi, density, endpoint=False)
    points = np.column_stack((np.cos(angles), np.sin(angles), np.sin(angles * 2) * 0.65))
    figure = go.Figure()
    figure.add_trace(
        go.Scatter3d(
            x=points[:, 0], y=points[:, 1], z=points[:, 2], mode="markers+text",
            text=[f"f{i + 1}" for i in range(density)], textposition="top center",
            marker={"size": 7, "color": "#B45635", "opacity": 0.95},
        )
    )
    for index, point in enumerate(points):
        figure.add_trace(
            go.Scatter3d(x=[0, point[0]], y=[0, point[1]], z=[0, point[2]],
                         mode="lines", line={"color": "#8E8A80", "width": 2},
                         hoverinfo="skip", showlegend=False)
        )
    figure.update_layout(
        height=560, margin={"l": 0, "r": 0, "t": 10, "b": 0},
        paper_bgcolor="#FAF9F6", plot_bgcolor="#FAF9F6", showlegend=False,
        scene={"xaxis": {"visible": False}, "yaxis": {"visible": False}, "zaxis": {"visible": False},
               "bgcolor": "#FAF9F6", "aspectmode": "cube"},
    )
    st.plotly_chart(figure, use_container_width=True, config={"displaylogo": False})


def render_body(body: str) -> None:
    """Split plot placeholders from Markdown so both systems remain composable."""
    sections = re.split(f"({re.escape(PLOT_TOKEN)})", body)
    for section in sections:
        if section == PLOT_TOKEN:
            render_superposition_plot()
        elif section.strip():
            # Let Streamlit parse Markdown and LaTeX directly; raw HTML wrappers can disable both.
            st.markdown(section)


def main() -> None:
    st.set_page_config(page_title=SITE_CONFIG["AUTHOR_NAME"], page_icon="✳", layout="wide", initial_sidebar_state="expanded")
    inject_styles()
    posts = load_posts()

    with st.sidebar:
        st.markdown(f'<p class="site-kicker"></p><p class="site-name">{SITE_CONFIG["AUTHOR_NAME"]}</p><p class="site-subtitle">{SITE_CONFIG["SUBTITLE"]}</p>', unsafe_allow_html=True)
        st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
        if posts:
            selected_slug = st.radio("Reading list", [post.slug for post in posts], format_func=lambda slug: next(post.title for post in posts if post.slug == slug), label_visibility="collapsed")
            selected = next(post for post in posts if post.slug == selected_slug)
        else:
            selected = None
            st.caption("Add a .md or .txt file to posts/ to begin.")
           
       

    if selected is None:
        st.markdown('<p class="site-kicker">Welcome</p><h1 class="post-title">A quiet place for unfinished ideas.</h1><p class="post-subtitle">Your first essay will appear here when you add it to the posts folder.</p>', unsafe_allow_html=True)
        return

    st.markdown(f'<p class="post-meta">{selected.slug.replace("_", " ")}</p><h1 class="post-title">{selected.title}</h1><p class="post-subtitle">{selected.subtitle}</p><div class="rule"></div>', unsafe_allow_html=True)
    render_body(selected.body)
    st.markdown(f'<div class="footer">{SITE_CONFIG["AUTHOR_NAME"]} · {selected.title}</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
