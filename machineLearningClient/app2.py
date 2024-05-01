"""These imports are used create a flask server for the ml part  """

import os
from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import cross_origin
import openai


def predict(user_loc, openai_key):
    """Function to call openAI api and get result"""
    openai.my_api_key = openai_key
    messages = [
        {"role": "system", "content": "You are an intelligent assistant."},
        {"role": "user", "content": "Yes or no, is " + user_loc + "a geographic location?"},
    ]
    chat = openai.chat.completions.create(messages=messages, model="gpt-3.5-turbo")
    if "Yes" in chat.choices[0].message.content:
        messages = [
            {"role": "system", "content": "You are an intelligent assistant."},
            {"role": "user", "content": "List the 5 best things to do in " + user_loc},
        ]
        chat = openai.chat.completions.create(messages=messages, model="gpt-3.5-turbo")
        return chat.choices[0].message.content
    return "Not a location"

def generate_image(description, openai_key):
    """Generate an image based on description using OpenAI's DALL-E."""
    response = openai.Image.create(
        model="image-dalle-2",
        prompt=description,
        n=1,
        size="1024x1024",
        api_key=openai_key
    )
    image_url = response['data'][0]['url']  # This may vary depending on API response structure
    return image_url


def get_key():
    """Function to retreive key from environment"""
    return os.environ.get("OPENAI_API_KEY")


def init_app(db):
    """Function to run the app"""
    users = db.users
    key = get_key()
    main_app = create_app(users, key)
    main_app.run(host="0.0.0.0", port=5001)


def create_app(collection, api_key):
    """Create the app and related functions"""
    app = Flask(__name__)
    app.config["CORS_HEADERS"] = "Content-Type"

    @app.route("/ml_result", methods=["GET"])
    @cross_origin()
    def machine_learning_client():
        """Function to generate Ml Part"""
        user = collection.find_one({"name": "Test User"})
        if user:
            user_loc = "" + user["city"] + user["region"] + user["country"]
            ml_response = predict(user_loc, api_key)
            # Dump user data into JSON format
            collection.update_one(
                {"_id": user["_id"]}, {"$set": {"ml_response": ml_response}}
            )
            return jsonify({"message": "Ml Response Added"}), 200
        return jsonify({"message": "User not found"}), 404
    
    @app.route("/ml_search", methods=["GET"])
    @cross_origin()
    def search_location():
        """Function to get recommendation from a searched location"""
        loc = request.args.get('loc')
        response = predict(loc, api_key)
        return jsonify({"ml_response": response}), 200


    @app.route("/ml_sch", methods=["GET"])
    @cross_origin()
    def get_sch():
        """Function to get recommendation from a searched location"""
        sch = request.args.get('sch')


        openai.my_api_key = api_key

        messages = [
            {"role": "system", "content": "You are an intelligent assistant."},
            {"role": "user", "content": sch},
        ]
        chat = openai.chat.completions.create(messages=messages, model="gpt-3.5-turbo")
        response = chat.choices[0].message.content

        return jsonify({"ml_response": response}), 200

    return app

    @app.route('/recommend', methods=['GET'])
    def recommend():
        user_loc = request.args.get('user_loc', '')
        openai_key = os.getenv('OPENAI_API_KEY') 
        description = "Generate an artistic image of a landscape described as: " + user_loc
        image_url = generate_image(description, openai_key)
        
        return jsonify({
            'image_url': image_url
        })


if __name__ == "__main__":
    init_app(MongoClient("mongodb://mongo_db:27017/mydatabase").mydatabase)
