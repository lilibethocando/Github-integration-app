import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import gAuthPlugin from 'vue3-google-oauth2'
import './index.css'

// Font Awesome core
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faGithub } from '@fortawesome/free-brands-svg-icons';

library.add(faGithub);

const app = createApp(App)

app.component('font-awesome-icon', FontAwesomeIcon);

const gAuthOptions = {
    clientId: import.meta.env.VITE_GOOGLE_CLIENT_ID,
    scope: 'email profile',
    prompt: 'consent',
    fetch_basic_profile: true
}

app.use(gAuthPlugin, gAuthOptions)
app.use(router)
app.mount('#app')
