# Publishing to PyPI

This guide explains how to package and publish **TheUltimateRAG** to the Python Package Index (PyPI) so users can install it via `pip install theultimaterag`.

## Prerequisites

1.  **PyPI Account**: Register at [pypi.org](https://pypi.org/).
2.  **API Token**: Go to Account Settings -> API Tokens and create a new token.

## 1. Prepare the Environment

Install the build and upload tools:

```bash
pip install --upgrade build twine
```

## 2. Build the Package

Run this command from the project root (where `pyproject.toml` is):

```bash
# Clean previous builds
rm -rf dist/

# Build Source and Wheel distribution
python -m build
```

You should see a `dist/` folder created containing `.whl` and `.tar.gz` files.

## 3. Upload to PyPI

### TestPyPI (Optional but Recommended)

First, upload to TestPyPI to verify everything works without affecting the real index.

```bash
python -m twine upload --repository testpypi dist/*
```

### Real PyPI

Once confident, upload to the real index:

```bash
python -m twine upload dist/*
```

- **Username**: `__token__`
- **Password**: Your PyPI API Token (`pypi-...`)

## 4. Verification

After uploading, you can verify it by installing it in a fresh environment:

```bash
pip install theultimaterag
```
