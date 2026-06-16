# Architecture Documentation

## Overview

GPT Translator is built using a **declarative, interface-driven architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                  Entry Points                           │
├──────────────────────┬──────────────────────────────────┤
│   train.py           │   translate.py                   │
└──────────────────────┴──────────────────────────────────┘
         │                         │
         ▼                         ▼
┌─────────────────────┐   ┌──────────────────────┐
│ TrainingPipeline    │   │  GPTTranslator       │
└─────────────────────┘   │  TranslatorApp       │
         │                └──────────────────────┘
         │
    ┌────┴────┬─────────────────┬──────────────┐
    ▼         ▼                 ▼              ▼
┌────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Data   │ │ Data     │ │ Model    │ │ Config   │
│Handler │ │Validator │ │Trainer   │ │Loader    │
└────────┘ └──────────┘ └──────────┘ └──────────┘
    │         │              │
    └────┬────┴──────────────┘
         │
         ▼
    ┌──────────────┐
    │  Interfaces  │
    │  (Abstract)  │
    └──────────────┘
```

## Core Components

### 1. Configuration Layer (`src/core/`)

#### `config.py`
- **`ConfigLoader`**: Loads YAML configuration files with environment variable substitution
  - Supports `${ENV_VAR}` syntax in YAML
  - Loads from `config/config.yaml` and `config/training_config.yaml`
  
- **`Settings`**: Pydantic model for environment-based configuration
  - Uses `python-dotenv` to load `.env` file
  - Type-safe configuration access

**Files involved:**
- `config/config.yaml` - Main application configuration
- `config/training_config.yaml` - Training-specific parameters
- `.env` - Environment variables (API keys, etc.)

#### `interfaces.py`
- **`DataValidator`**: Abstract interface for data validation
  - Method: `validate(data) -> (is_valid, errors)`
  
- **`DataProcessor`**: Abstract interface for data processing
  - Method: `process(input_path, output_path) -> bool`
  
- **`ModelTrainer`**: Abstract interface for model training
  - Methods: `start_training()`, `get_status()`, `wait_completion()`
  
- **`Translator`**: Abstract interface for translation
  - Method: `translate(text, model_id) -> str`

### 2. Training Pipeline (`src/training/`)

#### `validator.py`
- **`TranslationDataValidator`** (implements `DataValidator`)
  - Validates JSON format for fine-tuning data
  - Checks required fields: `messages`, `completion`
  - Validates message structure with `role` and `content`
  - Validates sample count (min/max from config)
  - Returns detailed error list for debugging

#### `data_handler.py`
- **`TranslationDataHandler`** (implements `DataProcessor`)
  - Loads JSON files
  - Validates using `TranslationDataValidator`
  - Converts JSON to JSONL format (one sample per line)
  - Splits data into training/validation sets
  - Handles file I/O and directory creation

#### `model.py`
- **`OpenAIModelTrainer`** (implements `ModelTrainer`)
  - Manages interaction with OpenAI Fine-tuning API
  - Uploads training files to OpenAI
  - Starts fine-tuning jobs
  - Monitors job status with polling
  - Handles completion and returns model ID
  - Lists all fine-tuning jobs

#### `pipeline.py`
- **`TrainingPipeline`**
  - Orchestrates complete training workflow:
    1. Data preparation (validation + JSONL conversion)
    2. Train/validation split
    3. Fine-tuning job submission
    4. Optional: Wait for completion with logging
  - Provides summary logging of each step
  - Error handling and detailed logging

### 3. Translator (`src/translator/`)

#### `translator.py`
- **`GPTTranslator`** (implements `Translator`)
  - Sends requests to OpenAI API for translation
  - Uses configurable model (base or fine-tuned)
  - Customizable inference parameters (temperature, max_tokens)
  - Can switch models at runtime with `set_model()`
  - Handles API errors with logging

#### `app.py`
- **`TranslatorApp`**
  - PyEdifice-based web GUI
  - Two-column interface:
    - Left: Russian text input
    - Right: English translation output
  - Features:
    - "Translate" button for API call
    - "Clear" button to reset form
    - Status messages (success/error/loading)
    - Non-blocking translation (state tracking)
  - Event handlers for user interactions

## Data Flow

### Training Flow

```
Raw JSON File
    │
    ▼
[TranslationDataHandler.process()]
    │
    ├─→ Load JSON
    │
    ├─→ [TranslationDataValidator.validate()]
    │   ├─→ Check format
    │   ├─→ Validate fields
    │   └─→ Return errors if invalid
    │
    ├─→ Convert to JSONL
    │
    └─→ Save JSONL file
        │
        ▼
    [TrainingPipeline.run()]
        │
        ├─→ Split train/validation
        │
        ├─→ [OpenAIModelTrainer.start_training()]
        │   ├─→ Upload file to OpenAI
        │   └─→ Submit fine-tuning job
        │
        └─→ [OpenAIModelTrainer.wait_completion()]
            ├─→ Poll job status
            ├─→ Log progress
            └─→ Return model ID when done
                │
                ▼
            Fine-tuned Model
            (ft-gpt-4o-mini-...)
