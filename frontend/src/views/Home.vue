<template>
  <div v-if="!isLoggedIn" class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8 flex flex-col justify-center items-center">
    <h2 class="text-2xl font-bold bg-stone-700 rounded-md text-yellow-400 mb-4 w-fit p-2">Welcome to GitHub Integration
      App</h2>
    <p class="p-4 text-gray-600">Please login to start using the application.</p>
    <div id="googleSignInButton"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/utils/axiosConfig';

const isLoggedIn = ref(false);
const router = useRouter();

onMounted(async () => {
  if (document.getElementById('googleSignInButton') && !isLoggedIn.value) {
    window.google.accounts.id.initialize({
      client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
      callback: async (response) => {
        console.log("Google Token:", response.credential);
        try {
          const djangoResponse = await api.post('api/auth/google-oauth2/', {
            id_token: response.credential,
            backend: 'google-oauth2' 
          });

          router.push('/login');

        } catch (error) {
          console.error('Error getting Django token:', error);
        }
      },
    });

    window.google.accounts.id.renderButton(
      document.getElementById('googleSignInButton'),
      { theme: 'outline', size: 'medium' }
    );
  }
});

</script>
