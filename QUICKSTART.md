# Quick Start Guide

## 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
# Edit .env file and add your OpenAI API key
OPENAI_API_KEY=sk-...
```

## 2. Test the Components

```bash
# Run tests to verify setup
python test_components.py
```

Expected output:
- ✓ Config Loader
- ✓ Data Validator
- ✓ Data Handler

## 3. Prepare Training Data

### Format

Create a JSON file with training examples:

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
        "content": "Привет, как дела?"
      }
    ],
    "completion": " Hello, how are you?"
  },
  {
    "messages": [
      {
        "role": "system",
        "content": "You are a professional translator. Translate the following Russian text to English, maintaining the original style and meaning."
      },
      {
        "role": "user",
        "content": "Это очень красивый день."
      }
    ],
    "completion": " It is a very beautiful day."
  }
]
```

**Important:**
- System message is the same for all examples
- User message contains Russian text
- Completion is the English translation
- Minimum 5 examples required
- Recommended 100+ examples for good results

### Save your data

Place your JSON file in `data/raw/`:
- `data/raw/my_translations.json`
- `data/raw/literary_translations.json`
- etc.

## 4. Fine-tune the Model

### Start Training

```bash
# Simple start
python train.py --data data/raw/my_translations.json

# Start and wait for completion (10+ minutes)
python train.py --data data/raw/my_translations.json --wait
```

Output will show:
```
[Step 1] Preparing data...
✓ File uploaded: file-xxx
✓ Validation passed

[Step 2] Starting fine-tuning...
Training job created: ft-abc123def456

[Step 3] Waiting for training completion...
Training in progress... Status: running
...
✓ Training completed successfully!
✓ Model ID: ft-gpt-4o-mini-2024-07-18-xxx
```

**Save the model ID!** You'll need it to use the trained model.

### Check Status Later

```bash
# Check specific job
python train.py --job-id ft-abc123def456

# List all jobs
python train.py --list-jobs
```

## 5. Use the Translator

### GUI Application

```bash
# Launch GUI with default model
python translate.py --gui

# Launch with fine-tuned model
python translate.py --model ft-gpt-4o-mini-2024-07-18-xxx --gui
```

The GUI will open in your browser:
1. Enter Russian text in the left panel
2. Click "Translate"
3. See English translation in the right panel

### Command Line

```bash
# Translate text
python translate.py --text "Привет, мир!"

# Translate file
python translate.py --file input.txt --output output.txt

# Use fine-tuned model
python translate.py --text "Привет" --model ft-xxx123
```

## Example Data Format (Russian-English)

Here are some examples for your training data:

### Greetings
```json
{
  "messages": [...],
  "completion": " Hello, how are you?"
}
```

### Questions
```json
{
  "messages": [...],
  "completion": " What is your name?"
}
```

### Statements
```json
{
  "messages": [...],
  "completion": " This is a beautiful day."
}
```

### Complex Sentences
```json
{
  "messages": [...],
  "completion": " The book was so interesting that I couldn't put it down."
}
```

## Troubleshooting

### "API key not found"
- Check `.env` file has `OPENAI_API_KEY=sk-...`
- Make sure it's in the project root

### "File not found"
- Check file path is correct
- Path should be relative to project root (where `train.py` is)

### "Validation failed"
- Check JSON structure matches examples
- All required fields present: `messages`, `completion`
- At least 2 items in messages array
- `completion` should be a non-empty string

### "Training timeout"
- Fine-tuning can take 10+ minutes
- Use `--wait` flag or check status with `--job-id`
- OpenAI may queue your job if API is busy

## Next Steps

1. **Collect data**: Gather 100+ Russian-English translation pairs
2. **Organize**: Put them in a JSON file in `data/raw/`
3. **Test**: Run `python test_components.py`
4. **Train**: Run `python train.py --data data/raw/my_data.json --wait`
5. **Use**: Launch GUI with `python translate.py --model ft-xxx --gui`

## Performance Tips

- **More data = Better results**: 100+ examples minimum
- **Quality over quantity**: Clean, accurate translations matter most
- **Diverse examples**: Include different types of text (casual, formal, technical)
- **Consistent format**: Use same system message for all examples
- **Monitor logs**: Check `logs/training.log` for details

## Configuration

Edit `config/training_config.yaml` to adjust:

```yaml
training:
  validation_split: 0.2     # 20% validation, 80% training
  learning_rate: 0.00002    # Learning rate for fine-tuning
  n_epochs: 3               # Number of training epochs

inference:
  temperature: 0.3          # Lower = more consistent
  max_tokens: 2000          # Max output length
  top_p: 1.0               # Diversity in output
```

## Getting Help

- Check logs in `logs/` directory
- Review `README.md` for detailed documentation
- Example data: `data/raw/example_translations.json`
- Run tests: `python test_components.py`
