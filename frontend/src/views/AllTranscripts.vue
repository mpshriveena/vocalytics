<template>
    <div class="body">
      <section class="vh-100">
        <div class="container py-5 h-200">
          <div class="row d-flex justify-content-center align-items-center h-100">
            <div class="col col-lg-14 col-xl-12">
              <div class="card rounded-3">
                <div class="card-body p-4">
                  <h4 class="text-center my-3 pb-3"><strong>History of All User Transcripts</strong></h4>
                  <p>Here are the words users transcribed so far..</p>
                  <table class="table mb-4">
                    <thead>
                      <tr>
                        <th scope="col">User ID</th>
                        <th scope="col">Transcription({{transcriptions.length}})</th>
                        <th scope="col">Detected Language</th>
                        <th scope="col">Transcribed On</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="transcription in transcriptions" :key="transcription.id">
                        <td>{{ transcription.user_id }}</td>
                        <td>{{ transcription.transcription }}</td>
                        <td>{{ transcription.detected_language }}</td>
                        <td>{{ transcription.date_created }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
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
    data() {
      return {
        transcriptions: [],
        user_id: JSON.parse(localStorage.getItem('user_info')).user_id,
      };
    },
    mounted() {
      this.getTranscriptions();
    },
    methods: {
      getTranscriptions(){
        const accesstoken = localStorage.getItem("access_token");
        axios.get('http://127.0.0.1:5000/transcriptions/', {
          params: {
            user_id: this.user_id,
          },
          headers: {
            Authorization: `Bearer ${accesstoken}`
          }
        })
          .then(response => {
            this.transcriptions = response.data.transcriptions;
          })
          .catch(error => {
            console.error('Error found', error);
          });
      },
    },
  };
  </script>
  
  <style scoped>
  * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Poppins', 'sans-serif';
  }
  .body{
    background: rgb(226, 226, 226);
      min-height: 100vh;
  }
  h4{
    color:rgb(1, 4, 161);
  }
  </style>