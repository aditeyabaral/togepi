import os
import torch
import platform
import argparse
import pandas as pd
from tqdm.auto import tqdm
from transformers import AdamW
from transformers import RobertaConfig, BertConfig, DistilBertConfig
from transformers import BertForMaskedLM, RobertaForMaskedLM, DistilBertForMaskedLM
from transformers import RobertaTokenizerFast, BertTokenizerFast, DistilBertTokenizerFast

parser = argparse.ArgumentParser(description='Pre-train a Transformer model from scratch')
parser.add_argument('--model', '-m', type=str, help='Model to train', required=True)
parser.add_argument('--dataset', '-d', type=str, help='Path to dataset', required=True, default="../data/dataset.csv")
parser.add_argument('--hub', '-hf', type=bool, help='Push model to HuggingFace Hub', required=False, default=False)
parser.add_argument('--username', '-u', type=str, help='Username for HuggingFace Hub', required=False)
parser.add_argument('--password', '-p', type=str, help='Password for HuggingFace Hub', required=False)
args = parser.parse_args()

MODEL_NAME = args.model
PUSH_TO_HUB = args.hub
USERNAME = args.username
PASSWORD = args.password
DATASET_PATH = args.dataset

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

df = pd.read_csv(DATASET_PATH)
print(df.shape)

translation = list(df['translation'].values)
transliteration = list(df['transliteration'].values)
combined = translation + transliteration

model_map = {
    "BERT": [BertForMaskedLM, BertTokenizerFast, BertConfig],
    "DistilBERT": [DistilBertForMaskedLM, DistilBertTokenizerFast, DistilBertConfig],
    "RoBERTa": [RobertaForMaskedLM, RobertaTokenizerFast, RobertaConfig]
}

tokenizer_model_map = {
    "BERT": "wordTokenizer",
    "DistilBERT": "wordTokenizer",
    "RoBERTa": "BPETokenizer"
}

def load_tokenizer(model_name):
  if model_name not in tokenizer_model_map:
    print("Invalid model name!")
    return None
  tok = tokenizer_model_map[model_name]
  Tok1 = model_map[model_name][1]
  path_to_tokenizer = f"../models/tokenizer/tokenizer/{tok}"
  path_to_combined = path_to_tokenizer + "_combined"
  Tokenizer = Tok1.from_pretrained(path_to_tokenizer, max_len = 128)
  Tokenizer_combined = Tok1.from_pretrained(path_to_combined, max_len = 128)
  if "GPT" in model_name:
    Tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    Tokenizer_combined.add_special_tokens({'pad_token': '[PAD]'})
  return Tokenizer, Tokenizer_combined

class Dataset(torch.utils.data.Dataset):
    def __init__(self, encodings):
        # store encodings internally
        self.encodings = encodings

    def __len__(self):
        # return the number of samples
        return self.encodings['input_ids'].shape[0]

    def __getitem__(self, i):
        # return dictionary of input_ids, attention_mask, and labels for index i
        return {key: tensor[i] for key, tensor in self.encodings.items()}

def get_encodings(Tokenizer):
  batch = Tokenizer(transliteration, max_length=128, padding=True, truncation=True, return_tensors="pt")
  labels = torch.tensor(batch['input_ids'])
  mask = torch.tensor(batch['attention_mask'])

  # make copy of labels tensor, this will be input_ids
  input_ids = labels.detach().clone()
  # create random array of floats with equal dims to input_ids
  rand = torch.rand(input_ids.shape)
  # mask random 15% where token is not 0 [PAD], 1 [CLS], or 2 [SEP]
  mask_arr = (rand < .15) * (input_ids != 0) * (input_ids != 1) * (input_ids != 2)
  # loop through each row in input_ids tensor (cannot do in parallel)
  for i in range(input_ids.shape[0]):
      # get indices of mask positions from mask array
      selection = torch.flatten(mask_arr[i].nonzero()).tolist()
      # mask input_ids
      input_ids[i, selection] = 3  # our custom [MASK] token == 3
  encodings = {'input_ids': input_ids, 'attention_mask': mask, 'labels': labels}
  return encodings

def preTrain(Tokenizer):
  encodings = get_encodings(Tokenizer)
  dataset = Dataset(encodings)
  loader = torch.utils.data.DataLoader(dataset, batch_size=16, shuffle=True)
  model_objs = model_map[MODEL_NAME]
  model_obj = model_objs[0]
  config_obj = model_objs[2]
  config = config_obj(
    max_position_embeddings=514,
    hidden_size=768,
    num_attention_heads=12,
    num_hidden_layers=6
  )
  model = model_obj(config)
  device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
  # and move our model over to the selected device
  model.to(device)
  # activate training mode
  model.train()
  # initialize optimizer
  optim = AdamW(model.parameters(), lr=1e-4)

  epochs = 15
  for epoch in range(epochs):
      # setup loop with TQDM and dataloader
      loop = tqdm(loader, leave=True)
      for batch in loop:
          # initialize calculated gradients (from prev step)
          optim.zero_grad()
          # pull all tensor batches required for training
          input_ids = batch['input_ids'].to(device)
          attention_mask = batch['attention_mask'].to(device)
          labels = batch['labels'].to(device)
          # process
          outputs = model(input_ids, attention_mask=attention_mask,
                          labels=labels)
          # extract loss
          loss = outputs.loss
          # calculate loss for every parameter that needs grad update
          loss.backward()
          # update parameters
          optim.step()
          # print relevant info to progress bar
          loop.set_description(f'Epoch {epoch}')
          loop.set_postfix(loss=loss.item())
  return model

def trainModel(model_name):
  Tokenizer, Tokenizer_combined = load_tokenizer(model_name)
  
  print(f"Training {model_name} transliterated!")
  model_transliteration = preTrain(Tokenizer)

  if PUSH_TO_HUB is not None and PUSH_TO_HUB:
    model_transliteration.push_to_hub(f"{model_name.lower()}-hinglish-small")
    Tokenizer.push_to_hub(f"{model_name.lower()}-hinglish-small")
  del model_transliteration
  del Tokenizer
  
  print(f"Training {model_name} combined!")
  model_combined = preTrain(Tokenizer_combined)

  if PUSH_TO_HUB is not None and PUSH_TO_HUB:
    model_combined.push_to_hub(f"{model_name.lower()}-hinglish-big")
    Tokenizer_combined.push_to_hub(f"{model_name.lower()}-hinglish-big")
  del model_combined
  del Tokenizer_combined

trainModel(MODEL_NAME)

