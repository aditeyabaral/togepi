import os
import nltk
import random
import argparse
import platform
import pandas as pd
from pathlib import Path
from tqdm.auto import tqdm
from itertools import dropwhile
from collections import Counter
from transformers import AutoModel
from torch.utils.data import DataLoader
from sentence_transformers.losses import CosineSimilarityLoss, ContrastiveLoss, OnlineContrastiveLoss
from sentence_transformers import SentenceTransformer, InputExample, models, evaluation

try:
    nltk.data.find('tokenizers/punkt')
except LookupError: 
    nltk.download('punkt')
from nltk.tokenize import word_tokenize

parser = argparse.ArgumentParser(description='Siamese pre-train an existing Transformer model')
parser.add_argument('--model', '-m', type=str, help='Transformer model name/path to siamese pre-train', required=True)
parser.add_argument('--dataset', '-d', type=str, help='Path to dataset in required format', required=True)
parser.add_argument('--hub', '-hf', type=bool, help='Push model to HuggingFace Hub', required=False, default=False)
parser.add_argument('--loss', '-l', type=str, help='Loss function to use -- cosine, contrastive or online_contrastive', required=False, default='contrastive')
parser.add_argument('--batch_size', '-b', type=int, help='Batch size', required=False, default=8)
parser.add_argument('--min_count', '-mc', type=int, help='Minimum frequency for a new token to be added to the Transformer', required=False, default=5)
parser.add_argument('--evaluator', '-v', type=bool, help='Evaluate as you train', required=False, default=False)
parser.add_argument('--evaluator_examples', '-ee', type=int, help='Number of examples to evaluate', required=False, default=1000)
parser.add_argument('--epochs', '-e', type=int, help='Number of epochs', required=False, default=20)
parser.add_argument('--sample_negative', '-s', type=bool, help='Sample negative examples', required=False, default=True)
parser.add_argument('--sample_size', '-ss', type=int, help='Number of negative examples to sample', required=False, default=2)
parser.add_argument('--username', '-u', type=str, help='Username for HuggingFace Hub', required=False)
parser.add_argument('--password', '-p', type=str, help='Password for HuggingFace Hub', required=False)
parser.add_argument('--output', '-o', type=str, help='Output directory path', required=False, default='saved_models/')
parser.add_argument('--hub_name', '-hn', type=str, help='Name of the model in the HuggingFace Hub', required=False)
args = parser.parse_args()
print(args)

MODEL_NAME = args.model
DATASET_PATH = args.dataset
PUSH_TO_HUB = args.hub
LOSS_FUNCTION = args.loss
EPOCHS = args.epochs
BATCH_SIZE = args.batch_size
MIN_COUNT = args.min_count
EVALUATE_AS_YOU_TRAIN = args.evaluator
EVALUATOR_EXAMPLES = args.evaluator_examples
USERNAME = args.username
PASSWORD = args.password
OUTPUT_PATH = args.output
HUB_NAME = args.hub_name
SAMPLE_NEGATIVE = args.sample_negative
NEGATIVE_SAMPLE_SIZE = args.sample_size


if PUSH_TO_HUB is not None and PUSH_TO_HUB:
  if USERNAME is None or PASSWORD is None:
    print("Please provide username and password for pushing to HuggingFace Hub!\nRun the script with python pretrain_transformer.py -h for help.")
    exit()
  else:
    print("Logging into HuggingFace Hub!")
    if platform.system() == "Linux":
      os.system(f"printf '{USERNAME}\{PASSWORD}' | transformers-cli login")
    else:
      print("Could not login to HuggingFace Hub automatically! Please enter credentials again")
      os.system("transformers-cli login")

if DATASET_PATH.endswith('.csv'):
  df = pd.read_csv(DATASET_PATH)
elif DATASET_PATH.endswith('.pickle'):
  df = pd.read_pickle(DATASET_PATH)
translation = list(df["translation"].values)
transliteration = list(df["transliteration"].values)
labels = [1.0 for _ in range(df.shape[0])]

tokens = list()
for sentence in tqdm(translation + transliteration):
  words = word_tokenize(sentence.lower())
  tokens.extend(words)
