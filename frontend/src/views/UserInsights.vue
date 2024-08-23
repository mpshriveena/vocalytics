<template>
    <div class="body">
        <div class="body1">
            
      <section class="insights-page">
        <h3><strong>Vocalytics Insights</strong></h3>
        <br>
        <div class="container">
          <div class="row">
            <div class="col-md-4">
              <div class="table-container">
                <h5>Your Most Frequent Words</h5>
                <table class="table">
                  <thead>
                    <tr>
                      <th>Word</th>
                      <th>Frequency</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="word in frequentWords" :key="word[0]">
                      <td>{{ word[0] }}</td>
                      <td>{{ word[1] }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="col-md-4">
              <div class="table-container">
                <h5>Most Frequent Words of All Users</h5>
                <table class="table">
                  <thead>
                    <tr>
                      <th>Word</th>
                      <th>Frequency</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="word in allUsersFrequentWords" :key="word[0]">
                      <td>{{ word[0] }}</td>
                      <td>{{ word[1] }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="col-md-4">
              <div class="table-container">
                <h5>Top 3 Unique Phrases</h5>
                <table class="table">
                  <thead>
                    <tr>
                      <th>Phrase</th>
                      <th>Frequency</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="phrase in topPhrases" :key="phrase[0]">
                      <td>{{ phrase[0] }}</td>
                      <td>{{ phrase[1] }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
</div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    
    data() {
      return {
        user_id: JSON.parse(localStorage.getItem('user_info')).user_id,
        frequentWords: [],
        allUsersFrequentWords: [],
        topPhrases: [],
      };
    },
    mounted() {
      this.fetchInsights();
    },
    methods: {
      fetchInsights() {
        const accesstoken = localStorage.getItem("access_token");
  
        axios.get('http://127.0.0.1:5000/frequent-words', {
          params: { user_id: this.user_id },
          headers: { Authorization: `Bearer ${accesstoken}` }
        }).then(response => {
          this.frequentWords = response.data.most_frequent_words;
        }).catch(error => {
          console.error('Error fetching frequent words:', error);
        });
  
        axios.get('http://127.0.0.1:5000/all-users-frequent-words', {
          headers: { Authorization: `Bearer ${accesstoken}` }
        }).then(response => {
          this.allUsersFrequentWords = response.data.all_users_frequent_words;
        }).catch(error => {
          console.error('Error fetching all users frequent words:', error);
        });
  
        axios.get('http://127.0.0.1:5000/top-phrases', {
          params: { user_id: this.user_id },
          headers: { Authorization: `Bearer ${accesstoken}` }
        }).then(response => {
          this.topPhrases = response.data.top_phrases;
        }).catch(error => {
          console.error('Error fetching top phrases:', error);
        });
      }
    }
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
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;

}
.body1{
    background: rgba(255, 255, 255, 1);
    padding: 5px;
    border-radius: 10px;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
    width: 95%;
    min-height: 80vh;
    overflow: auto;
    display:column;
    column-gap: 10%;
    justify-content: center;
    align-items: center;
}
  .insights-page {
    padding: 5%;
  }
  .table-container {
    margin-bottom: 20px;
  }
  .table-container h5 {
    margin-bottom: 10px;
  }
  .table {
    width: 100%;
    margin-bottom: 0;
  }
  .table th, .table td {
    text-align: center;
  }
  .table th{
    background-color: #e2e1e1; 
    color: #333;
  }
  h3,h5{
    text-align: center;
  }
  h3{
    color:rgb(1, 4, 161);
  }
  </style>
  