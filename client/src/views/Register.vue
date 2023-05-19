<template>
    <main>
        <h1 class="page-title">Register</h1>
        <div class="wrapper">
            <form class="register-form" @submit.stop.prevent="submit">
                <label for="username">Username:</label>
                <input type="text" v-model="username" class="form-input">
                <br>

                <label for="password">Password:</label>
                <input type="password" v-model="password" class="form-input">
                <br>

                <label for="confirm-password">Confirm Password:</label>
                <input type="password" v-model="confirmPassword" class="form-input">
                <br>

                <label for="role">Role:</label>
                <select id="role" v-model="role" class="form-input">
                    <option value="" disabled>Select role...</option>
                    <option value="regular">Regular</option>
                    <option value="admin">Admin</option>
                </select>
                <br>

                <button class="form-button" @click.stop.prevent="submit()">Register</button>
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
            confirmPassword: '',
            role: '',
        };
    },
    computed: {
        isAdmin() {
            return this.role === 'admin';
        },
    },
    methods: {
        submit() {
            if (!this.username 
                || !this.password 
                || this.password !== this.confirmPassword 
                || !this.role) {
                return;
            }

            fetch('/api/user/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: this.username,
                    password: this.password,
                    is_admin: this.isAdmin,
                }),
            })
            .then((res) => res.json())
            .then((data) => {
                if (data.message) {
                    alert(data.message);
                    return;
                }
                this.$router.push({ name: 'Login' });
            });
        },
    },
};
</script>
