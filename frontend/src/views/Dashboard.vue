<template>
  <div class="flex flex-col justify-center items-center">
    <h1 class="text-2xl font-bold bg-stone-700 rounded-md text-yellow-400 mb-4 w-fit p-2 m-4">Dashboard</h1>


    <div v-if="repositories.length > 0">
      <h2>Your GitHub Repositories</h2>
      <ul>
        <li v-for="repo in repositories" :key="repo.id">
          {{ repo.name }}
          <button @click="selectRepository(repo.name)">Select</button>
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

export default {
  data() {
    return {
      repositories: [],
    };
  },
  methods: {
    async fetchRepositories() {
      try {
        const response = await api.get('/api/github/repositories/');
        this.repositories = response.data;
      } catch (error) {
        console.error('Error fetching repositories:', error);
        this.repositories = [];
      }
    },

    async selectRepository(repoName) {
      try {
        const response = await api.post('/api/github/select-repo/', {
          repoName: repoName,
        });
        alert(response.data.message);
      } catch (error) {
        console.error('Error selecting repository:', error);
      }
    },
  },

  mounted() {
    this.fetchRepositories();
  },
};
</script>
