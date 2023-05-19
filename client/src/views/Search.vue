<template>
    <main>
        <h1 class="page-title">Search results</h1>
        <div class="wrapper">
            <h2>Users</h2>
            <div class="search-results" id="users">
                <div class="username" v-for="user in users" :key="user.id">
                    <router-link :to="'/profile/' + user.id">
                        <p>{{ user.username }}</p>
                    </router-link>
                </div>
            </div>
            <h2>Playlists</h2>
            <div class="search-results" id="playlists">
                <div v-for="playlist in playlists" :key="playlist.id">
                    <router-link :to="'/playlist/' + playlist.id">
                        <p>{{ playlist.name }}</p>
                    </router-link>
                </div>
            </div>
            <h2>Tracks</h2>
            <track-list :tracks="tracks" :canDelete="false" :playlist="null"/>
        </div>
    </main>
</template>

<script>
export default {
    data() {
        return {
            tracks: [],
            playlists: [],
            users: [],
        };
    },
    created() {
        this.search();
    },
    methods: {
        search(){
            fetch(`/api/search/tracks/?query=${this.$route.params.query}`, {})
            .then((tracks) => tracks.json())
            .then((tracks) => {
                this.tracks = tracks;
            });
            const opts = {};
            if (localStorage.getItem('token')){
                opts.headers = {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                };
            }
            fetch(`/api/search/playlists/?query=${this.$route.params.query}`, opts)
            .then((playlists) => playlists.json())
            .then((playlists) => {
                this.playlists = playlists;
            });
            fetch(`/api/search/users/?query=${this.$route.params.query}`, {})
            .then((users) => users.json())
            .then((users) => {
                this.users = users;
            });
        },
    },
    watch: {
        $route(to, from){
            this.search();
        },
    },
};
</script>
