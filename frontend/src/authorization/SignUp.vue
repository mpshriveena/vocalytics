<template>
  <div class='body'>
    <div class="inbody">
        <div class="signup-box">
        <form @submit.prevent="SignUp">
          <h1><strong>Register</strong></h1>
          <div class = "inputbox">
            <input type="text" id="username" placeholder="name" v-model="username" required>
            <label>Username</label>

          </div>
            <div class = "inputbox">
              <input type="email" id="email" placeholder="name@example.com" v-model="email" required>
              <label>Email</label>

            </div>
            <div class = "inputbox">
              <input type="password" id="password" v-model="password" required>
              <label>Password</label>
            </div>
            <button class="button" @click='SignUp'> Register </button>
            <div class="login-link">
            <p>Already have an account? <router-link to="/"><a>Login</a></router-link> </p>
          </div>
          </form>
          <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification';

export default{
  data(){
    return{
      username:'',
      email:'',
      password:'',
      role:'user',
      errorMessage:'',
    };
  },
  methods:{
    async SignUp(){
      try{
        await axios.post('http://127.0.0.1:5000/register',{
          username: this.username,
          email: this.email,
          password: this.password,
          role:this.role
        });
        this.$router.push('/');
        
      } catch(error){
        this.errorMessage = error.response.data.message
      }
    }
  }
}


</script>
<style scoped>
.body {
      margin:0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Poppins', 'sans-serif';
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      background: rgb(226, 226, 226);
    }
    .inbody{
    background: rgba(255, 255, 255, 1);
    padding: 10px;
    border-radius: 10px;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
    min-width: 30%;
    height: 60vh; 
    overflow: auto;
    display:flex;
    flex-direction:row;
    column-gap: 5%;
  }
  .signup-box{
      display:flex;
      justify-content:center;
      align-items:center;
      width:100%;
      height: 100%;
      background: rgb(228, 228, 228);
      color:rgb(0, 0, 0);
    }
    .signup-box h1{
      font-size:32px;
      text-align:center;
      text-shadow: 3px 3px 8px rgb(133, 133, 132); 
    
    }
    .signup-box .inputbox{
      position:relative;
      width:340px;
      height: 50px;
      border-bottom:2px solid rgb(0, 0, 0);
      margin: 30px 0;
    }
    
    .inputbox input{
      width:100%;
      height: 100%;
      background:transparent;
      border:none;
      outline: none;
      color: rgb(0, 0, 0);
    }
    .inputbox ::placeholder{
      color:rgb(184, 184, 184);
    }
    
    .inputbox label{
      position:absolute;
      top:50%;
      left:0;
      transform: translateY(-50%);
      font-size: 16px;
      font-weight: 500;
      pointer-events: 500;
      transition: .5s ease;
    }
    .inputbox input:focus~label,
    .inputbox input:valid~label{
      top:-5px;
    }
    .button{
      width:100%;
      height:45px;
      background: rgb(0, 3, 161);
      border:none;
      outline:none;
      color:white;
      border-radius: 4px;
      cursor:pointer;
      font-weight:500;
      text-shadow: 3px 3px 8px rgb(0, 0, 0);
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
    }
    .button:hover{
      background: rgb(0, 2, 90);

    }
    .signup-box .login-link, .error-message{
      font-size: 14.5px;
      font-weight: 500;
      text-align: center;
      margin-top: 25px;
      color: rgb(0, 0, 0);
    }
    .login-link a {
      color: rgb(1, 44, 236); 
      text-decoration: none;
    }
    
    .login-link a:hover {
      text-decoration: underline; 
    }


</style>
