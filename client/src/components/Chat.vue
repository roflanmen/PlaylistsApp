<template>
    <div>
        <!-- fixed button to open chat -->
        <button class="chat-button" @click="show = !show">
            <img src="@/assets/img/chat-button.png">
        </button>
        <div class="chat" v-if="show">
            <div class="chat__messages">
            <div v-for="message in messages" :key="message.id" class="chat__message">
                <div class="chat__message__content">{{ message.content }}</div>
            </div>
            </div>
            <div class="chat__input">
            <input
                type="text"
                v-model="message"
                @keyup.enter="sendMessage"
                placeholder="Type your message here..."
            />
            </div>
        </div>
        <script type="application/javascript" defer src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    </div>
</template>

<script>
/* eslint-disable */
import Vue from "vue";
export default {
    name: "Chat",
    data() {
        return {
            message: "",
            messages: [],
            socket: null,
            show: false,
        };
    },
    methods: {
        sendMessage() {
            if (this.message) {
                this.socket.emit("text", this.message);
                this.message = "";
            }
        }
    },
    mounted() {
        let self = this;
        setTimeout(function(){
            self.socket = io("wss://playlists.herokuapp.com/api/chat");
            // self.socket = io("ws://localhost:8000/api/chat");
            self.socket.on('connect', function() {
                console.log('connected')
            });
            self.socket.on('message', function(data) {
                self.messages.push({
                    content: data,
                });
                try {
                    var chat__messages = document.getElementsByClassName("chat__messages")[0];
                    chat__messages.scrollTop = chat__messages.scrollHeight;
                } catch (error) {
                    // pass
                    
                }

            });
        }, 1000)
      
    },
};
</script>
