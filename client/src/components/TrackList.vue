<template>
    <div class="playlist" id="playlist">
        <div class="song" v-for="(track, index) in tracks" :key="index">
            <button v-if="!playing[index]" class="control-button" 
                    @click="play(index)">
                <img src="@/assets/img/play-button.png">
            </button>
            <button v-if="playing[index]" class="control-button" 
                    @click="pause()">
                <img src="@/assets/img/pause-button.png">
            </button>
            <button class="control-button" 
                    @click="addToPlaylist(track)">
                <img src="@/assets/img/add-to-playlist.png">
            </button>
            <button class="control-button" 
                    @click="deleteFromPlaylist(track)"
                    v-if="canDelete">
                <img src="@/assets/img/delete-button.png">
            </button>
            <p>{{track.title}}</p>
        </div>
    </div>
</template>

<script>

export default {
    props: ['tracks', 'canDelete', 'playlist'],
    data() {
        return {
            playing: [],
            loaded: false,
        };
    },
    methods: {
        play(track){
            if (!this.loaded){
                this.$root.$emit('loadQueue', this.tracks);
                this.loaded = true;
            }
            
            this.$root.$emit('play', track);
            for (let i = 0; i < this.tracks.length; i += 1){
                this.playing.splice(i, 1, false);
            }
            this.playing.splice(track, 1, true);
        },
        pause(){
            this.$root.$emit('pause');
            for (let i = 0; i < this.tracks.length; i += 1){
                this.playing.splice(i, 1, false);
            }
        },
        addToPlaylist(track){
            this.$root.$emit('addToPlaylist', track);
        },
        deleteFromPlaylist(track){
            fetch(`/api/playlists/${this.playlist}/tracks/${track.youtube_id}/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            })
            .then((response) => {
                this.tracks.splice(this.tracks.indexOf(track), 1);
            });
        },
    },
    watch: {
        tracks(){
            this.playing = [];
            for (let i = 0; i < this.tracks.length; i += 1){
                this.playing.push(false);
            }
            this.loaded = false;
        },
    },
};
</script>