token_counter = Counter(tokens)
for key, count in dropwhile(lambda key_count: key_count[1] >= MIN_COUNT, token_counter.most_common()):
  del token_counter[key]
tokens = list(token_counter.keys())
total_tokens = len(tokens)

random.seed(0)
if SAMPLE_NEGATIVE:
  collection = list(zip(translation, transliteration))
  new_collection = list()
  for c in tqdm(random.sample(collection, int(0.5 * df.shape[0]))):
    translation_c = c[0]
    transliteration_c = c[1]
    new_collection.append((translation_c, transliteration_c, 1.0))

    sampled = False
    while not sampled:
      transliteration_c_sampled = random.sample(transliteration, NEGATIVE_SAMPLE_SIZE)
      if transliteration_c in transliteration_c_sampled:
        continue
      else:
        sampled = True
    for s in transliteration_c_sampled:
      new_collection.append((translation_c, s, 0.0)) # for cosine find similarity

    sampled = False
    while not sampled:
      translation_c_sampled = random.sample(translation, NEGATIVE_SAMPLE_SIZE)
      if translation_c in translation_c_sampled:
        continue
      else:
        sampled = True
    for s in translation_c_sampled:
      new_collection.append((s, translation_c_sampled, 0.0)) # for cosine find similarity

  translation, transliteration, labels = zip(*new_collection)

total_examples = len(translation)
train_examples = list()
for i in range(total_examples):
  if isinstance(transliteration[i], list):
    tl = transliteration[i][0]
  else:
    tl = transliteration[i]
  train_examples.append(InputExample(texts=[translation[i], tl], label=labels[i]))
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=BATCH_SIZE)

word_embedding_model = models.Transformer(MODEL_NAME)
word_embedding_model.training = True
try:
  for b in range(0, total_tokens, 1000):
    word_embedding_model.tokenizer.add_tokens(tokens[b:b+1000], special_tokens=True)
  word_embedding_model.auto_model.resize_token_embeddings(len(word_embedding_model.tokenizer))
except:
  word_embedding_model.auto_model.resize_token_embeddings(len(word_embedding_model.tokenizer))
pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())

if LOSS_FUNCTION == 'cosine':
  loss_function = CosineSimilarityLoss
elif LOSS_FUNCTION == 'contrastive':
  loss_function = ContrastiveLoss
elif LOSS_FUNCTION == 'online_contrastive':
  loss_function = OnlineContrastiveLoss
else:
  print("Loss function not supported! Defaulting to cosine.")
  loss_function = ContrastiveLoss

model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
train_loss = loss_function(model)

if EVALUATE_AS_YOU_TRAIN:
  evaluator_examples = random.sample(list(zip(translation, transliteration, labels), EVALUATOR_EXAMPLES))
  evaluator_examples_translation = [example[0] for example in evaluator_examples]
  evaluator_examples_transliteration = [example[1] for example in evaluator_examples]
  evaluator_examples_labels = [example[2] for example in evaluator_examples]
  evaluator = evaluation.EmbeddingSimilarityEvaluator(evaluator_examples_translation, evaluator_examples_transliteration, evaluator_examples_labels)
  model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=EPOCHS, warmup_steps=100, evaluator=evaluator, evaluation_steps=1000, save_best_model=True)
else:
  model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=EPOCHS, warmup_steps=100)

if not Path(OUTPUT_PATH).exists():
  Path(OUTPUT_PATH).mkdir(parents=True)

model.save(f"{OUTPUT_PATH}/{MODEL_NAME}")
word_embedding_model.save(f"{OUTPUT_PATH}/{MODEL_NAME}_TRANSFORMER")

if PUSH_TO_HUB is not None and PUSH_TO_HUB:
  print("Pushing to HuggingFace Hub!")
  word_embedding_model_hub = AutoModel.from_pretrained(f"{OUTPUT_PATH}/{MODEL_NAME}_TRANSFORMER")
  word_embedding_model_hub.push_to_hub(HUB_NAME)
  word_embedding_model.tokenizer.push_to_hub(HUB_NAME)
  model.save_to_hub(f"sentencetransformer-{HUB_NAME}")
  del model, word_embedding_model, word_embedding_model_hub, pooling_model