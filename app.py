from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os, random
from elo import update_elo

app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb+srv://YashmitSunkara:11132008@cluster0.vjgqqbm.mongodb.net/')
db = client['whois_db']

IMAGE_FOLDER = './static/images/'

@app.route('/api/images', methods=['GET'])
def get_image_pair():
    category = request.args.get('category')
    collection = db[category]
    people = list(collection.find({}))
    if len(people) < 2:
        return jsonify({"error": "Not enough people"})
    pair = random.sample(people, 2)
    return jsonify([{ 
    "name": p['name'], 
    "image": f"/static/images/{p['filename']}" 
    } for p in pair])



@app.route('/api/vote', methods=['POST'])
def vote():
    data = request.json
    category = data['category']
    winner_name = data['winner']
    loser_name = data['loser']
    collection = db[category]

    winner = collection.find_one({'name': winner_name})
    loser = collection.find_one({'name': loser_name})
    w_elo, l_elo = update_elo(winner['elo'], loser['elo'])

    collection.update_one({'name': winner_name}, {'$set': {'elo': w_elo}, '$inc': {'wins': 1}})
    collection.update_one({'name': loser_name}, {'$set': {'elo': l_elo}, '$inc': {'losses': 1}})
    return jsonify({'success': True})

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    category = request.args.get('category')
    collection = db[category]
    board = list(collection.find({}, {'_id': 0}))
    board.sort(key=lambda x: x['elo'], reverse=True)
    return jsonify(board)

if __name__ == '__main__':
    app.run(debug=True)
