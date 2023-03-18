const params = new URLSearchParams(window.location.search);
window.fetch(`/api/playlists/${params.get('id')}`)
    .then((res) => res.json())
    .then((res) => {
        document.getElementsByClassName('page-title')[0].innerHTML = res.name;
        res.tracks.forEach((track) => {
            if (!track) { return; }
            const trackDiv = document.createElement('div');
            trackDiv.className = 'song';
            trackDiv.innerHTML = `
                <button class="control-button" onclick="toggleTrack('${track.youtube_id}')"><img src="play-button.png"></button>
                <p>${track.title}<p>
            `;
            document.getElementById('playlist').appendChild(trackDiv);
        });
    });
