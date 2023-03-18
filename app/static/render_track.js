var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player = document.createElement('div');
player.id = 'player';


window.onYouTubeIframeAPIReady = function() {
    document.body.appendChild(player);
    player.style.display = 'none';
    player = new YT.Player('player', {
        height: '0',
        width: '0',
        videoId: 'dQw4w9WgXcQ',
    });
}

function toggleTrack(id){
    if(player.getVideoData()['video_id'] != id){
        player.loadVideoById(id);
    }
    if(player.getPlayerState() == 1){
        player.pauseVideo();
    } else {
        player.playVideo();
    }
}