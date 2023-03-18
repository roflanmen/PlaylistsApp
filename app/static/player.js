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
};

function toggleTrack(id) {
    player.setVolume(40);
    if (player.getVideoData().video_id !== id) {
        player.loadVideoById(id);
    }
    if (player.getPlayerState() === 1) {
        player.pauseVideo();
    } else {
        player.playVideo();
    }
}
