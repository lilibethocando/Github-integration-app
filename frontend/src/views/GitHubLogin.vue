<template>
    <div class="flex flex-col justify-center items-center w-full h-screen">
        <div class="text-2xl font-bold">Proceed to click on the link below, you will be redirected to a Github page for authorization</div>
        <div class="border border-green-900 rounded-lg bg-green-700 text-white text-2xl m-4 p-4">
            
            <button @click="redirectToGithub" class="flex items-center space-x-2">
                <!-- GitHub Icon -->
                <font-awesome-icon :icon="['fab', 'github']" />
                <!-- Button text-->
                <span>Link GitHub Account</span>
            </button>
        </div>
    </div>
</template>


<script setup>
const redirectToGithub = () => {
    window.location.href = 'http://127.0.0.1:8000/api/github/login/';
};
</script>