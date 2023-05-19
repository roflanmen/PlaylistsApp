<template>
    <div id="player-controls">
        <div class="control-buttons">
            <button class="control-button" id="previous" @click="previous()">
                <img src="@/assets/img/previous-button.png">
            </button>
            <button v-if="!playing" class="control-button" id="play" @click="play()">
                <img src="@/assets/img/play-button.png">
            </button>
            <button v-if="playing" class="control-button" id="pause" @click="pause()">
                <img src="@/assets/img/pause-button.png">
            </button>
            <button class="control-button" id="next" @click="next()">
                <img src="@/assets/img/next-button.png">
            </button>
            <!-- <button class="control-button" id="repeat" @click="repeat()">
                <img src="@/assets/img/repeat-button.png">
            </button> -->
        </div>

        <div class="time">
            <span class="current-time" id="current-time">{{ currentTimeFormatted }}</span>
        </div>
        <div class="progress">
            <input type="range" min="0" :max="duration" value="0" id="progress-bar" 
                   @input="seek(currentTime)" v-model="currentTime">
        </div>
        <div class="time">
            <span class="duration" id="duration">{{ durationFormatted }}</span>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Player',
    data() {
        return {
            duration: 0,
            currentTime: 0,
            player: null,
            playing: false,
            currentTrack: null,
        };
    },
    computed: {
        durationFormatted() {
            return this.formatTime(this.duration);
        },
        currentTimeFormatted() {
            return this.formatTime(this.currentTime);
        },
    },
    methods: {
        loadQueue(queue){
            this.player.cuePlaylist(queue.map((track) => track.youtube_id));
            this.player.setLoop(true);
            // this.player.playVideo(queue[0].youtube_id);
        },
        play(track){
            if (track !== undefined){
                this.player.playVideoAt(track);
            }
            this.player.playVideo();
            this.playing = true;
        },
        pause(){
            this.player.pauseVideo();
            this.playing = false;
        },
        next(){
            this.player.nextVideo();
        },
        previous(){
            this.player.previousVideo();
        },
        seek(seconds){
            this.player.seekTo(seconds);
        },
        getDuration(){
            return this.player.getDuration();
        },
        getCurrentTime(){
            return this.player.getCurrentTime();
        },
        formatTime(seconds){
            const date = new Date(0);
            date.setSeconds(Math.floor(seconds));
            return date.toISOString().substring(14, 19);
        },
    },
    created() {
        const tag = document.createElement('script');
        tag.src = 'https://www.youtube.com/iframe_api';
        const firstScriptTag = document.getElementsByTagName('script')[0];
        document.head.appendChild(tag);

        const player = document.createElement('div');
        player.id = 'player';

        const self = this;
        window.onYouTubeIframeAPIReady = function () {
            document.body.appendChild(player);
            /* eslint-disable */
            self.player = new YT.Player('player', {
            /* eslint-enable */
                playerVars: { autoplay: 0 },
                height: '1',
                width: '1',
                videoId: 'dQw4w9WgXcQ',
            });
            function onPlayerReady(event) {
                setInterval(() => {
                    if (!self.getCurrentTime()){ return; }
                    self.currentTime = self.getCurrentTime();
                    self.duration = self.getDuration();
                }, 100);
            }
            function onStateChange(event) {
                // if (event.data == -1){
                //     setTrackButtonState(null, false);
                // }
                // if (event.data == 1){
                //     currentlyPlaying = event.target.getPlaylistIndex();
                //     setTrackButtonState(event.target.getPlaylistIndex(), true);
                // }
                // if (event.data == 2 || event.data == 0){
                //     setTrackButtonState(event.target.getPlaylistIndex(), false);
                // }
            }
            self.player.addEventListener('onReady', onPlayerReady);
            self.player.addEventListener('onStateChange', onStateChange);
        };
    },
    mounted() {
        this.$root.$on('loadQueue', this.loadQueue);
        this.$root.$on('play', this.play);
        this.$root.$on('pause', this.pause);
    },
};
</script>
