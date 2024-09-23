<template>
  <div>
    <router-view></router-view>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/utils/axiosConfig';

const isLoggedIn = ref(false);
const githubLinked = ref(false);
const router = useRouter();

const handleCredentialResponse = async (response) => {
    console.log("Google Token:", response.credential);
    localStorage.setItem('google_token', response.credential);
    isLoggedIn.value = true;

    try {
        const djangoResponse = await api.post('api/auth/google/', {
          id_token: response.credential,
        });

        if (djangoResponse.data.token) {
            localStorage.setItem('django_token', djangoResponse.data.token); 
            console.log('Django token saved:', djangoResponse.data.token);
            router.push('/callback'); 
        } else {
            console.error('No Django token returned:', djangoResponse.data);
            router.push('/login');
        }
    } catch (error) {
        console.error('Error getting Django token:', error);
        router.push('/login');
    }
};


onMounted(() => {
  window.google.accounts.id.initialize({
    client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
    callback: handleCredentialResponse,
  });

  const googleButton = document.getElementById('googleSignInButton');
  if (googleButton) {
    window.google.accounts.id.renderButton(googleButton, {
      theme: 'outline',
      size: 'medium',
    });
  } else {
    console.error("Google Sign-In button element not found.");
  }
});
</script>
