<template>
    <div class="flex flex-col justify-center items-center w-full h-screen">
        <div class="text-2xl font-bold">Proceed to click on the link below, you will be redirected to a Github page for authorization</div>
        <div class="border border-green-900 rounded-lg bg-green-700 text-white text-2xl m-4 p-4">
            <button @click="loginWithGitHub" class="flex items-center space-x-2">
                <!-- GitHub Icon -->
                <font-awesome-icon :icon="['fab', 'github']" />
                <!-- Button text-->
                <span>Link GitHub Account</span>
            </button>
        </div>
    </div>
</template>


<script setup>

const clientId = import.meta.env.VITE_GITHUB_CLIENT_ID;
const redirectUri = 'http://localhost:5173/callback';

const loginWithGitHub = () => {
    window.location.href = `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&scope=user`;
    const code = new URLSearchParams(window.location.search).get('code');
};

</script>