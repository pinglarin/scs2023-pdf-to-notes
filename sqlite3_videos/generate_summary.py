import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm
from datasets import load_dataset, interleave_datasets
from transformers import DataCollatorForSeq2Seq, BartForConditionalGeneration, BartTokenizer, AutoTokenizer, AutoModelForSeq2SeqLM, pipeline, AutoModelForMaskedLM, DataCollatorForLanguageModeling, Trainer, Seq2SeqTrainer, TrainingArguments, Seq2SeqTrainingArguments
import evaluate

num_epoch = 2
metric = evaluate.load("accuracy")
# scientific_papers, wiki_asp
device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = BartTokenizer.from_pretrained("sshleifer/distilbart-xsum-12-1")
model = BartForConditionalGeneration.from_pretrained("sshleifer/distilbart-xsum-12-1")
model.train().to(device)
model.max_seq_length = 100000

classifier = pipeline("summarization", model=model, tokenizer=tokenizer, max_length=2706)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

def create_dataloader(data):
    data_shuffle = data.shuffle(seed=42)
    data_dataset = data_shuffle.with_format("torch")
    encoded_data = data_dataset.map(tokenizer, batched=True)
    dataloader = DataLoader(data_dataset, collate_fn=DataCollatorForLanguageModeling(tokenizer))
    return dataloader, encoded_data

def predict(x, y=None, showTxt=False):
    if showTxt:
        print("input text: ", x)
    result = classifier(x)
    print("predicted summary: ", result)
    if y != None:
        print("actual abstract: ", y)

def predict_text(text):
    
    result = classifier(text)
    return result

def summarize_text(classifier, text: str, max_len: int) -> str:
    try:
        summary = classifier(text, max_length=max_len, min_length=10, do_sample=False)
        return summary[0]["summary_text"]
    except IndexError as ex:
        print("Sequence length too large for model, cutting text in half and calling again")
        return summarize_text(classifier, text=text[:(len(text) // 2)], max_len=max_len//2) + summarize_text(classifier, text=text[(len(text) // 2):], max_len=max_len//2)

def summarize(text, max_len=1024):
    try:
        summary = classifier(text, max_length=max_len, min_length=10, do_sample=False)
        return summary[0]["summary_text"]
    except IndexError as ex:
        print("Sequence length too large for model, cutting text in half and calling again")
        return summarize_text(classifier, text=text[:(len(text) // 2)], max_len=max_len//2) + summarize_text(classifier, text=text[(len(text) // 2):], max_len=max_len//2)


train1 = load_dataset("scientific_papers", name="pubmed", split="train", streaming=True, cache_dir="./cache")
train2 = load_dataset("scientific_papers", name="arxiv", split="train", streaming=True, cache_dir="./cache")
val1 = load_dataset("scientific_papers", name="pubmed", split="validation", streaming=True, cache_dir="./cache")
val2 = load_dataset("scientific_papers", name="arxiv", split="validation", streaming=True, cache_dir="./cache")

train_mixed = interleave_datasets([train1, train2])
val_mixed = interleave_datasets([val1, val2])

train_mixed = train_mixed.with_format("torch")
val_mixed = val_mixed.with_format("torch")

def tokenize_function(examples):
    return tokenizer(examples['article'], padding="max_length", truncation=True)


small_train_dataset = train_mixed.shuffle(seed=42).take(100)# .select(range(1000))
small_eval_dataset = val_mixed.shuffle(seed=42).take(20) # .select(range(1000))

tokenized_train = small_train_dataset.map(tokenize_function, batched=True)
tokenized_val = small_eval_dataset.map(tokenize_function, batched=True)

training_args = Seq2SeqTrainingArguments(
    output_dir="./results",
    learning_rate=2e-5,
    per_device_train_batch_size=32,
    weight_decay=0.01,
    max_steps=int(1e6),
    evaluation_strategy="epoch",
    num_train_epochs=num_epoch,
    # generation_config='./config'
)

trainer = Seq2SeqTrainer(
    model=model,
    tokenizer=tokenizer,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_val,
    data_collator=data_collator,
)

trainer.train()