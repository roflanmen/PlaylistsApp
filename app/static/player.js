const tag = document.createElement('script');
tag.src = 'https://www.youtube.com/iframe_api';
const firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

let player = document.createElement('div');
player.id = 'player';

window.onYouTubeIframeAPIReady = function () {
    document.body.appendChild(player);
    player = new YT.Player('player', {
        height: '1',
        width: '1',
        videoId: 'dQw4w9WgXcQ',
    });
    setInterval(() => {
        let bar = document.getElementById('progress-bar');
        if (bar !== document.activeElement) {
            let value = player.getCurrentTime()/player.getDuration() * 1000;
            if (value){
                bar.value = value;
            }
        }

        let date = new Date(0);
        date.setSeconds(Math.floor(player.getCurrentTime()));
        let time = date.toISOString().substring(14, 19);

        document.getElementById('current-time').innerHTML = time;
    }, 100);
    document.getElementById('progress-bar').onchange = function () {
        player.seekTo(player.getDuration() * this.value / 1000);
        document.getElementById('progress-bar').blur();
    }
};

function toggleTrack(id = null) {
    document.getElementById('player-controls').style.display = 'flex';
    player.setVolume(40);
    if (player.getVideoData().video_id !== id && id) {
        player.loadVideoById(id);
        setTimeout(() => {
            let date = new Date(0);
            date.setSeconds(Math.floor(player.getDuration()));
            let time = date.toISOString().substring(14, 19);

            document.getElementById('progress-bar').value = 0;
            document.getElementById('current-time').innerHTML = '00:00';
            document.getElementById('duration').innerHTML = time;

        }, 1000);
    }
    if (player.getPlayerState() === 1) {
        player.pauseVideo();
    } else {
        player.playVideo();
    }
}
