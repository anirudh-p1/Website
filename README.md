# File-Driven Research Portfolio

A minimal Streamlit portfolio inspired by academic web essays. Content lives in `posts/`; the app discovers it automatically.

## Structure

```text
Website/
├── main.py
├── requirements.txt
└── posts/
	├── 1_superposition.md
	├── 2_3b1b_blog.md
	└── 3_math_projects.txt
```

Each post uses this format:

```text
Title
Subtitle

Markdown body, including $inline$ or $$block$$ LaTeX and fenced code.
```

Filenames control navigation order. Add `.md` or `.txt` files to `posts/`, and restart or reload Streamlit to see them. The special token `[INSERT_PLOT_SUPERPOSITION]` inserts the interactive Plotly visualization.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run main.py
```

Edit `SITE_CONFIG` at the top of `main.py` to update the author identity and social links globally.