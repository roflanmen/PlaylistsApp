<template>
  <div id="app">
    <header class="main-header">
        <div class="logo-name">
          <img src="@/assets/img/favicon.png" alt="Logo" class="logo">
          <h1>Playlists</h1>
        </div>
      <form class="search-form" @submit.stop.prevent="submit">
        <input type="text" name="query" placeholder="Search..." 
               class="search-input" required v-model="searchQuery">
        <button class="search-button" @click.stop.prevent="submitSearch()">Search</button>
      </form>
      <nav class="header-nav">
        <ul>
          <li v-if="!logged"><router-link to="/register">Register</router-link></li>
          <li v-if="!logged"><router-link to="/login">Login</router-link></li>
          <li v-if="logged"><a @click="logout">Logout</a></li>
          <li v-if="logged"><router-link to="/profile">Profile</router-link></li>
        </ul>
      </nav>
    </header>
    <h3 class="error-message">{{ error }}</h3>
    <router-view @login="logged = true" @logout="logout()"/>
    <div class="modal-add-to-playlist" v-if="addingToPlaylist">
        <div class="modal-content">
            <button @click="addingToPlaylist = false">Close</button>
            <p>Add to playlist</p>
            <label for="playlist">Choose playlist:</label>
            <select name="playlist" id="" v-model="chosenPlaylist">
                <option :value="playlist.id" 
                        v-for="(playlist,index) in playlists" 
                        :key="index">
                        {{ playlist.name }}
                </option>
            </select>
            <button type="submit" class="form-button" 
                @click.stop.prevent="submitAddToPlaylist()">Add</button>
        </div>
    </div>
    <chat />
    <player />
  </div>
</template>

<script>
import Vue from 'vue';
import Player from './components/Player.vue';
import TrackList from './components/TrackList.vue';
import Chat from './components/Chat.vue';

Vue.component('TrackList', TrackList);

export default {
    name: 'App',
    data() {
        return {
            searchQuery: '',
            logged: false,
            playlists: [],
            addingToPlaylist: false,
            chosenPlaylist: null,
            track: null,
            error: '',
        };
    },
    methods: {
        submitSearch() {
            if (!this.searchQuery) {
                return;
            }
            this.$router.push({ name: 'Search', params: { query: this.searchQuery } });
        },
        submitAddToPlaylist(){
            this.addingToPlaylist = false;
            const url = `/api/playlists/${this.chosenPlaylist}/tracks/`;
            this.chosenPlaylist = this.playlists[0].id;
            this.error = '';
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
                body: JSON.stringify({
                    youtube_id: this.track.youtube_id,
                }),
            })
            .then((response) => {
                if (response.status === 201) {
                    this.track = null;
                } else {
                    const self = this;
                    setTimeout(() => {
                        self.error = '';
                    }, 1500);
                }
                return response.json();
            })
            .then((data) => {
                if (data.message){
                    this.error = `Error adding to playlist: ${data.message}`;
                }
            });
        },
        logout() {
            localStorage.removeItem('token');
            this.logged = false;
            this.$router.push({ name: 'Login' });
        },
        addToPlaylist(track) {
            this.addingToPlaylist = true;
            this.track = track;
        },
        refreshUser(){
            fetch('/api/user/', {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            })
            .then((response) => {
                if (response.status === 200){
                    this.logged = true;
                  } else {
                    localStorage.removeItem('token');
                    this.$router.push({ name: 'Login' });
                }
            });
            fetch('/api/user/', {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            })
            .then((response) => response.json())
            .then((data) => {
                this.playlists = data.playlists;
                this.chosenPlaylist = this.playlists[0].id;
            });
        },
    },
    created() {
        this.refreshUser();
    },
    components: {
        Player,
        Chat,
    },
    mounted() {
        this.$root.$on('addToPlaylist', this.addToPlaylist);
        this.$root.$on('login', this.refreshUser);
    },
};
</script>

