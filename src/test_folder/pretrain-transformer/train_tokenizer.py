import os
import argparse
import pandas as pd
from tqdm.auto import tqdm
from tokenizers import BertWordPieceTokenizer
from tokenizers import ByteLevelBPETokenizer, SentencePieceBPETokenizer

parser = argparse.ArgumentParser(description='Create Tokenizers for a dataset')
parser.add_argument('--dataset', '-d', type=str, help='Path to dataset', required=True)
parser.add_argument('--min_freq', '-m', type=str, help='Minimum frequency of a token', required=False, default=2)
args = parser.parse_args()
print(args)

DATASET_PATH = args.dataset
MIN_FREQ = args.min_freq
df = pd.read_csv(DATASET_PATH)

translation = list(df["translation"].values)
transliteration = list(df["transliteration"].values)
combined = translation + transliteration

if not os.path.isdir("tokenizer_data"):
  os.makedirs("tokenizer_data")
  os.makedirs("tokenizer_data/translation")
  os.makedirs("tokenizer_data/transliteration")
  os.makedirs("tokenizer_data/combined")

for i in tqdm(df.shape[0]):
  translation_text = translation[i].strip()
  transliteration_text = transliteration[i].strip()
  with open(f"tokenizer_data/translation/{i}.txt", 'w') as f1, open(f"tokenizer_data/combined/{i}{i}.txt", 'w') as f2:
    f1.write(translation_text)
    f2.write(translation_text)
  with open(f"tokenizer_data/transliteration/{i}.txt", 'w') as f1, open(f"tokenizer_data/combined/{i}{i}.txt", 'w') as f2:
    f1.write(transliteration_text)
    f2.write(transliteration_text)

translation_path = [f"tokenizer_data/translation/{f}" for f in tqdm(os.listdir("tokenizer_data/translation"))]
transliteration_path = [f"tokenizer_data/transliteration/{f}" for f in tqdm(os.listdir("tokenizer_data/transliteration"))]
combined_path = [f"tokenizer_data/combined/{f}" for f in tqdm(os.listdir("tokenizer_data/combined"))]

sent_tokenizer = SentencePieceBPETokenizer()
word_tokenizer = BertWordPieceTokenizer()
byte_tokenizer = ByteLevelBPETokenizer()

sent_tokenizer.train(files=transliteration_path, min_frequency=MIN_FREQ, 
                                  special_tokens=['<s>', '<pad>', '</s>', '<unk>', '<mask>'], show_progress=True)

word_tokenizer.train(files=transliteration_path, min_frequency=MIN_FREQ, 
                                  special_tokens=["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"], show_progress=True)

byte_tokenizer.train(files=transliteration_path, min_frequency=MIN_FREQ, 
                                  special_tokens=['<s>', '<pad>', '</s>', '<unk>', '<mask>'], show_progress=True)

os.mkdir("../models/tokenizer/sentenceTokenizer")
os.mkdir("../models/tokenizer/wordTokenizer")
os.mkdir("../models/tokenizer/BPETokenizer")

sent_tokenizer.save_model("../models/tokenizer/sentenceTokenizer")
word_tokenizer.save_model("../models/tokenizer/wordTokenizer")
byte_tokenizer.save_model("../models/tokenizer/BPETokenizer")

sent_tokenizer_comb = SentencePieceBPETokenizer()
word_tokenizer_comb = BertWordPieceTokenizer()
byte_tokenizer_comb = ByteLevelBPETokenizer()

sent_tokenizer_comb.train(files=combined_path, min_frequency=MIN_FREQ, 
                                  special_tokens=['<s>', '<pad>', '</s>', '<unk>', '<mask>'], show_progress=True)

word_tokenizer_comb.train(files=combined_path, min_frequency=MIN_FREQ, 
                                  special_tokens=["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"], show_progress=True)

byte_tokenizer_comb.train(files=combined_path, min_frequency=MIN_FREQ, 
                                  special_tokens=['<s>', '<pad>', '</s>', '<unk>', '<mask>'], show_progress=True)

os.mkdir("../models/tokenizer/sentenceTokenizer_combined")
os.mkdir("../models/tokenizer/wordTokenizer_combined")
os.mkdir("../models/tokenizer/BPETokenizer_combined")

sent_tokenizer_comb.save_model("../models/tokenizer/sentenceTokenizer_combined")
word_tokenizer_comb.save_model("../models/tokenizer/wordTokenizer_combined")
byte_tokenizer_comb.save_model("../models/tokenizer/BPETokenizer_combined")