<template>
  <div class="flex flex-col justify-center items-center">
    <h1 class="text-2xl font-bold bg-stone-700 rounded-md text-yellow-400 mb-4 w-fit p-2 m-4">Dashboard</h1>

    <div v-if="repositories.length > 0" class="w-full max-w-2xl">
      <h2 class="flex justify-center text-green-900 text-xl font-semibold mb-4">Your GitHub Repositories</h2>
      <ul class="space-y-2">
        <li v-for="(repo, index) in repositories.slice(0, 20)" :key="index" class="bg-stone-100 p-4 rounded-md shadow-md hover:bg-yellow-50 transition-colors">
          <a 
            :href="repo.html_url" 
            target="_blank" 
            rel="noopener noreferrer"
            class="text-green-700 hover:underline font-medium"
            @click.prevent="selectRepository(repo)"
          >
            {{ repo.name }}
          </a>
        </li>
      </ul>
    </div>
    <div v-else>
      <p class="text-2xl">No repositories found or GitHub account not linked.</p>
    </div>
  </div>
</template>

<script>
import api from '@/utils/axiosConfig'; 
import axios from 'axios';

export default {
  data() {
    return {
      repositories: [],
    };
  },
  methods: {
    async fetchGitHubRepositories() {  
      const djangoToken = localStorage.getItem('django_token'); 
      if (djangoToken) {
        try {
          const response = await api.get('api/github/repositories/', {
            headers: {
              Authorization: `Token ${djangoToken}`,
            },
          });

          const repositories_url = response.data.repositories;
          if (typeof repositories_url === 'string' && repositories_url.startsWith('http')) {
            const repositoriesResponse = await axios.get(repositories_url);
            this.repositories = repositoriesResponse.data;
          } else {
            console.error('Invalid repositories URL:', repositories_url);
          }

        } catch (error) {
          console.error('Error fetching repositories:', error);
        }
      } else {
        console.error('Django token not found. Please log in again.');
      }
    },

    async selectRepository(repo) {
      const djangoToken = localStorage.getItem('django_token'); 
      if (djangoToken) {
        try {
          await api.post('api/github/select/repositories/', {
            repoName: repo.name,
            repoUrl: repo.html_url,
          }, {
            headers: {
              Authorization: `Token ${djangoToken}`,
            },
          });
          console.log(`Repository ${repo.name} selected successfully.`);
        } catch (error) {
          console.error('Error selecting repository:', error);
        }
      }
    }
  },

  mounted() {
    this.fetchGitHubRepositories();  
  },
};
</script>
