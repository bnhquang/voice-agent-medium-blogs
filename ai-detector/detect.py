"""How likely is a paragraph to be AI-written? Uses Desklib's open detector, stored in ./model. Runs locally.

    python detect.py "Your paragraph here."
    python detect.py "First paragraph." "Second paragraph."
"""

import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")  # library deprecation notices, not about your text

import torch
import torch.nn as nn
from transformers import AutoConfig, AutoModel, AutoTokenizer, PreTrainedModel
from transformers.utils import logging

logging.set_verbosity_error()
logging.disable_progress_bar()
MODEL_DIR = Path(__file__).resolve().parent / "model"


class DesklibAIDetectionModel(PreTrainedModel):  # as on the model card: DeBERTa, mean pooling, one linear head
    config_class = AutoConfig

    def __init__(self, config):
        super().__init__(config)
        self.model = AutoModel.from_config(config)
        self.classifier = nn.Linear(config.hidden_size, 1)
        self.post_init()

    def forward(self, input_ids, attention_mask):
        hidden = self.model(input_ids, attention_mask=attention_mask)[0]
        mask = attention_mask.unsqueeze(-1).float()
        return self.classifier((hidden * mask).sum(1) / mask.sum(1))


def main():
    paragraphs = sys.argv[1:]
    if not paragraphs:
        sys.exit('Usage: python detect.py "Your paragraph here."')
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = DesklibAIDetectionModel.from_pretrained(MODEL_DIR).eval()
    for i, text in enumerate(paragraphs, 1):
        inputs = tokenizer(text, truncation=True, max_length=768, return_tensors="pt")
        with torch.no_grad():
            p = torch.sigmoid(model(inputs["input_ids"], inputs["attention_mask"])).item()
        print(f"{i}. {p:.0%} AI  ({'AI' if p >= 0.5 else 'human'})  {text[:60]}{'...' if len(text) > 60 else ''}")


if __name__ == "__main__":
    main()
