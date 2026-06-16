# Setup & Installation Guide

## System Requirements

- Python 3.8+
- pip (Python package manager)
- OpenAI API key (https://platform.openai.com/api-keys)

## Step 1: Clone/Initialize Project

```bash
# If starting fresh
cd d:\Projects\gpt-translator
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

## Step 2: Create Virtual Environment

### Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Windows (Command Prompt)
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 4: Configure Environment

### Create `.env` file in project root:

```bash
# .env file
OPENAI_API_KEY=sk-your-actual-key-here
LOG_LEVEL=INFO
```

**Important**: Never commit `.env` to git (it's in `.gitignore`)

## Step 5: Verify Installation

```bash
# Run component tests
python test_components.py

# Expected output:
# ✓ PASS - Config Loader
# ✓ PASS - Data Validator
# ✓ PASS - Data Handler
# Total: 3/3 passed
```

## Step 6: Review Examples

```bash
# See usage examples
python examples.py

# Read documentation
cat QUICKSTART.md
cat README.md
cat ARCHITECTURE.md
```

## Troubleshooting

### ImportError: No module named 'openai'

```bash
pip install -r requirements.txt
```

### OpenAI API key issues

1. Check `.env` file exists in project root
2. Verify key format: `sk-...` (should start with `sk-`)
3. Get new key from https://platform.openai.com/api-keys

### pyedifice issues

```bash
pip install --upgrade pyedifice
```

### Config not loading

```bash
# Verify config files exist:
ls config/config.yaml
ls config/training_config.yaml

# Check for syntax errors:
python -c "import yaml; yaml.safe_load(open('config/config.yaml'))"
```

## Environment Details

### Python Version Check

```bash
python --version
# Should be 3.8 or higher
```

### Package Versions

```bash
pip list | grep -E "openai|pydantic|pyyaml|pyedifice"
```

### Directory Structure Check

```bash
# Should exist:
# - src/core/
# - src/training/
# - src/translator/
# - config/
# - data/raw/
# - data/processed/
# - data/models/
```

## Running the Project

### 1. Test with example data (no API needed)

```bash
python test_components.py
```

### 2. Prepare your data

Create `data/raw/my_translations.json` with training pairs

### 3. Start fine-tuning (requires OpenAI API key)

```bash
python train.py --data data/raw/my_translations.json --wait
```

### 4. Use the translator

```bash
# GUI mode
python translate.py --gui

# Command line
python translate.py --text "Привет"
```

## File Checklist

After setup, verify these files exist:

```
✓ .env
✓ .gitignore
✓ requirements.txt
✓ README.md
✓ QUICKSTART.md
✓ ARCHITECTURE.md
✓ SETUP.md
✓ train.py
✓ translate.py
✓ test_components.py
✓ examples.py
✓ config/config.yaml
✓ config/training_config.yaml
✓ src/core/config.py
✓ src/core/interfaces.py
✓ src/core/__init__.py
✓ src/training/validator.py
✓ src/training/data_handler.py
✓ src/training/model.py
✓ src/training/pipeline.py
✓ src/training/__init__.py
✓ src/translator/translator.py
✓ src/translator/app.py
✓ src/translator/__init__.py
✓ src/__init__.py
✓ data/raw/example_translations.json
✓ data/processed/ (directory, will be created)
✓ data/models/ (directory, will be created)
✓ logs/ (directory, will be created)
```

## First-Time Workflow

```bash
# 1. Verify setup
python test_components.py

# 2. View examples
python examples.py

# 3. Prepare your data
# Create data/raw/my_translations.json

# 4. Validate data
python -c "
from src.core import ConfigLoader
from src.training import TranslationDataValidator
config = ConfigLoader().get_training_config()
v = TranslationDataValidator(config)
import json
with open('data/raw/my_translations.json') as f:
    data = json.load(f)
valid, errors = v.validate(data)
print('Valid!' if valid else f'Errors: {errors}')
"

# 5. Start training
python train.py --data data/raw/my_translations.json

# 6. Check status
python train.py --job-id <job_id_from_above>

# 7. Launch GUI when ready
python translate.py --gui
```

## Common Issues & Solutions

### Issue: ModuleNotFoundError

**Solution**: Ensure you're in the project root directory

```bash
cd d:\Projects\gpt-translator
python train.py --help
```

### Issue: "Config file not found"

**Solution**: Run from project root (where `train.py` is)

```bash
# Good
python train.py --data data/raw/example_translations.json

# Bad - don't do this
cd src/training && python train.py
```

### Issue: OpenAI API timeout

**Solution**: Fine-tuning can take 10+ minutes

```bash
# Check status instead of waiting
python train.py --job-id <job_id>

# You can check later
# python train.py --job-id <job_id> --wait
```

### Issue: GUI not opening

**Solution**: Check if port is available and try again

```bash
# PyEdifice uses localhost:5000 by default
# Make sure no other service uses this port
```

## Next Steps

1. **Read QUICKSTART.md** for quick start guide
2. **Read README.md** for full documentation
3. **Read ARCHITECTURE.md** for design details
4. **Run examples.py** to see usage patterns
5. **Prepare your training data**
6. **Start fine-tuning**

## Getting Help

- **Installation issues**: Check Python version, run `pip install -r requirements.txt`
- **API issues**: Verify `.env` file has correct OPENAI_API_KEY
- **Configuration issues**: Run `python test_components.py`
- **Usage issues**: Check README.md or QUICKSTART.md
- **Architecture questions**: Read ARCHITECTURE.md

## Project Structure

```
gpt-translator/
├── config/                      # Configuration files
│   ├── config.yaml
│   └── training_config.yaml
├── src/                         # Source code
│   ├── core/                   # Core components
│   ├── training/               # Training pipeline
│   └── translator/             # Translation app
├── data/                        # Data directories
│   ├── raw/                    # Original files
│   ├── processed/              # Prepared files
│   └── models/                 # Model references
├── logs/                        # Log files
├── .env                         # Environment variables
├── .gitignore
├── requirements.txt
├── train.py                     # Training entry point
├── translate.py                 # Translator entry point
├── test_components.py           # Tests
├── examples.py                  # Usage examples
├── README.md                    # Full documentation
├── QUICKSTART.md               # Quick start guide
├── ARCHITECTURE.md             # Design documentation
└── SETUP.md                    # This file
```

## Ready to Start?

```bash
# Test installation
python test_components.py

# View quick start guide
cat QUICKSTART.md

# Or jump into training
python train.py --help
```

Good luck! 🚀
