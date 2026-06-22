from flask_app import app 
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models import recipe
from flask_app.models import user

import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

def get_youtube_videos(search_term):
    api_key = os.getenv("YOUTUBE_API_KEY", "").strip()

    if not api_key:
        print("Missing YouTube API key")
        return []

    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": search_term,
        "type": "video",
        "maxResults": 4,
        "key": api_key
    }

    response = requests.get(url, params=params)

    print("YouTube status code:", response.status_code)
    print("YouTube response:", response.text)

    if response.status_code != 200:
        return []

    data = response.json()
    videos = []

    for item in data.get("items", []):
        videos.append({
            "title": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
            "video_id": item["id"]["videoId"]
        })

    return videos

@app.route('/new')
def new():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('new.html')

@app.route('/recipe/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/')

    user_data = {
        'id': session['user_id']
    }

    data = {
        'id': id
    }

    one_recipe = recipe.Recipe.get_recipe_id(data)

    youtube_videos = get_youtube_videos(one_recipe.name + " recipe")

    return render_template(
        'recipes.html',
        user=user.User.get_id(user_data),
        recipe=one_recipe,
        youtube_videos=youtube_videos
    )


@app.route('/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        'id' : session['user_id']
    }
    data = {
        'id' : id
    }
    return render_template('edit.html', user=user.User.get_id(user_data), recipe=recipe.Recipe.get_recipe_id(data))

@app.route('/update', methods=['POST'])
def update():
    if 'user_id' not in session:
        return redirect('/logout')

    if not recipe.Recipe.validate_recipe(request.form):
        return redirect(url_for("edit_recipe", id=request.form['id']))

    data = {
        "id": request.form["id"],
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date": request.form["date"],
        "under30": request.form.get("under30")
    }

    recipe.Recipe.edit_recipe(data)

    return redirect('/dashboard')


@app.route('/add_recipe', methods=['POST'])
def newrecipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect('/new')

    data = {
        "name" : request.form['name'],
        "description" : request.form['description'],
        "instructions" : request.form['instructions'],
        "date" : request.form['date'],
        "under30" : request.form['under30'],
        "user_id": session['user_id']
    }
    recipe.Recipe.save_recipe(data)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def destroy(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id" : id
    }
    recipe.Recipe.delete_recipe(data)
    return redirect('/dashboard')