<style lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap');
$primary-color: #6b30a9;
$primary-color-light: #a456cc;
$background-color: #0d0c15;
$background-color-light: #1b1729;
$input-border-color: #ffffff;
$font-color: rgb(234, 234, 234);
$transparent: rgba(#000000,0);
$input-background-color: #1b1729;
$input-border-radius: 5px;
$form-margin: 20px;
$form-padding: 5px;
$form-border: 1px solid $input-border-color;
$error-color: #ff0000;

$font-family: 'Roboto', sans-serif;
$control-button-size: 35px;

html, body {
  margin: 0;
  min-height: 100vh;
  background-color: $background-color-light;
  color: $font-color;
  font-family: $font-family;

  a, a:visited, button{
    color: $font-color;
    text-decoration: none;
  }

  button {
    background-color: $transparent;
  }
  input, textarea, select {
    background-color: $input-background-color;
    color: $font-color;
  }
}
// Mixins
@mixin button-style {
  padding: 5px 10px;
  border: none;
  border-radius: $input-border-radius;
  cursor: pointer;

  font-family: $font-family;

  transition: all 0.2s ease-in-out;
  &:hover {
    color: $primary-color-light;
  }
}

@mixin form-style {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: $form-margin;
  border: 2px solid $input-border-color;
  border-radius: $input-border-radius;
  padding: 10px;
}

@mixin control-button-text-style {
  margin-block-start: 0.5em;
  margin-block-end: 0.5em;
  margin-left: 5px;
}

// Main Header styles

.main-header {
  display: flex;
  justify-content: space-between;
  flex-direction: row;
  align-items: center;
  padding: 15px;
  padding-left: 30px;
  background-color: $background-color;
  font-family: $font-family;

  .logo {
    height: 50px;
    margin-right: 20px;
  }

  @media screen and (max-width: 960px) {
    flex-direction: column;
    > * {
      margin: 15px;
    }
  }

  .logo-name {
    display: flex;
    justify-content: center;
    align-items: center;
  }
}
.search-form {
  display: flex;
  align-items: center;
  margin-left: 20px;

  .search-button {
    @include button-style;
  }
  input {
    padding: $form-padding;
    border-radius: $input-border-radius;
    border: none;
    margin-right: 5px;
  }
}

.header-nav {
  ul {
    list-style: none;
    display: flex;
    margin: 0;
    padding: 0;
  }
  li {
    margin: 0 10px;
  }
  a {
    @include button-style;
    text-decoration: none;
  }
}
// Form styles
.register-form, .login-form, .edit-form {
  @include form-style;

  .form-input {
    padding: $form-padding;
    border-radius: $input-border-radius;
    border: $form-border;
    margin-bottom: 10px;
    width: 100%;
    max-width: 300px;
  }

  .form-button {
    @include button-style;
  }
}

// Page title styles
.page-title {
  text-align: center;
  margin: 20px;
}

.register-button:hover,
.login-button:hover,
.profile-button:hover {
  background-color: $primary-color-light;
}
main {
  color: $font-color;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  font-family: $font-family;

  .wrapper {
    display: flex;
    justify-content: left;
    align-items: left;
    flex-direction: column;
    width: 80%;
    max-width: 1100px;
    padding: 10px 25px;
    border-radius: 5px;
    background-color: $background-color;
  }
}


.song{
  display: flex;
  align-items: left;
  flex-direction: row;
  margin: 5px;
  border: $form-border;
  border-radius: $input-border-radius;
  padding: 5px;
  p{
    @include control-button-text-style;
  }
}
.control-button {
  border-radius: 100%;
  border: none;
  width: $control-button-size;
  height: $control-button-size;
  position: relative;
  transition: all 0.5s ease-in-out;
  img {
    width: 70%;
    height: 70%;
    position: absolute;
    top: 50%;
    left: 50%;
    margin: -35%;
  }
  opacity: 0.7;
  &:hover {
    cursor: pointer;
    opacity: 1;
  }
}

.playlist p{
    @include control-button-text-style;
}
.control-buttons{
  display: flex;
  flex-direction: row;
  margin: 15px;
  div{
    display: flex;
    flex-direction: row;
  }
}

#player-controls{
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  bottom: 0;
  width: 100%;
  height: 11%;
  background-color: $background-color;
  div{
    display: flex;
    flex-direction: row;
  }
  .progress{
    width: 55%;
    margin: 0 10px;
  }
  #progress-bar{
    -webkit-transition: .2s; /* 0.2 seconds transition on hover */
    transition: opacity .2s;
    width: 100%;
  }
}

.modal-add-to-playlist{
    z-index: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    position: fixed;
    left: 50%;
    top: 50%;
    margin: -10%;
    width: 20%;
    background-color: $background-color;
    .modal-content{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      width: 100%;
      height: 100%;
      border: $form-border;
      border-radius: $input-border-radius;
      padding-left: 10px;
        padding-right: 10px;
      input{
        width: 100%;
        max-width: 200px;
      }
      button{
        margin: 5px;
      }
    }
}

.error-message{
  color: $error-color;
  margin: 0;
  padding: 0;
  text-align: center;
}

.chat {
    position: fixed;
    bottom: 11%;
    right: calc(5% + 50px);
    width: 300px;
    height: 200px;
    background-color: $background-color-light;
    border-radius: 5px;
    border: $background-color 3px solid;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.chat__messages {
    width: 100%;
    height: calc(100% - 1em - 3px);
    overflow-y: scroll;
}
.chat__messages::-webkit-scrollbar {
    width: 12px;
}

.chat__messages::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3); 
    border-radius: 10px;
}

.chat__messages::-webkit-scrollbar-thumb {
    border-radius: 10px;
    border: $background-color 1px solid;
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.5); 
}
.chat__message {
    margin: 3px;
    border-radius: 5px;
    border: $background-color 1px solid;
    color: $font-color;
}
.chat__input {
    position: absolute;
    bottom: 0;
    width: 97%;
    input {
      width: 100%;
    }
    
}

.chat-button{
  position: fixed;
  bottom: 11%;
  right: 5%;
  width: 50px;
  height: 50px;
  border-radius: 100%;
  border: none;
  background-color: $background-color;
  img{
    max-width: 100%;
    max-height: 100%;
  }
}
</style>
