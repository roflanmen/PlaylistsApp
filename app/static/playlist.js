const params = new URLSearchParams(window.location.search);
window.fetch(`/api/playlists/${params.get('id')}`)
    .then((res) => res.json())
    .then((res) => {
        document.getElementsByClassName('page-title')[0].innerHTML = res.name;
        let i = 0;
        res.tracks.forEach((track) => {
            if (!track) { return; }
            const trackDiv = document.createElement('div');
            trackDiv.className = 'song';
            trackDiv.innerHTML = `
                <button class="control-button" onclick="toggleTrack('${i}')"><img src="play-button.png"></button>
                <p>${track.title}<p>
            `;
            document.getElementById('playlist').appendChild(trackDiv);
            tracksJson.push(track);
            i++;
        });
        makeQueue();
    });
