"""A file-driven Streamlit portfolio for essays, projects, and research notes.

Run locally with: streamlit run main.py
Add content by dropping Markdown or plain-text files into the posts/ directory.
The first line is the title, the second line is the subtitle, and the remaining
text is rendered as the article body.
"""

from dataclasses import dataclass
import itertools
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
CIRCLE_TOKEN = "[INSERT_CIRCLE_EXPLORER]"


@dataclass(frozen=True)
class Post:
    """The small, predictable content contract used by the site."""

    slug: str
    title: str
    subtitle: str
    body: str
    path: Path


def load_posts() -> list[Post]:
    """Load valid .md/.txt posts, ordered by filename for stable navigation.

    Every post is intentionally plain text: title on line one, subtitle on line
    two, and Markdown content after that. This keeps adding a page as simple as
    creating a file in ``posts/``.
    """
    POSTS_DIR.mkdir(exist_ok=True)
    posts: list[Post] = []

    for path in sorted(POSTS_DIR.glob("*")):
        if not path.is_file() or path.suffix.lower() not in {".md", ".txt"}:
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        if len(lines) < 2 or not lines[0].strip() or not lines[1].strip():
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
        
        /* Keep the spacing tight to fix the top-left alignment gap */
        [data-testid="stSidebar"] { background: #F1EFE9; border-right: 1px solid var(--line); }
        [data-testid="stSidebar"] > div:first-child { padding-top: 1.25rem !important; }
        
        .block-container { max-width: 1180px; padding: 4rem 4rem 6rem; }
        .site-kicker, .post-meta, .eyebrow { color: var(--accent); font: 500 .72rem/1.4 'DM Mono', monospace; letter-spacing: .08em; text-transform: uppercase; }
        .site-subtitle { color: var(--muted); font: .88rem/1.55 'Libre Baskerville', serif; max-width: 18rem; }
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
        @media (max-width: 700px) { .block-container { padding: 2.5rem 1.25rem 4rem; } .post-title { font-size: 2.5rem; } }
        .post-meta { color: var(--accent); font-size: 0.8rem; font-weight: 500; text-transform: uppercase; letter-spacing: .05em; }
        
        /* Clean default typography settings */
        .site-name { color: var(--ink); font-weight: 700; font-size: 1.25rem; margin: 0 0 1rem 0; }
        .post-title { color: var(--ink); font-weight: 700; font-size: 3rem; margin: .8rem 0 1rem; max-width: 900px; }
        .post-subtitle { color: var(--muted); font-size: 1.15rem; max-width: 720px; }
        .rule { border-top: 1px solid var(--line); margin: 1.5rem 0; }
        
        .footer { border-top: 1px solid var(--line); color: var(--muted); font-size: 0.8rem; margin-top: 5rem; padding-top: 1rem; }

        /* FORCE REMOVE STREAMLIT HOSTING UI */
        /* Hides the top-right toolbar including 'Fork this app', 'Deploy', and 'Manage app' statuses */
        [data-testid="stStatusWidget"], [data-testid="stToolbar"], .stDeployButton { 
            display: none !important; 
            visibility: hidden !important; 
        }
        
        /* Hides the default hamburger Main Menu dropdown */
        #MainMenu { 
            display: none !important; 
            visibility: hidden !important; 
        }
        
        /* Removes the bottom footer 'Made with Streamlit' tag */
        footer { 
            display: none !important; 
            visibility: hidden !important; 
        }
        
        /* Ensures layout adjustment bars don't render background block artifacts */
        header { 
            visibility: hidden !important; 
        }
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


