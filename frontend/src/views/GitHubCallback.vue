<template>
    <div>
        <p>Handling GitHub Callback...</p>
    </div>
</template>

<script>
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';

export default {
    setup() {
        const router = useRouter();

        const handleGitHubCallback = async () => {

            const token = new URLSearchParams(window.location.search).get('token');

            if (token) {
                console.log('Received Django token:', token);

                localStorage.setItem('django_token', token);
                console.log('Django token saved:', token);

                router.push('/dashboard');
            } else {
                console.error('Token not found in URL');
                router.push('/login');
            }
        };

        onMounted(() => {
            handleGitHubCallback();
        });
    },
};
</script>
