# Wildlife Image Recognition System

A Python-based wildlife species recognition system using Siamese Networks and Tkinter GUI.

## Features

- **Modern GUI Interface**: Clean and intuitive Tkinter-based interface
- **Siamese Network**: PyTorch-based few-shot learning with ResNet18 backbone
- **Real-time Predictions**: Upload wildlife images and get instant species predictions
- **Top-K Predictions**: View top 5 most likely species with confidence scores
- **Image Display**: Automatic image resizing to fit canvas while maintaining aspect ratio
- **Status Messages**: Real-time status updates during image loading and prediction

## Architecture

### Siamese Network
- **Backbone**: Pretrained ResNet18 for feature extraction
- **Embedding**: Custom fully-connected layers (512 → 256 → 128 dimensions)
- **Similarity Metric**: Cosine similarity for species matching
- **Few-shot Learning**: Supports learning from limited examples

### GUI Components
- **Title Bar**: Application branding
- **Button Frame**: Upload and Clear actions
- **Image Canvas**: Resizable image display with placeholder
- **Predictions Panel**: Scrollable list of top predictions with confidence bars
- **Status Bar**: Real-time operation feedback

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python wildlife_recognition_app.py
```

## Usage

1. **Upload Image**: Click the "Upload Image" button and select a wildlife image
2. **View Predictions**: The system will automatically predict the species and display:
   - Top prediction with species name and confidence
   - Top 5 predictions with visual confidence bars
3. **Clear**: Reset the interface to upload a new image

## Species Database

The system currently recognizes the following species (demo mode with synthetic embeddings):
- Leopard
- Lion
- Elephant
- Giraffe
- Zebra
- Rhino
- Buffalo
- Cheetah

**Note**: In demo mode, the system uses randomly initialized embeddings. For production use, the model should be trained on actual wildlife images to create meaningful species embeddings.

## Technical Details

### Model Architecture
```
Input Image (224x224)
    ↓
ResNet18 Backbone (pretrained)
    ↓
Flatten (512 features)
    ↓
FC Layer (512 → 256) + ReLU + Dropout
    ↓
FC Layer (256 → 128)
    ↓
128-dim Embedding
```

### Prediction Pipeline
1. Image preprocessing (resize, normalize)
2. Feature extraction through Siamese Network
3. Cosine similarity computation with reference embeddings
4. Confidence calculation and ranking
5. Return top-K predictions

## Future Enhancements

- Train model on real wildlife dataset (e.g., iNaturalist, Wildlife dataset)
- Add support for custom species reference images
- Implement model fine-tuning interface
- Add batch prediction mode
- Export predictions to CSV/JSON
- Add confidence threshold filtering
- Support for video frame analysis

## Requirements

- Python 3.8+
- PyTorch 2.0+
- Torchvision 0.15+
- Pillow 10.0+
- Tkinter (usually included with Python)

## License

This project is for educational and research purposes.
