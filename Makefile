# Makefile

# Target to remove __pycache__ directories
clean:
		find . -type d -name "__pycache__" -exec rm -r {} +
