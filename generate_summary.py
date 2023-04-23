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

# def convert_to_features(example_batch):
#     input_encodings = tokenizer.batch_encode_plus(example_batch['text'], pad_to_max_length=True, max_length=1024, truncation=True))
#     target_encodings = tokenizer.batch_encode_plus(example_batch['summary'], pad_to_max_length=True, max_length=1024, truncation=True))
    
#     labels = target_encodings['input_ids']
#     decoder_input_ids = shift_tokens_right(labels, model.config.pad_token_id)
#     labels[labels[:, :] == model.config.pad_token_id] = -100
    
#     encodings = {
#         'input_ids': input_encodings['input_ids'],
#         'attention_mask': input_encodings['attention_mask'],
#         'decoder_input_ids': decoder_input_ids,
#         'labels': labels,
#     }

#     return encodings

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




# DOWNLOAD DATASETS

# train1 = load_dataset("scientific_papers", name="pubmed", split="train", cache_dir="./cache", )
# train2 = load_dataset("scientific_papers", name="arxiv", split="train", cache_dir="./cache")
# test1 = load_dataset("scientific_papers", name="pubmed", split="test", cache_dir="./cache")
# test2 = load_dataset("scientific_papers", name="arxiv", split="test", cache_dir="./cache")
# val1 = load_dataset("scientific_papers", name="pubmed", split="validation", cache_dir="./cache")
# val2 = load_dataset("scientific_papers", name="arxiv", split="validation", cache_dir="./cache")

train1 = load_dataset("scientific_papers", name="pubmed", split="train", streaming=True, cache_dir="./cache")
train2 = load_dataset("scientific_papers", name="arxiv", split="train", streaming=True, cache_dir="./cache")
# test1 = load_dataset("scientific_papers", name="pubmed", split="test", streaming=True, cache_dir="./cache")
# test2 = load_dataset("scientific_papers", name="arxiv", split="test", streaming=True, cache_dir="./cache")
val1 = load_dataset("scientific_papers", name="pubmed", split="validation", streaming=True, cache_dir="./cache")
val2 = load_dataset("scientific_papers", name="arxiv", split="validation", streaming=True, cache_dir="./cache")

train_mixed = interleave_datasets([train1, train2])
# test_mixed = interleave_datasets([test1, test2])
val_mixed = interleave_datasets([val1, val2])

train_mixed = train_mixed.with_format("torch")
val_mixed = val_mixed.with_format("torch")

def tokenize_function(examples):
    
    # print(examples)
    return tokenizer(examples['article'], padding="max_length", truncation=True)

# tokenized_train = train_mixed.map(tokenize_function, batched=True)
# tokenized_val = val_mixed.map(tokenize_function, batched=True)

small_train_dataset = train_mixed.shuffle(seed=42).take(100)# .select(range(1000))
small_eval_dataset = val_mixed.shuffle(seed=42).take(20) # .select(range(1000))

tokenized_train = small_train_dataset.map(tokenize_function, batched=True)
tokenized_val = small_eval_dataset.map(tokenize_function, batched=True)


# train_loader = DataLoader(small_train_dataset)
# val_loader = DataLoader(small_eval_dataset)

# print(type(tokenized_train))
# last_item = next(iter(small_train_dataset))

# print(last_item)

# df = pd.DataFrame(next(iter(train_mixed)))
# print(len(small_train_dataset))
# print(len(small_eval_dataset))
# print(small_train_dataset.shape)
# print(small_eval_dataset.shape)
# predict(classifier, next(iter(train_mixed))['article'], next(iter(train_mixed))['abstract'])

# print("predicted: \n", summarize_text(classifier, next(iter(train_mixed))['article'], max_len=2706))
# print("--------------------------------")
# print("actual abstract: ", next(iter(train_mixed))['abstract'])

# for i in train_mixed:

#     print(i['abstract'])
#     print(i['section_names'])
#     break

# train_dataloader, encoded_train = create_dataloader(train_mixed)
# test_dataloader, encoded_test = create_dataloader(test_mixed)
# val_dataloader, encoded_val = create_dataloader(val_mixed)


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
    # train_dataset=small_train_dataset,
    # eval_dataset=small_eval_dataset,
    # train_dataset=encoded_train,
    # eval_dataset=encoded_val,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_val,
    data_collator=data_collator,
)

trainer.train()

# trainer.predict(encoded_test)

# dataset = dataset.map(tokenizer)
# torch_tokenized_dataset = tokenized_dataset.with_format("torch")
# print("dataset", dataset[0])



# result = classifier(shuffled_dataset)
# print("RESULTS")
# for r in result:
#     print(r)

# optimizer = torch.optim.AdamW(params=model.parameters(), lr=1e-5)
# for epoch in range(num_epoch):
#     dataset.set_epoch(epoch)
#     for i, batch in enumerate(tqdm(dataloader, total=5)):
#         if i == 5:
#             break
#         batch = {k: v.to(device) for k, v in batch.items()}
#         outputs = model(**batch)
#         loss = outputs[0]
#         loss.backward()
#         optimizer.step()
#         optimizer.zero_grad()
#         if i % 10 == 0:
#             print(f"loss: {loss}")

