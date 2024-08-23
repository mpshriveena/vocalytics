<template>
    <div class="colour" style="background-color: rgb(236, 213, 255);">
      <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
          <router-link class="navbar-brand" to="/">Vocalytics</router-link>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav me-auto">
              <li class="nav-item" v-if="userRole">
              <router-link class="nav-link active" aria-current="page" to="/home">Home</router-link>
            </li>
              <li class="nav-item" v-if="userRole === 'user'">
                <router-link class="nav-link active" aria-current="page" to="/history">History</router-link>
              </li>
              <li class="nav-item" v-if="userRole === 'admin'">
                <router-link class="nav-link active" aria-current="page" to="/alltranscripts">All Transcripts</router-link>
              </li>
              <li class="nav-item" v-if="userRole === 'user'">
                <router-link class="nav-link active" aria-current="page" to="/insights">Insights</router-link>
              </li>
              <li class="nav-item" v-if="userRole === 'admin'">
                <router-link class="nav-link active" aria-current="page" to="/admininsights">Insights</router-link>
              </li>
             
              <li class="nav-item">
                <router-link class="nav-link active" aria-current="page" to="/about">About</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link active" aria-current="page" to="/contact">Contact</router-link>
              </li>
              <li class="nav-item" v-if="userRole">
              <button class="nav-link" @click="logout">Logout</button>
            </li>
            
            </ul>
          </div>
        </div>
      </nav>
    </div>
  </template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification';

export default {
    setup() {
    const toast = useToast();

    return {
      toast
    };
  },
  computed: {
    userRole() {
      const userInfo = localStorage.getItem('user_info');
      if (userInfo) {
        const user = JSON.parse(userInfo);
        console.log('User role:', user.role.name);
        return user.role.name;
      }
      return null;
    }
  },
  methods: {
    logout() {
      const accesstoken = localStorage.getItem("access_token");
      this.$axios.post('http://127.0.0.1:5000/logout', null, {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
      .then(() => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_info');
        this.$router.push('/').then(() => {
        window.location.reload();
        this.toast.success("Logged out successfully!!");
      });
      })
      .catch(error => {
        console.log('logout failed', error);
      });
    },
  }
}
</script>


