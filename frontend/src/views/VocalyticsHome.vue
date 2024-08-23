<template>
    <div class="home">
      <div class="inhome">
     
        <div class="hello">
          <div class="content">
            <h2 class="logo"><strong><i class='bx bx-microphone'></i> Vocalytics</strong></h2>
          </div>
            <div class="text-sci">
              <h1> Welcome ! !<br><strong> To our Voice Analyzer</strong></h1>
              <p>World has many languages for its communication. 
                Thats why transcription and translation became people's one of the necessity. 
               We aim to provide quality translations for your voice anywhere, anytime!! 
               Please use the "About" page 
          to know how to use this website. Happy Vocalyzing!!</p>
            </div>
        </div>
        <div class="login">
            <div class="form-box">
            <form @submit.prevent="LogIn">
              <h2><strong>Login</strong></h2>
              <div class="input-box">
                <input type="email" id="email" placeholder="name@example.com" v-model='email' required>
                <label>Email</label>
              </div>
              <div class="input-box">
                <input type="password" id="password" v-model='password' required>
                <label>Password</label>
              </div>
              
                <button type="submit" class="button" @click='LogIn'> Login </button>
              
              <div class="register-link">
                <p>Don't have an account? <router-link to="/register"><a>Register</a></router-link> </p>
              </div>
              <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
              </div>
            </form>
            
            </div>
        </div>
        </div>
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
      data(){
        return{
          email:'',
          password:'',
          errorMessage:'',
        };
      },
      
      methods:{
          LogIn(){
            this.$axios.post('http://127.0.0.1:5000/', {
              email: this.email,
              password: this.password
            }).then(response => {
      const user = response.data.user
      
      const access_token = response.data.access_token
      const backgroundImageURL = `../public/background2.jpg`;
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user_info',JSON.stringify(user));
      window.location.reload();
      this.toast.success("Login successful!!");
      this.$router.push('/home');
    }).catch(error => {
      this.errorMessage = error.response.data.message
    });
           
        }
      }
    }
    </script>
    
    <style scoped>
    .home {
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
    .inhome{
    background: rgba(255, 255, 255, 1);
    padding: 10px;
    border-radius: 10px;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
    width: 90%;
    height: 80vh; 
    overflow: auto;
    display:flex;
    flex-direction:row;
    column-gap: 5%;
  }
    
    .hello .content{
      font-size:30px;
    
    }
    .home .hello{
      width:100%;
      height: 100%;
      background:transparent;
      padding: 12%;
      color:rgb(0, 0, 0);
    }
    
    .home .login{
      width:100%;
      height: 100%;
    }
    
    .hello .content h2 {
      font-size: 30px;
      text-shadow: 3px 3px 8px rgba(0, 0, 0, 0.616);
    }
    
    .text-sci h1 {
      font-size: 40px;
      text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.452); 
    }
    
    .text-sci p {
      font-size: 22px;
      margin: 20px 0;
      color: rgb(66, 66, 66);
      text-shadow: 5px 5px 15px rgba(0, 0, 0, 1);
      padding: 10px;
      border-radius: 5px; 
    }
    .login .form-box{
      display:flex;
      justify-content:center;
      align-items:center;
      width:100%;
      height: 100%;
      background: rgb(228, 228, 228);
      color:rgb(0, 0, 0);
    }
    .form-box h2{
      font-size:32px;
      text-align:center;
      text-shadow: 3px 3px 8px rgb(133, 133, 132); 
    
    }
    .form-box .input-box{
      position:relative;
      width:340px;
      height: 50px;
      border-bottom:2px solid rgb(0, 0, 0);
      margin: 30px 0;
    }
    
    .input-box input{
      width:100%;
      height: 100%;
      background:transparent;
      border:none;
      outline: none;
      color: rgb(0, 0, 0);
    }
    .input-box ::placeholder{
      color:rgb(184, 184, 184);
    }
    
    .input-box label{
      position:absolute;
      top:50%;
      left:0;
      transform: translateY(-50%);
      font-size: 16px;
      font-weight: 500;
      pointer-events: 500;
      transition: .5s ease;
    }
    .input-box input:focus~label,
    .input-box input:valid~label{
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
    .form-box .register-link, .error-message{
      font-size: 14.5px;
      font-weight: 500;
      text-align: center;
      margin-top: 25px;
      color: rgb(0, 0, 0);
    }
    .register-link a {
      color: rgb(1, 44, 236); 
      text-decoration: none;
    }
    
    .register-link a:hover {
      text-decoration: underline; 
    }
    .logo{
      color:rgb(1, 4, 161);
    }
    @media screen and (max-width: 768px) {
.inhome{
  flex-direction:column;
}
.login .form-box{
  height:50vh;
  
}
    }
    
    </style>
    