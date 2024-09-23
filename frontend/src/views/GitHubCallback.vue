<template>
    <div>
        <p>Handling GitHub Callback...</p>
    </div>
</template>

<script>
import api from '@/utils/axiosConfig';
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';

export default {
    setup() {
        const router = useRouter();

        const handleGitHubCallback = async () => {
            const code = new URLSearchParams(window.location.search).get('code');

            if (code) {
                try {
                    console.log('GitHub authorization code:', code);
                    console.log('Exchanging code for token...');

                    const response = await api.post('/api/github/oauth/', {
                        code,
                    });
                    const { access_token } = response.data;

                    if (access_token) {
                        localStorage.setItem('django_token', access_token);
                        console.log('Token de GitHub guardado en localStorage:', access_token);

                        const userResponse = await api.get('https://api.github.com/user', {
                            headers: {
                                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                            },
                        });

                        const userInfo = userResponse.data;
                        console.log('GitHub user info:', userInfo);


                        const djangoToken = localStorage.getItem('django_token'); 

                        await api.post('/api/store/github/user/', {

                            access_token: access_token,
                            github_username: userInfo.login,
                        }, {
                            headers: {
                                Authorization: `Token ${djangoToken}`, 
                            },
                        });

                        router.push('/dashboard');
                    } else {
                        console.error('Could not obtain GitHub token:', response.data);
                        router.push('/login');
                    }
                } catch (error) {
                    console.error('Could not obtain GitHub token:', error);
                    router.push('/login');
                }
            } else {
                console.error('Authorization code not found in GitHub URL');
                router.push('/login');
            }
        };

        onMounted(() => {
            handleGitHubCallback();
        });
    },
};
</script>
