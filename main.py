from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn


app = FastAPI()

songs =[]

# Model for a song
class Song(BaseModel):
    def __init__(self, title: str, artist: str):
        self.title = title
        self.artist = artist

# Create a new song
@app.post("/add-song/")
def add_song(title: str, artist: str, genre: str, album: str, year_of_release: str, duration: int, description: str):
    new_song = Song(title=title, artist=artist, genre=genre, album=album, year_of_release=year_of_release, duration=duration, description=description)
    songs.append(new_song)
    return {"message": "Song added successfully"}

# List all songs
@app.get("/list-songs/")
def list_songs():
    return {"songs": [song.__dict__ for song in songs]}

# Delete a song by its index
@app.delete("/delete-song/{song_index}/")
def delete_song(song_index: int):
    if song_index < 0 or song_index >= len(songs):
        raise HTTPException(status_code=404, detail="Song not found")
    
    deleted_song = songs.pop(song_index)
    return {"message": f"Song '{deleted_song.title}' by {deleted_song.artist} deleted successfully"}

@app.put("/songs/{song_index}", response_model=Song)
def update_song(song_index: int, song: Song):
    if 0 <= song_index < len(songs):
        updated_song = song.dict()
        songs[song_index].update(updated_song)
        return {"message": "Song updated", "updated_song": songs[song_index]}
    else:
        return {"message": "Song not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# class Song(BaseModel):
#     title: str
#     artist: str

# # @app.get("/")
# # async def root():
# #     return {"message": "Hello World"}

# @app.post("/add-song/")
# async def add_song(song: Song):
#     songs_db.append(song)
#     return {"message": "Song added successfully"}

# @app.get("/list-songs/")
# async def list_songs():
#     return {"songs":songs_db}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
