import torch
from transformers import BertJapaneseTokenizer, BertForSequenceClassification
import torch.nn.functional as F

def judgement(txt):
    # 日本語の事前学習モデル
    MODEL_NAME = 'tohoku-nlp/bert-base-japanese-whole-word-masking'

    tokenizer = BertJapaneseTokenizer.from_pretrained(MODEL_NAME)
    bert_sc = BertForSequenceClassification.from_pretrained('./model_transformers')

    # データの符号化
    encoding = tokenizer(
        txt,
        padding='longest',
        return_tensors='pt'
    )

    # トークンをデコードして、別の変数に保存
    decoded_text = tokenizer.decode(encoding["input_ids"][0], clean_up_tokenization_spaces=True)

    # モデルによる分類スコアの取得
    with torch.no_grad():
        output = bert_sc(**encoding)
    score = output.logits  # 分類スコア

    # ソフトマックスを適用して確率を計算
    probabilities = F.softmax(score, dim=1)

    # 最も高い確率のクラスを予測
    predicted_class = torch.argmax(probabilities, dim=1)

    if predicted_class == 0:
        result1 = f"テキスト：{txt}\nこれはラノベらしい文章です。\nラノベらしさ: {probabilities[0][0].item() * 100:.2f}%"
        return result1
    else:
        result2 = f"テキスト：{txt}\nこれはラノベらしくありません。\nラノベらしさ: {probabilities[0][0].item() * 100:.2f}%"
        return result2