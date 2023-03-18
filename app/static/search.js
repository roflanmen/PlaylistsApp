const params = new URLSearchParams(window.location.search);
window.fetch(`/api/search/tracks/?query=${params.get('query')}`)
    .then((tracks) => tracks.json())
    .then((tracks) => {
        tracks.forEach((track) => {
            if (!track) { return; }
            const trackDiv = document.createElement('div');
            trackDiv.className = 'song';
            trackDiv.innerHTML = `
                <button class="control-button" onclick="toggleTrack('${track.youtube_id}')"><img src="play-button.png"></button>
                <p>${track.title}<p>
            `;
            document.getElementById('tracks').appendChild(trackDiv);
        });
    });
window.fetch(`/api/search/playlists/?query=${params.get('query')}`)
    .then((playlists) => playlists.json())
    .then((playlists) => {
        playlists.forEach((playlist) => {
            if (!playlist) { return; }
            const playlistDiv = document.createElement('div');
            playlistDiv.className = 'playlist';
            playlistDiv.innerHTML = `
                <a href="/playlist.html?id=${playlist.id}"><p>${playlist.name}<p></a><br>
            `;
            document.getElementById('playlists').appendChild(playlistDiv);
        });
    });
window.fetch(`/api/search/users/?query=${params.get('query')}`)
    .then((users) => users.json())
    .then((users) => {
        users.forEach((user) => {
            if (!user) { return; }
            const userDiv = document.createElement('div');
            userDiv.className = 'username';
            userDiv.innerHTML = `
                <a href="/profile.html?id=${user.id}"><p>${user.username}<p></a>
            `;
            document.getElementById('users').appendChild(userDiv);
        });
    });
