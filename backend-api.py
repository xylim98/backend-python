import flask
from flask import request, jsonify
from urllib.request import urlopen
import json
import pandas as pd
from marshmallow import Schema, fields


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>TribeHired Backend Test</h1><p>Build a REST API to return the Top Post and create a Search API</p>"

class ObjectSchema(Schema):
    post_id = fields.Str()
    post_title = fields.Str()
    post_body = fields.Str()
    total_number_of_comments = fields.Str()

@app.route('/top-comment', methods=['GET'])
def top_comment():
    df = pd.read_json("https://jsonplaceholder.typicode.com/comments")
    total_comment = df.groupby(['postId']).size().reset_index(name='total_comment').sort_values(by=['total_comment'], ascending=False).reset_index(drop=True)
    post = pd.read_json(f"https://jsonplaceholder.typicode.com/posts")
    my_dict = []

    for index,row in total_comment.iterrows():
        tmp_dict = {'post_id':row['postId'], 'post_title':post.loc[post['id'] == row['postId'], 'title'].values[0],'post_body':post.loc[post['id'] == row['postId'], 'body'].values[0],'total_number_of_comments':row['total_comment']}
        my_dict.append(tmp_dict)

    object_schema = ObjectSchema()
    json_string = object_schema.dumps(my_dict, many=True)

    return jsonify(json.loads(json_string))

@app.route('/search', methods=['GET'])
def search():
    comments = urlopen("https://jsonplaceholder.typicode.com/comments")
    data_json = json.loads(comments.read())

    id = int(request.args.get('id',0))
    postId = int(request.args.get('postId',0))
    name = request.args.get('name', '')
    email = request.args.get('email','')
    body = request.args.get('body','')
    body = body.replace('\\n','')
    results = []

    for comment in data_json:
        if (id == comment['id'] if id != 0 else True) and (postId == comment['postId'] if postId != 0 else True) and (name == comment['name'] if name != '' else True) and (email == comment['email'] if email != '' else True) and (body == comment['body'].replace('\n','') if body != '' else True):
            results.append(comment)

    return jsonify(results)

app.run()