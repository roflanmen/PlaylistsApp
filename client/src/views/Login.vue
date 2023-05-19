<template>
    <main>
        <h1 class="page-title">Login</h1>
        <div class="wrapper">
            <form class="login-form" @submit.stop.prevent="submit">
                <label for="username">Username:</label>
                <input type="text" id="username" class="form-input" v-model="username">
                <br>

                <label for="password">Password:</label>
                <input type="password" id="password" class="form-input" v-model="password">
                <br>

                <button class="form-button" @click.stop.prevent="submit()">Login</button>
            </form>
        </div>
    </main>
</template>

<script>
export default {
    data() {
        return {
            username: '',
            password: '',
        };
    },
    methods: {
        submit() {
            if (!this.username || !this.password) {
                return;
            }
            fetch('/api/user/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: this.username,
                    password: this.password,
                }),
            })
                .then((res) => res.json())
                .then((data) => {
                    if (data.message) {
                        alert(data.message);
                        return;
                    }
                    localStorage.setItem('token', data.token);
                    this.$emit('login');
                    this.$root.$emit('login');
                    this.$router.push({ name: 'Profile' });
                });
        },
    },
    emits: ['login'],
};
</script>
