from flask import Flask, jsonify
import pandas as pd
import random
import os

app = Flask(__name__)

dislike_df = pd.DataFrame({'user_id':[1,1,1,1], '甘味':[1,3,3,4],'苦味':[5,3,3,4]
,'酸味':[2,3,3,4],'塩味':[2,3,3,4],'食感':[1,3,3,4],'脂質':[2,2,2,3],
'カテゴリ':['Vegetable','Meat','Rice','Vegetable']})
#アンケートは事前に勝手に作っとく
#inputはrails側でのuser_id
preference_df = pd.DataFrame(columns = ['user_id','甘味','苦味','酸味','塩味',
'食感','脂質','カテゴリ'])
preference_df = preference_df.append(dislike_df)


material_df = pd.read_csv('/Users/keresu0720/Desktop/my_flask/material.csv')
material_df = material_df[material_df['都道府県ID'] = 13]
#1...北海道
#13...東京都
#21...岐阜県
#スクリプトがあるディレクトリでにあるCSVを読み込む

def match_preference(row):
    max_similar_score = 0
    for i in range(3):
        if row[8] == preference_df.iloc[i,7]:
            similar_score = 0
            for j in range(5):
                if preference_df.iloc[i,j+1] == row[j+2]:
                    similar_score += 2
                elif abs(preference_df.iloc[i,j+1] - row[j+2]) == 1:
                    similar_score += 1
            if similar_score > max_similar_score:
                max_similar_score = similar_score
    return max_similar_score

    #マテリアルデータフレームから一致してないものを出す

@app.route("/", methods = ['POST'])
def get_material():
    suggestion_material = []
    while len(suggestion_material) < 5:
        random_material = random.randint(0,9)
        #注意：10個データをCSVで用意
        #item_idで判定
        if random_material not in suggestion_material:
            if match_preference(material_df.iloc[random_material,:]) < 6:
                suggestion_material.append(random_material)
    return jsonify({'recommendation1':suggestion_material[0],'recommendation2':suggestion_material[1],'recommendation3':suggestion_material[2],'recommendation4':suggestion_material[3],'recommendation5':suggestion_material[4]})
    #suggestion_materialはDataframeではなくリスト
    #item_idを返せば良い


if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0')