```

### Translation Flow

```
Russian Text Input
    │
    ▼
[GPTTranslator.translate()]
    │
    ├─→ Prepare API request:
    │   ├─→ System message (translator prompt)
    │   └─→ User message (text to translate)
    │
    ├─→ Call OpenAI API
    │
    ├─→ Extract response
    │
    └─→ Return English translation
        │
        ▼
    English Text Output
```

## Class Design

### Inheritance & Interfaces

All implementations follow **Liskov Substitution Principle**:

```
DataValidator (ABC)
    │
    └─→ TranslationDataValidator

DataProcessor (ABC)
    │
    └─→ TranslationDataHandler

ModelTrainer (ABC)
    │
    └─→ OpenAIModelTrainer

Translator (ABC)
    │
    └─→ GPTTranslator
```

### Dependency Injection

Configuration is injected into classes:

```python
config = ConfigLoader().get_main_config()
translator = GPTTranslator(config)
validator = TranslationDataValidator(config)
```

This allows:
- Easy testing with mock configs
- Parameter changes without code modification
- Swapping implementations (if needed)

## Configuration Management

### YAML Structure

**`config.yaml`** (main config):
```yaml
app:
  name: GPT Translator
openai:
  api_key: ${OPENAI_API_KEY}  # From .env
  model: gpt-4o-mini
paths:
  data_raw: ./data/raw
  ...
```

**`training_config.yaml`** (training-specific):
```yaml
training:
  validation_split: 0.2
  batch_size: 8
fine_tuning:
  model: gpt-4o-mini
  suffix: translation-v1
validation:
  min_samples: 5
  max_samples: 10000
inference:
  temperature: 0.3
  max_tokens: 2000
```

### Environment Variables

Loaded from `.env`:
```
OPENAI_API_KEY=sk-...
LOG_LEVEL=INFO
```

Accessible via `ConfigLoader.settings`:
```python
loader = ConfigLoader()
api_key = loader.settings.openai_api_key
```

## Entry Points

### Training (`train.py`)

```python
pipeline = TrainingPipeline(config)
model_id = pipeline.run(data_path, wait_for_completion=True)
```

Features:
- Data validation before training
- Progress logging
- Job status tracking
- List all jobs

### Translation (`translate.py`)

```python
translator = GPTTranslator(config, model_id="ft-xxx")
result = translator.translate(text)
```

Features:
- GUI mode: `python translate.py --gui`
- CLI mode: `python translate.py --text "..."`
- File mode: `python translate.py --file input.txt`

## Error Handling

### Validation Errors
- Caught in `DataValidator.validate()`
- Returns list of detailed error messages
- Pipeline stops with clear error output

### Training Errors
- OpenAI API errors caught in `ModelTrainer`
- Logged with exception context
- Pipeline fails gracefully

### Translation Errors
- API errors caught in `GPTTranslator.translate()`
- Displayed in GUI status
- Logged for debugging

## Logging

### Levels
- `DEBUG`: Detailed execution flow
- `INFO`: Important events (default)
- `WARNING`: Potential issues
- `ERROR`: Failures with context

### Output
- Console: Human-readable format
- Files:
  - `logs/training.log` - Training events
  - `logs/translator.log` - Translation app events

## Testing

### `test_components.py`
- Tests config loading
- Tests data validation
- Tests data processing
- Runs without API calls

### `examples.py`
- Shows usage patterns
- Demonstrates API calls
- Shows configuration

## Extensibility

### Adding New Validator
```python
class CustomValidator(DataValidator):
    def validate(self, data):
        # Custom validation logic
        return is_valid, errors
```

### Adding New Translator
```python
class CustomTranslator(Translator):
    def translate(self, text, model_id=None):
        # Custom translation logic
        return translated_text
```

### Adding New Model Trainer
```python
class CustomTrainer(ModelTrainer):
    def start_training(self, data_path):
        # Custom training logic
        return job_id
```

## Design Principles

1. **Declarative Configuration**: All parameters in YAML, no magic numbers
2. **Interface-Driven Design**: Abstract interfaces for all major components
3. **Single Responsibility**: Each class has one reason to change
4. **Dependency Injection**: Configuration injected, not hardcoded
5. **Error Clarity**: Detailed error messages for debugging
6. **Logging**: Comprehensive logging for monitoring
7. **No Hidden State**: State explicitly managed in objects
8. **Composability**: Small components combined for complex tasks

## Performance Considerations

- **Data Validation**: Linear O(n) scan for validation
- **JSONL Conversion**: Streaming for large files
- **API Polling**: Configurable check intervals (default 30s)
- **GUI**: Non-blocking translation with state tracking
- **Memory**: Efficient streaming for large files

## Future Extensions

Possible extensions following the architecture:

1. **Multiple Translation Directions**: Add translator pairs (RU→EN, EN→RU, etc.)
2. **Batch Translation**: Process multiple texts efficiently
3. **Model Comparison**: Compare base vs. fine-tuned models
4. **Advanced Validation**: Language detection, spell checking
5. **Database Integration**: Store translations for analytics
6. **API Server**: FastAPI wrapper around translator
7. **Monitoring Dashboard**: Track translation quality metrics
