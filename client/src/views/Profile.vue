<template>
    <main>
        <h1 class="page-title">Profile
            <router-link to="/editprofile" v-if="ownProfile">Edit </router-link>
            <a href="" @click.prevent.stop="deleteUser" 
               v-if="ownProfile || iAdmin">Delete </a>
            <a @click="creatingPlaylist = true" v-if="ownProfile">Create playlist</a>
        </h1>
        
        <div class="wrapper" id="wrapper">
            <div v-if="creatingPlaylist">
                <form class="edit-form">
                    <p>Playlist creation</p>
                    <label for="name">Name:</label>
                    <input type="name" class="form-input" v-model="name">
                    <br>

                    <label for="isPublic">Is public</label>
                    <input type="checkbox" class="form-input" v-model="isPublic">
                    <br>

                    <button type="submit" class="form-button" 
                            @click.stop.prevent="submit()">Create</button>
                    </form>
            </div>
            <p><span class="username">{{ role + " " + username }}</span></p>
            <h2 class="block-name">Playlists:</h2>
            <router-link v-for="playlist in playlists" :key="playlist.id"
                         :to="'/playlist/' + playlist.id">
                <p>{{ playlist.name }}</p>
            </router-link>
        </div>
    </main>
</template>

<script>
export default {
    data() {
        return {
            role: '',
            username: '',
            playlists: [],
            id: null,
            ownProfile: false,
            iAdmin: false,
            creatingPlaylist: false,
            name: '',
            isPublic: false,
        };
    },
    created() {
        this.refreshUser();
    },
    methods: {
        refreshUser(){
            let url = '/api/user/';
            const params = {};
            this.ownProfile = true;
            if (this.$route.params.id){
                url += this.$route.params.id;
                this.ownProfile = false;
            }
            if (localStorage.getItem('token')){
                params.headers = {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                };
            }
            fetch(url, params)
            .then((user) => user.json())
            .then((user) => {
                if (user.message){
                    alert(user.message);
                    this.$router.push('/');
                    return;
                }
                this.id = user.id;
                this.username = user.username;
                this.role = user.is_admin ? 'Admin' : 'User';
                this.playlists = user.playlists;
            });
            if (localStorage.getItem('token')){
                fetch('/api/user', {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`,
                    },
                })
                .then((user) => user.json())
                .then((user) => {
                    if (user.id === this.id){
                        this.ownProfile = true;
                    }
                    this.iAdmin = user.is_admin;
                });
            }
        },
        deleteUser(){
            let url = '/api/user/';
            if (this.$route.params.id){
                url += this.$route.params.id;
            }
            fetch(url, {
                method: 'DELETE',
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            })
            .then((res) => res.json())
            .then((res) => {
                if (res.message === 'User deleted'){
                    if (this.$route.params.id === undefined){
                        localStorage.removeItem('token');
                        this.$emit('logout');
                    }
                    this.$router.push('/');
                } else {
                    alert(res.message);
                }
            });
        },
        submit() {
            if (!this.name) { return; }
            const body = {
                name: this.name,
                is_public: this.isPublic,
            };
            fetch('/api/playlists/', {
                method: 'POST',
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(body),
            })
                .then((res) => res.json())
                .then((data) => {
                    if (data.message) {
                        alert(data.message);
                        return;
                    }
                    this.creatingPlaylist = false;
                    this.refreshUser();
                });
        },
    },
    emits: ['logout'],
};
</script>
