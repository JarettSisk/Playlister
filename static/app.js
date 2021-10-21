
// Elements
let songList = document.querySelector('.song-list');
const addSongForm = document.querySelector("#add-song-form");

function createSongDom(title, artist, id) {
    const songLi = document.createElement('li');
    songLi.classList.add('song');
    songLi.setAttribute('id', id);

    const removeBtnForm = document.createElement('form');
    removeBtnForm.setAttribute('method', 'POST');

    const removeBtn = document.createElement('button');
    removeBtn.classList.add('remove');
    removeBtn.innerText = 'X';
    removeBtn.setAttribute('type', 'submit');

    

    // Add listener to the new remove btn
    removeBtnForm.addEventListener("submit", async function(e) {
        e.preventDefault()
        await axios.post(`${currentLocation.pathname}/remove`, {
            song_id: id,
            })
          .then(function (response) {
            console.log(response);
          })
          .catch(function (error) {
            console.log(error);
          });
        appendSongs();
        removeBtnForm.parentElement.remove();
      })

    songLi.innerText = `${title} - ${artist}`;
    removeBtnForm.appendChild(removeBtn);
    songLi.appendChild(removeBtnForm);
    

    return songLi;

}








var currentLocation = window.location;
console.log(currentLocation.pathname);

// Create the list of songs for this playlist
async function appendSongs() {
    songList.innerHTML = "";
    try {
        const response = await axios.get(`${currentLocation.pathname}/songs`);
        songs = response.data.songs;
        console.log(songs);
        for(song of songs) {
            songEl = createSongDom(song.title, song.artist, song.id)
            songList.append(songEl);
        }
    } catch (error) {
        console.error(error);
    }
}
// initial call
appendSongs()

// Add new song
addSongForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    await axios.post(`${currentLocation.pathname}/add`, {
        title: e.target.title.value,
        artist: e.target.artist.value
        })
      .then(function (response) {
        console.log(response);
        songEl = createSongDom(response.data.title, response.data.artist, response.data.song_id);
        songList.appendChild(songEl)
      })
      .catch(function (error) {
        console.log(error);
      });
    songEl = createSongDom
    this.reset();
})