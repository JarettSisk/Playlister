
// Elements
let songList = document.querySelector('.song-list');
const addSongForm = document.querySelector("#add-song-form");

function createSongDom(title, artist, id) {
    const songLi = document.createElement('li');
    songLi.classList.add('song');
    songLi.setAttribute('id', id);

    const removeBtnForm = document.createElement('form');
    removeBtnForm.classList.add('remove-btn-form');
    removeBtnForm.setAttribute('method', 'POST');

    const removeBtn = document.createElement('button');
    removeBtn.classList.add('remove');
    removeBtn.classList.add('hidden-print');
    removeBtn.innerText = 'X';
    removeBtn.setAttribute('type', 'submit');

    

    // Add listener to the new remove btn
    removeBtnForm.addEventListener("submit", async function(e) {
        e.preventDefault()
        await axios.post(`${currentLocation.pathname}/remove-song`, {
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
    songLi.prepend(removeBtnForm);
    

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
    
    await axios.post(`${currentLocation.pathname}/add-song`, {
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
    songPopup.innerHTML = "";
})


// input and function for dynamic search

// Get the input from the DOM
const titleInput = document.querySelector("#title");
const artistInput = document.querySelector("#artist")
songPopup = document.querySelector('.song-popup');

// Add event listener to check for changes of the input
titleInput.addEventListener('input', async function() {
 // Clear song options everytime this is ran

    // When input is changed, use axios to search the itunes api for songs that match the input
    try {
        const response = await axios.get(`https://itunes.apple.com/search?term=${encodeURI(titleInput.value)}&media?term=song&enitity=album&limit=3`);
        // Once the response comes back, append a list with the first 3 options to the dom so that they become clickable 
        songPopup.innerHTML = "";
        console.log(response.data);
        data = response.data;
        // If value not empty
        if (titleInput.value !== '') {
            // If results exist,  show them
            if (data.resultCount !== 0) {
                for(song of data.results) {
                    createDynamicSearchDom(song.trackName, song.artistName);
                }
                // Else say "no results found"
            } else {
                createDynamicSearchDom('Oops', "no results found");
            }
        }
    } catch (error) {
        console.error(error);
    }
    
})

// This will be the dom create function for the list of songs. Inside we will also need to attach event listeners to each item that will auto fill the song / artist box with the option you clicked on.
function createDynamicSearchDom(title, artist) {
    popupLi = document.createElement("li");
    popupLi.innerText = `${title} - ${artist}`;

    popupLi.addEventListener('click', function() {
        titleInput.value = title;
        artistInput.value = artist;
        songPopup.innerHTML = "";
    })

    songPopup.appendChild(popupLi);
}