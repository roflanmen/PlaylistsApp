<template>
    <main>
        <h1 class="page-title">Edit user</h1>
        <div class="wrapper">
            <form class="edit-form">

                <label for="password">Password:</label>
                <input type="password" class="form-input" v-model="password">
                <br>

                <label for="username">Username (if you want to change):</label>
                <input type="text" class="form-input" v-model="username">
                <br>

                <label for="new-password">New password (if you want to change):</label>
                <input type="password" class="form-input" v-model="newPassword">
                <br>

                <label for="confirm-password">Confirm new password:</label>
                <input type="password" class="form-input" v-model="newPasswordConfirm">
                <br>

                <button type="submit" class="form-button" 
                        @click.stop.prevent="submit()">Edit</button>
            </form>
        </div>
    </main>
</template>

<script>
export default {
    data(){
        return {
            username: '',
            password: '',
            newPassword: '',
            newPasswordConfirm: '',
        };
    },
    methods: {
        submit() {
            if (!this.password) { return; }
            const body = {
                password: this.password,
            };
            if (this.username) {
                body.username = this.username;
            }
            if (this.newPassword && this.newPassword === this.newPasswordConfirm) {
                body.new_password = this.newPassword;
            }
            fetch('/api/user/', {
                method: 'PUT',
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
                    this.$router.push({ name: 'Profile' });
                });
        },
    },
};
</script>
