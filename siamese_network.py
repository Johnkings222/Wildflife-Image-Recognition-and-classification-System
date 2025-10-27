"""
Wildlife Image Recognition using Pretrained ResNet18
Uses ImageNet classification for accurate species detection
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image
import numpy as np
import json


# ImageNet wildlife class mappings (class_idx: species_name)
# These are actual ImageNet classes for wildlife animals
IMAGENET_WILDLIFE_CLASSES = {
    # Big Cats
    288: "Leopard",
    289: "Snow Leopard",
    290: "Jaguar",
    291: "Lion",
    292: "Tiger",
    293: "Cheetah",
    281: "Tabby Cat",
    282: "Tiger Cat",
    283: "Persian Cat",

    # Canines
    273: "Dingo",
    274: "Wild Dog",
    275: "African Hunting Dog",

    # Bears
    294: "Brown Bear",
    295: "American Black Bear",
    296: "Ice Bear (Polar Bear)",
    297: "Sloth Bear",

    # Elephants
    385: "Indian Elephant",
    386: "African Elephant",

    # Primates
    365: "Gorilla",
    366: "Chimpanzee",
    367: "Orangutan",
    368: "Gibbon",
    369: "Baboon",
    370: "Macaque",
    371: "Langur",
    372: "Colobus Monkey",
    373: "Proboscis Monkey",
    374: "Marmoset",
    375: "Capuchin",
    376: "Spider Monkey",

    # Ungulates (Hoofed Animals)
    340: "Zebra",
    341: "Pig",
    342: "Wild Boar",
    343: "Warthog",
    344: "Hippopotamus",
    345: "Ox",
    346: "Water Buffalo",
    347: "Bison",
    349: "Gazelle",
    350: "Antelope",
    351: "Impala",
    352: "Bighorn Sheep",
    353: "Ibex",

    # Giraffe and Okapi
    354: "Giraffe",

    # Rhinoceros
    356: "Rhinoceros",

    # Other Mammals
    357: "Hamster",
    358: "Porcupine",
    359: "Fox Squirrel",
    360: "Marmot",
    361: "Beaver",
    362: "Guinea Pig",
    363: "Hog",
    364: "Sorrel (Horse)",

    # Marine Mammals
    147: "Sea Lion",
    148: "Seal",

    # Birds
    7: "Cock (Rooster)",
    8: "Hen",
    9: "Ostrich",
    10: "Brambling",
    11: "Goldfinch",
    12: "House Finch",
    13: "Junco",
    14: "Indigo Bunting",
    15: "Robin",
    16: "Bulbul",
    17: "Jay",
    18: "Magpie",
    19: "Chickadee",
    20: "Water Ouzel",
    21: "Kite",
    22: "Bald Eagle",
    23: "Vulture",
    24: "Great Grey Owl",
    80: "Black Grouse",
    81: "Ptarmigan",
    82: "Ruffed Grouse",
    83: "Prairie Chicken",
    84: "Peacock",
    85: "Quail",
    86: "Partridge",
    87: "African Grey Parrot",
    88: "Macaw",
    89: "Sulphur-Crested Cockatoo",
    90: "Lorikeet",
    127: "White Stork",
    128: "Black Stork",
    129: "Spoonbill",
    130: "Flamingo",
    131: "Little Blue Heron",
    132: "American Egret",
    133: "Bittern",
    134: "Crane",
    135: "Limpkin",
    136: "European Gallinule",
    137: "American Coot",
    138: "Bustard",
    139: "Ruddy Turnstone",
    140: "Red-Backed Sandpiper",
    141: "Redshank",
    142: "Dowitcher",
    143: "Oystercatcher",
    144: "Pelican",
    145: "King Penguin",
    146: "Albatross",

    # Reptiles
    31: "Tree Frog",
    32: "Tailed Frog",
    33: "Loggerhead Turtle",
    34: "Leatherback Turtle",
    35: "Mud Turtle",
    36: "Terrapin",
    37: "Box Turtle",
    38: "Banded Gecko",
    39: "Common Iguana",
    40: "American Chameleon",
    41: "Whiptail Lizard",
    42: "Agama",
    43: "Frilled Lizard",
    44: "Alligator Lizard",
    45: "Gila Monster",
    46: "Green Lizard",
    47: "African Chameleon",
    48: "Komodo Dragon",
    49: "African Crocodile",
    50: "American Alligator",
    51: "Triceratops",
}


class WildlifeRecognitionModel:
    """
    Wildlife Recognition using Pretrained ResNet18 ImageNet Classifier
    """
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load pretrained ResNet18 with full classifier
        self.model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
        self.model.to(self.device)
        self.model.eval()

        # Image preprocessing (ImageNet standard)
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                              std=[0.229, 0.224, 0.225])
        ])

        # Load ImageNet class labels
        self.imagenet_classes = self._load_imagenet_classes()

    def _load_imagenet_classes(self):
        """
        Create mapping of all ImageNet classes
        """
        # This is a simplified version - in production you'd load from a JSON file
        # For now, we use our wildlife mapping
        return IMAGENET_WILDLIFE_CLASSES

    def preprocess_image(self, image_path):
        """
        Load and preprocess an image
        """
        image = Image.open(image_path).convert('RGB')
        image_tensor = self.transform(image).unsqueeze(0)
        return image_tensor.to(self.device)

    def predict(self, image_path, top_k=5):
        """
        Predict species for an input image using ImageNet classification
        Returns top-k predictions with confidence scores
        """
        # Preprocess image
        image_tensor = self.preprocess_image(image_path)

        # Get predictions
        with torch.no_grad():
            outputs = self.model(image_tensor)
            probabilities = F.softmax(outputs, dim=1)

        # Get top predictions from all ImageNet classes
        top_probs, top_indices = torch.topk(probabilities[0], k=100)

        # Filter for wildlife classes and get top-k
        wildlife_predictions = []
        seen_species = set()

        for prob, idx in zip(top_probs, top_indices):
            idx = idx.item()
            prob = prob.item() * 100  # Convert to percentage

            if idx in IMAGENET_WILDLIFE_CLASSES:
                species_name = IMAGENET_WILDLIFE_CLASSES[idx]

                # Avoid duplicate species (aggregate probabilities)
                if species_name not in seen_species:
                    wildlife_predictions.append((species_name, prob))
                    seen_species.add(species_name)
                else:
                    # If species already seen, add probabilities
                    for i, (name, existing_prob) in enumerate(wildlife_predictions):
                        if name == species_name:
                            wildlife_predictions[i] = (name, existing_prob + prob * 0.5)
                            break

                if len(wildlife_predictions) >= top_k * 2:
                    break

        # Sort by confidence and return top-k
        wildlife_predictions.sort(key=lambda x: x[1], reverse=True)

        # If no wildlife detected, return top general predictions
        if not wildlife_predictions:
            return self._get_general_predictions(probabilities[0], top_k)

        return wildlife_predictions[:top_k]

    def _get_general_predictions(self, probabilities, top_k):
        """
        Fallback: Get general ImageNet predictions if no wildlife detected
        """
        # Get top indices
        top_probs, top_indices = torch.topk(probabilities, k=top_k)

        predictions = []
        for prob, idx in zip(top_probs, top_indices):
            idx = idx.item()
            prob = prob.item() * 100

            # Use class index as label if not in our mapping
            if idx in IMAGENET_WILDLIFE_CLASSES:
                label = IMAGENET_WILDLIFE_CLASSES[idx]
            else:
                label = f"Class {idx}"

            predictions.append((label, prob))

        return predictions


# Siamese Network kept for future few-shot learning implementation
class SiameseNetwork(nn.Module):
    """
    Siamese Network with shared ResNet18 backbone
    (For future few-shot learning implementation)
    """
    def __init__(self, embedding_dim=128):
        super(SiameseNetwork, self).__init__()

        # Load pretrained ResNet18
        resnet = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)

        # Remove the final classification layer
        self.backbone = nn.Sequential(*list(resnet.children())[:-1])

        # Add custom embedding layer
        self.fc = nn.Sequential(
            nn.Linear(512, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(256, embedding_dim)
        )

    def forward_one(self, x):
        """
        Forward pass for one image through the shared backbone
        """
        x = self.backbone(x)
        x = x.view(x.size()[0], -1)
        x = self.fc(x)
        return x

    def forward(self, input1, input2):
        """
        Forward pass for both images
        """
        output1 = self.forward_one(input1)
        output2 = self.forward_one(input2)
        return output1, output2

    def get_embedding(self, x):
        """
        Get embedding for a single image
        """
        return self.forward_one(x)


# Main prediction function
def predict_species(image_path):
    """
    Main prediction function using ImageNet classifier
    Returns species name and confidence
    """
    model = WildlifeRecognitionModel()
    predictions = model.predict(image_path, top_k=5)
    return predictions
