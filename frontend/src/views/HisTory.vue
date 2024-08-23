<template>
  <div class="body">
    <section class="vh-100">
      <div class="container py-5 h-200">
        <div class="row d-flex justify-content-center align-items-center h-100">
          <div class="col col-lg-14 col-xl-12">
            <div class="card rounded-3">
              <div class="card-body p-4">
                <h4 class="text-center my-3 pb-3"><strong>History of Transcripts</strong></h4>
                <form id="searchform" class="d-flex ms-auto" method="post" @submit.prevent="searchFunction">
            <select class="form-select me-2" id="field" name="field" aria-label="Default select example" v-model="field">
              <option value="transcription" selected>Transcription</option>
              <option value="language">Detected Language</option>
            </select>
            <input type="text" id="search" name="search" class="form-control me-2" placeholder="Search" v-model="search" />
            <button type="submit" class="button" @click="searchFunction">Search</button>
          </form>
                <p>Here are the words you transcribed so far..</p>
                <table class="table mb-4">
                  <thead>
                    <tr>
                      <th scope="col">Transcription({{mytranscriptions.length}})</th>
                      <th scope="col">Detected Language</th>
                      <th scope="col">Transcribed On</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="mytranscription in mytranscriptions" :key="mytranscription.id">
                      <td>{{ mytranscription.transcription }}</td>
                      <td>{{ mytranscription.detected_language }}</td>
                      <td>{{ mytranscription.date_created }}</td>
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
      mytranscriptions: [],
      user_id: JSON.parse(localStorage.getItem('user_info')).user_id,
      field:'',
      search:''
    };
  },
  mounted() {
    this.getmyTranscriptions();
  },
  methods: {
    getmyTranscriptions(){
      const accesstoken = localStorage.getItem("access_token");
      axios.get('http://127.0.0.1:5000/mytranscriptions/', {
        params: {
          user_id: this.user_id,
        },
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
        .then(response => {
          this.mytranscriptions = response.data.mytranscriptions;
        })
        .catch(error => {
          console.error('Error found', error);
        });
    },
    searchFunction() {
      const user_id = JSON.parse(localStorage.getItem('user_info')).user_id;
      const accesstoken = localStorage.getItem("access_token");
      axios.post('http://127.0.0.1:5000/search', {
        field: this.field,
        search: this.search,
        user_id: user_id
      },
        {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
      .then(response => {
        sessionStorage.setItem('searchResults', JSON.stringify(response.data));
        this.$router.go(0);
        this.$router.push({ path: `/searchresults` });
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
#searchform {
  display: flex;
  align-items: center;
}
.button{
    width:200px;
    height:38px;
    background: rgb(255, 255, 255);
    border:none;
    outline:none;
    color:rgb(0, 0, 0);
    border-radius: 4px;
    cursor:pointer;
    font-weight:500;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  }
  .button:hover{
    background: rgb(0, 0, 0);
    color:rgb(255, 255, 255);

  }
  h4{
    color:rgb(1, 4, 161);
  }
</style>