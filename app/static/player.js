const tag = document.createElement('script');
tag.src = 'https://www.youtube.com/iframe_api';
const firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

let player = document.createElement('div');
player.id = 'player';
function formatTime(seconds){
    let date = new Date(0);
    date.setSeconds(Math.floor(seconds));
    return date.toISOString().substring(14, 19);
}
let tracksJson = [];

window.onYouTubeIframeAPIReady = function () {
    document.body.appendChild(player);
    player = new YT.Player('player', {
        height: '1',
        width: '1',
        videoId: 'dQw4w9WgXcQ'
    });
    function onPlayerReady(event) {
        setInterval(() => {
            let bar = document.getElementById('progress-bar');
            if (bar !== document.activeElement) {
                let value = player.getCurrentTime()/player.getDuration() * 1000;
                if (value){
                    bar.value = value;
                }
            }
            if(player.getCurrentTime()){
                document.getElementById('current-time').innerHTML = formatTime(player.getCurrentTime());
                document.getElementById('duration').innerHTML = formatTime(player.getDuration());
            }
        }, 100);
        makeQueue();
    };
    function onStateChange(event) {
        if (event.data == -1){
            setTrackButtonState(null, false);
        }
        if (event.data == 1){
            currentlyPlaying = event.target.getPlaylistIndex();
            setTrackButtonState(event.target.getPlaylistIndex(), true);
        }
        if (event.data == 2 || event.data == 0){
            setTrackButtonState(event.target.getPlaylistIndex(), false);
        }
    }
    player.addEventListener('onReady', onPlayerReady);
    player.addEventListener('onStateChange', onStateChange);
    document.getElementById('progress-bar').onchange = function () {
        player.seekTo(player.getDuration() * this.value / 1000);
        document.getElementById('progress-bar').blur();
    }
};

function toggleTrack(id = null) {
    if (id === null) {
        id = player.getPlaylistIndex();
    }
    document.getElementById('player-controls').style.display = 'flex';
    player.setVolume(40);
    if (player.getPlaylistIndex() != id) {
        console.log(id, player.getPlaylistIndex());
        player.playVideoAt(id);
    } else {
        if (player.getPlayerState() == 1) {
            player.pauseVideo();
        } else {
            player.playVideo();
        }
    }
}

let queue = [];
let currentlyPlaying = null;

let numOfEvents = 0;
function makeQueue(){
    numOfEvents++;
    if(numOfEvents < 2){ return; }
    tracks = document.getElementsByClassName('song');
    tracksJson.forEach((track) => {
        queue.push(track.youtube_id);
    });
    currentlyPlaying = 0;
    player.loadPlaylist(queue);
    player.setLoop(true);

    document.getElementById('previous').onclick = () => {  
        player.previousVideo();
    };
    document.getElementById('next').onclick = () => {
        player.nextVideo();
    }
}

function setTrackButtonState(id, play){
    if(!id){
        id = currentlyPlaying;
    }
    let tracks = document.getElementsByClassName('song');
    let track = tracks[id];
    let button = track.getElementsByClassName('control-button')[0];
    let img = button.getElementsByTagName('img')[0];
    if(play){
        img.src = 'pause-button.png';
    } else {
        img.src = 'play-button.png';
    }
    setControlPlayButtonState(play);
}

function setControlPlayButtonState(play){
    let button = document.getElementById('play');
    let img = button.getElementsByTagName('img')[0];
    if(play){
        img.src = 'pause-button.png';
    } else {
        img.src = 'play-button.png';
    }
}