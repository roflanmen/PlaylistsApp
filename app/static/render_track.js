function renderTrack(youtube_id, element_id) {
    player = new YT.Player(element_id, {
        height: '0',
        width: '0',
        videoId: youtube_id,
    });
}
var player;
window.onYouTubeIframeAPIReady = function() {
    renderTrack('dQw4w9WgXcQ', 'player');
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