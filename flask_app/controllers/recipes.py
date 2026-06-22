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

    try:
        response = requests.get(url, params=params, timeout=8)

        print("YouTube status code:", response.status_code)

        if response.status_code != 200:
            print("YouTube response:", response.text)
            return []

        data = response.json()
        videos = []

        for item in data.get("items", []):
            snippet = item.get("snippet", {})
            thumbnails = snippet.get("thumbnails", {})
            medium_thumbnail = thumbnails.get("medium", {})

            video_id = item.get("id", {}).get("videoId")

            if not video_id:
                continue

            videos.append({
                "title": snippet.get("title", "Untitled Video"),
                "description": snippet.get("description", ""),
                "thumbnail": medium_thumbnail.get("url", ""),
                "video_id": video_id
            })

        return videos

    except requests.RequestException as e:
        print("YouTube API error:", e)
        return []


@app.route('/new')
def new():
    if 'user_id' not in session:
        return redirect('/')

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

    if not one_recipe:
        flash("Recipe not found.", "recipe")
        return redirect('/dashboard')

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
        return redirect('/')

    user_data = {
        'id': session['user_id']
    }

    data = {
        'id': id
    }

    one_recipe = recipe.Recipe.get_recipe_id(data)

    if not one_recipe:
        flash("Recipe not found.", "recipe")
        return redirect('/dashboard')

    return render_template(
        'edit.html',
        user=user.User.get_id(user_data),
        recipe=one_recipe
    )


@app.route('/update', methods=['POST'])
def update():
    if 'user_id' not in session:
        return redirect('/')

    recipe_id = request.form.get('id')

    if not recipe_id:
        flash("Recipe ID is missing.", "recipe")
        return redirect('/dashboard')

    if not recipe.Recipe.validate_recipe(request.form):
        return redirect(url_for("edit_recipe", id=recipe_id))

    data = {
        "id": recipe_id,
        "name": request.form.get("name", "").strip(),
        "description": request.form.get("description", "").strip(),
        "instructions": request.form.get("instructions", "").strip(),
        "date": request.form.get("date", ""),
        "under30": request.form.get("under30", "0")
    }

    recipe.Recipe.edit_recipe(data)

    return redirect('/dashboard')


@app.route('/add_recipe', methods=['POST'])
def newrecipe():
    if 'user_id' not in session:
        return redirect('/')

    if not recipe.Recipe.validate_recipe(request.form):
        return redirect('/new')

    data = {
        "name": request.form.get("name", "").strip(),
        "description": request.form.get("description", "").strip(),
        "instructions": request.form.get("instructions", "").strip(),
        "date": request.form.get("date", ""),
        "under30": request.form.get("under30", "0"),
        "user_id": session['user_id']
    }

    recipe.Recipe.save_recipe(data)

    return redirect('/dashboard')


@app.route('/delete/<int:id>')
def destroy(id):
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "id": id
    }

    recipe.Recipe.delete_recipe(data)

    return redirect('/dashboard')