def _proper_segment_intersection(first: np.ndarray, second: np.ndarray, third: np.ndarray, fourth: np.ndarray) -> bool:
    """Return whether two segments cross away from all four endpoints."""
    def orientation(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
        return float(np.cross(b - a, c - a))

    first_turn = orientation(first, second, third)
    second_turn = orientation(first, second, fourth)
    third_turn = orientation(third, fourth, first)
    fourth_turn = orientation(third, fourth, second)
    epsilon = 1e-9
    return (
        ((first_turn > epsilon and second_turn < -epsilon) or (first_turn < -epsilon and second_turn > epsilon))
        and ((third_turn > epsilon and fourth_turn < -epsilon) or (third_turn < -epsilon and fourth_turn > epsilon))
    )


def render_circle_explorer() -> None:
    """Let readers explore how chords and interior crossings create regions."""
    st.markdown(
        "**Build your own circle.** Move the controls, then watch the chords add "
        "vertices and faces. Random placement avoids the special coincidences that "
        "make the famous pattern break."
    )
    left, right = st.columns([1, 2.2])
    with left:
        point_count = st.slider("Points on the circle", 2, 14, 6, key="moser_point_count")
        placement = st.radio(
            "Placement",
            ["General position", "Evenly spaced"],
            key="moser_placement",
            help="General position keeps three chords from meeting at one interior point.",
        )
        seed = st.slider("Arrangement", 0, 100, 17, key="moser_seed", disabled=placement == "Evenly spaced")

    if placement == "Evenly spaced":
        angles = np.linspace(0, 2 * np.pi, point_count, endpoint=False) + np.pi / 2
    else:
        rng = np.random.default_rng(seed)
        angles = np.sort(rng.uniform(0, 2 * np.pi, point_count))
    points = np.column_stack((np.cos(angles), np.sin(angles)))

    chords = list(itertools.combinations(range(point_count), 2))
    crossing_count = sum(
        _proper_segment_intersection(points[i], points[j], points[k], points[l])
        for chord_index, (i, j) in enumerate(chords)
        for k, l in chords[chord_index + 1:]
        if len({i, j, k, l}) == 4
    )
    chord_count = len(chords)
    region_count = 1 + chord_count + crossing_count
    maximum = 1 + chord_count + (point_count * (point_count - 1) * (point_count - 2) * (point_count - 3)) // 24

    figure = go.Figure()
    circle = np.linspace(0, 2 * np.pi, 300)
    figure.add_trace(go.Scatter(
        x=np.cos(circle), y=np.sin(circle), mode="lines",
        line={"color": "#e6b566", "width": 3}, hoverinfo="skip", showlegend=False,
    ))
    for i, j in chords:
        figure.add_trace(go.Scatter(
            x=[points[i, 0], points[j, 0]], y=[points[i, 1], points[j, 1]],
            mode="lines", line={"color": "#8bb8b0", "width": 1.2},
            hoverinfo="skip", showlegend=False,
        ))
    figure.add_trace(go.Scatter(
        x=points[:, 0], y=points[:, 1], mode="markers+text",
        text=[str(index + 1) for index in range(point_count)],
        textposition="top center", marker={"size": 11, "color": "#f28f79"},
        hovertemplate="Point %{text}<extra></extra>", showlegend=False,
    ))
    figure.update_layout(
        height=520, margin={"l": 10, "r": 10, "t": 10, "b": 10},
        paper_bgcolor="#fffaf2", plot_bgcolor="#fffaf2", showlegend=False,
        xaxis={"visible": False, "range": [-1.18, 1.18], "scaleanchor": "y"},
        yaxis={"visible": False, "range": [-1.18, 1.18]},
    )
    with right:
        st.plotly_chart(figure, use_container_width=True, config={"displaylogo": False})

    metric_one, metric_two, metric_three = st.columns(3)
    metric_one.metric("Regions", region_count)
    metric_two.metric("Chords", chord_count)
    metric_three.metric("Interior crossings", crossing_count)
    if region_count == maximum:
        st.success(f"This arrangement reaches the general-position count: {maximum} regions.")
    else:
        st.info(
            f"This arrangement has {region_count} regions. The maximum for {point_count} points "
            f"is {maximum}; evenly spaced points can create extra coincidences."
        )


def render_body(body: str) -> None:
    """Split plot placeholders from Markdown so both systems remain composable."""
    sections = re.split(f"({re.escape(PLOT_TOKEN)}|{re.escape(CIRCLE_TOKEN)})", body)
    for section in sections:
        if section == PLOT_TOKEN:
            render_superposition_plot()
        elif section == CIRCLE_TOKEN:
            render_circle_explorer()
        elif section.strip():
            # Let Streamlit parse Markdown and LaTeX directly; raw HTML wrappers can disable both.
            st.markdown(section)


def main() -> None:
    st.set_page_config(page_title=SITE_CONFIG["AUTHOR_NAME"], page_icon="✳", layout="wide", initial_sidebar_state="expanded")
    inject_styles()
    posts = load_posts()

    with st.sidebar:
        st.markdown(f'<p class="site-name">{SITE_CONFIG["AUTHOR_NAME"]}</p><p class="site-subtitle">{SITE_CONFIG["SUBTITLE"]}</p>', unsafe_allow_html=True)
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
