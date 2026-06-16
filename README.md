# GPT Translator

Fine-tuning OpenAI's GPT-4o-mini model for Russian to English translations with a PyEdifice GUI application.

## Features

- **Fine-tuning Pipeline**: Automated data validation, preparation, and model training
- **Translation Translator**: Translate Russian text to English using base or fine-tuned models
- **PyEdifice GUI**: Simple web-based interface for interactive translations
- **Configuration-driven**: All parameters in YAML config files
- **Structured Architecture**: Class-based design with clear interfaces

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
LOG_LEVEL=INFO
```

### 3. Prepare Training Data

Create JSON file with training examples in format:

```json
[
  {
    "messages": [
      {
        "role": "system",
        "content": "You are a professional translator. Translate the following Russian text to English, maintaining the original style and meaning."
      },
      {
        "role": "user",
        "content": "Russian text here"
      }
    ],
    "completion": " English translation here"
  }
]
```

See `data/raw/example_translations.json` for examples.

## Usage

### Fine-tuning Model

```bash
# Start training with data
python train.py --data data/raw/example_translations.json

# Start training and wait for completion (can take 10+ minutes)
python train.py --data data/raw/example_translations.json --wait

# Check status of existing job
python train.py --job-id ft-abcd1234

# List all fine-tuning jobs
python train.py --list-jobs
```

### Using Translator

#### GUI Application

```bash
# Launch GUI with default model
python translate.py --gui

# Launch with specific fine-tuned model
python translate.py --model ft-xxx123 --gui
```

#### Command Line

```bash
# Translate single text
python translate.py --text "Hello world"

# Translate file
python translate.py --file input.txt --output output.txt

# Use fine-tuned model
python translate.py --text "Hello" --model ft-xxx123
```

## Configuration

### Main Config (`config/config.yaml`)

- `openai.api_key`: OpenAI API key (from environment)
- `openai.model`: Default model (gpt-4o-mini)
- `paths`: Data, models, and logs directories
- `logging`: Log level and format

### Training Config (`config/training_config.yaml`)

- `training`: Data split ratio, batch size, epochs
- `fine_tuning`: Model name and suffix
- `validation`: Min/max samples, token limits
- `inference`: Temperature, max_tokens, top_p

## Project Structure

```
gpt-translator/
├── config/
│   ├── config.yaml              # Main configuration
│   └── training_config.yaml     # Training parameters
├── src/
│   ├── core/
│   │   ├── config.py           # Configuration loader
│   │   └── interfaces.py        # Abstract interfaces
│   ├── training/
│   │   ├── pipeline.py         # Main training pipeline
│   │   ├── validator.py        # Data validation
│   │   ├── data_handler.py     # Data processing
│   │   └── model.py            # OpenAI fine-tuning
│   └── translator/
│       ├── translator.py        # Translation logic
│       └── app.py              # PyEdifice GUI
├── data/
│   ├── raw/                     # Original JSON files
│   ├── processed/              # Prepared JSONL files
│   └── models/                 # Model references
├── train.py                     # Training entry point
├── translate.py                # Translator entry point
└── requirements.txt            # Dependencies
```

## Classes & Interfaces

### Core Interfaces

- `DataValidator`: Validate training data
- `DataProcessor`: Process JSON to JSONL format
- `ModelTrainer`: Manage fine-tuning jobs
- `Translator`: Translate text

### Implementations

- `TranslationDataValidator`: JSON validation with detailed error reporting
- `TranslationDataHandler`: JSON to JSONL conversion with train/validation split
- `OpenAIModelTrainer`: OpenAI fine-tuning API integration
- `GPTTranslator`: Translation using OpenAI API
- `TranslatorApp`: PyEdifice GUI application

## Logging

Logs are saved to `logs/` directory:

- `logs/training.log`: Fine-tuning process logs
- `logs/translator.log`: Translation app logs

## Example Workflow

1. **Prepare data**:
   - Collect 100+ Russian-English translation pairs
   - Create `data/raw/my_translations.json`

2. **Train model**:
   ```bash
   python train.py --data data/raw/my_translations.json --wait
   ```
   - Note the returned model ID (e.g., `ft-xxx123`)

3. **Use model**:
   ```bash
   python translate.py --model ft-xxx123 --gui
   ```

## Notes

- Minimum 5 training samples required
- OpenAI fine-tuning takes 10+ minutes to complete
- Fine-tuned model IDs are returned after training succeeds
- GUI works best with 100+ training examples for noticeable improvement
