from typing import List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Model and tokenizer loading (singleton pattern for efficiency)
MODEL_NAME = "t5-small"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(device)


def summarize_text(text: str) -> str:
    """
    Summarize a single news string into 2-3 plain English lines.
    """
    # T5 expects a prefix for summarization
    input_text = f"summarize: {text.strip()}"
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True).to(device)
    summary_ids = model.generate(
        inputs,
        max_length=60,
        min_length=20,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True,
        no_repeat_ngram_size=2,
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
    return summary.strip()


def summarize_batch(texts: List[str]) -> List[str]:
    """
    Summarize a batch of news strings into 2-3 plain English lines each.
    """
    input_texts = [f"summarize: {t.strip()}" for t in texts]
    inputs = tokenizer(input_texts, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
    summary_ids = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=60,
        min_length=20,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True,
        no_repeat_ngram_size=2,
    )
    summaries = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)
    return [s.strip() for s in summaries] 