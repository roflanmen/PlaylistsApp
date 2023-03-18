// const params = new URLSearchParams(window.location.search);
// let user = window.fetch("/api/user/" + params.get('id'))
window.fetch('/api/user/1')
    .then((user) => user.json())
    .then((user) => {
        document.getElementsByClassName('username')[0].innerHTML = user.username;
        user.playlists.forEach((playlist) => {
            const playlistDiv = document.createElement('div');
            playlistDiv.className = 'playlist';
            playlistDiv.innerHTML = `
                <a href="/playlist.html?id=${playlist.id}"><p>${playlist.name}<p></a>
            `;
            document.getElementById('wrapper').appendChild(playlistDiv);
        });
    });
