from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample playlists with songs and album art
playlists = [
    {
        'id': 1,
        'name': 'Beach Vibes',
        'genre': 'Chill',
        'album_art': 'album1.jpg',
        'songs': [
            {'title': 'Sunset Melody', 'artist': 'Wave Riders'},
            {'title': 'Ocean Breeze', 'artist': 'Sandy Tunes'},
        ],
    },
    {
        'id': 2,
        'name': 'Workout Pump',
        'genre': 'Fitness',
        'album_art': 'album2.jpg',
        'songs': [
            {'title': 'Energy Boost', 'artist': 'Gym Beats'},
        ],
    },
]

def get_playlist(pid):
    return next((p for p in playlists if p['id'] == pid), None)

@app.route('/')
def home():
    return redirect(url_for('list_playlists'))

@app.route('/playlists/')
def list_playlists():
    genre = request.args.get('genre')
    if genre:
        filtered = [p for p in playlists if p['genre'].lower() == genre.lower()]
    else:
        filtered = playlists
    genres = sorted({p['genre'] for p in playlists})
    return render_template('playlists.html', playlists=filtered, genres=genres, selected_genre=genre)

@app.route('/playlist/<int:playlist_id>/', methods=['GET', 'POST'])
def playlist_detail(playlist_id):
    playlist = get_playlist(playlist_id)
    if not playlist:
        return "Playlist not found", 404

    if request.method == 'POST':
        title = request.form.get('title')
        artist = request.form.get('artist')
        if title and artist:
            playlist['songs'].append({'title': title, 'artist': artist})
            return redirect(url_for('playlist_detail', playlist_id=playlist_id))

    return render_template('playlist.html', playlist=playlist)

if __name__ == '__main__':
    app.run(debug=True)
