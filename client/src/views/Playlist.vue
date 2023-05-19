<template>
    <main>
        <h1 class="page-title">{{ name }}</h1>
        <div class="wrapper">
            <h1>
                <a @click="editingPlaylist = true" v-if="isMine">Edit playlist</a><br>
                <a @click="deletePlaylist()" v-if="isMine">Delete playlist</a>
            </h1>
            <div v-if="editingPlaylist">
                <form class="edit-form">
                    <p>Playlist editing</p>
                    <label for="name">Name:</label>
                    <input type="name" class="form-input" v-model="editedName">
                    <br>

                    <label for="isPublic">Is public</label>
                    <input type="checkbox" class="form-input" v-model="isPublic">
                    <br>

                    <button type="submit" class="form-button" 
                        @click.stop.prevent="submit()">Edit</button>
                </form>
            </div>
            <track-list :tracks="tracks" :canDelete="isMine" :playlist="id"/>
        </div>
    </main>
</template>

<script>
export default {
    data() {
        return {
            name: 'Playlist',
            tracks: [],
            isMine: false,
            editingPlaylist: false,
            editedName: '',
            isPublic: false,
            id: null,
        };
    },
    created() {
        this.refreshPlaylist();
    },
    methods: {
        refreshPlaylist(){
            fetch(`/api/playlists/${this.$route.params.id}/`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            })
            .then((playlist) => playlist.json())
            .then((playlist) => {
                if (playlist.message){
                    alert(playlist.message);
                    this.$router.back();
                    return;
                }
                this.name = playlist.name;
                this.tracks = playlist.tracks;
                this.isPublic = playlist.is_public;
                this.editedName = playlist.name;
                this.id = playlist.id;
            });
            fetch(`/api/playlists/${this.$route.params.id}/check_ownership`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            }).then((response) => {
                if (response.status === 200){
                    this.isMine = true;
                }
            });
        },
        deletePlaylist() {
            fetch(`/api/playlists/${this.$route.params.id}/`, {
                method: 'DELETE',
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            })
            .then((response) => {
                if (response.status === 200){
                    this.$router.push('/');
                }
            });
        },
        submit() {
            this.editingPlaylist = false;
            fetch(`/api/playlists/${this.$route.params.id}/`, {
                method: 'PUT',
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: this.editedName,
                    is_public: this.isPublic,
                }),
            })
            .then((response) => {
                if (response.status === 201){
                    this.$root.$emit('login');
                    this.refreshPlaylist();
                }
            });
        },
    },
};
</script>
