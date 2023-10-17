from fastapi.testclient import TestClient
from main import Song, app

client = TestClient(app)

# Clear the songs list before running tests
app.songs = []

def test_add_song():
    response = client.post("/add-song/", json={
        "title": "Test Song",
        "artist": "Test Artist",
        "genre": "Test Genre",
        "album": "Test Album",
        "year_of_release": "2023",
        "duration": 180,
        "description": "This is a test song."
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Song added successfully"}

def test_list_songs():
    response = client.get("/list-songs/")
    assert response.status_code == 200
    assert response.json() == {"songs": [app.songs[0].__dict__]}

def test_delete_song():
    response = client.delete("/delete-song/0/")
    assert response.status_code == 200
    assert response.json() == {"message": f"Song '{app.songs[0].title}' by {app.songs[0].artist} deleted successfully"}

def test_update_song():
    app.songs.append(Song(title="Old Title", artist="Old Artist"))
    response = client.put("/songs/0", json={"title": "New Title", "artist": "New Artist"})
    assert response.status_code == 200
    assert response.json() == {"message": "Song updated", "updated_song": app.songs[0].__dict__}