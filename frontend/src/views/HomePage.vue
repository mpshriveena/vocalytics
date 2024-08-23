<template>
    <div>
      <UserHome v-if="user_info && user_info.role.name === 'user'"/>
      <AdminHome v-if="user_info && user_info.role.name === 'admin'"/>
    </div>
  </template>
  
  <script>
  import UserHome from "./UserHome.vue";
  import AdminHome from "./AdminHome.vue";
  
  export default {
    data() {
      return {
        user_info: JSON.parse(localStorage.getItem('user_info')),
        access_token: localStorage.getItem('access_token'),
      };
    },
    components: {
      UserHome,
      AdminHome,
    },
  };
  </script>
  

<style>

</style>