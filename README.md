# File-Driven Website

A minimal Streamlit portfolio inspired by academic web essays. Content lives in `posts/`; the app discovers it automatically.

## Structure

```text
Website/
├── main.py
├── requirements.txt
└── posts/
	└── 1_3b1b_blog.md
```

Each post uses this format:

```text
Title
Subtitle

Markdown body, including $inline$ or $$block$$ LaTeX and fenced code.
```

Filenames control navigation order. Add another `.md` or `.txt` file to
`posts/` to add another page, then restart or reload Streamlit to see it. Keep
the first two lines as the title and subtitle; everything after them is the
page body. The special token `[INSERT_PLOT_SUPERPOSITION]` inserts the
interactive Plotly visualization.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run main.py
```

Edit `SITE_CONFIG` at the top of `main.py` to update the author identity and social links globally.
