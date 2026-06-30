uv run python obfuscator.py main.py
python3.13 -m py_compile dist.py
cp __pycache__/dist.*pyc dist.pyc
rm -rf __pycache__
rm dist.py