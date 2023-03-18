let params = new URLSearchParams(window.location.search);
let res = window.fetch("/api/search/tracks/?query=" + params.get('query'))
    .then(res => res.json())
    .then(res => {
        res.forEach(track => {
            if (!track) {return};
            let trackDiv = document.createElement('div');
            trackDiv.className = "song";
            trackDiv.innerHTML = `
                <button class="play-button" onclick="toggleTrack('${track.youtube_id}')"><img src="play-button.png"></button>
                <p>${track.title}<p>
            `;
            document.getElementById('tracks').appendChild(trackDiv);
        });
    })
