<template>
  <div class="body">
    <div class="inbody">
        <h2 class="logo"><strong>About Vocalytics<i class='bx bx-microphone'></i></strong></h2>
        <div class="content">
        <h4>Welcome to Vocalytics!! This is our voice analyzer designed to transcribe the words spoken by the
            user. If the words spoken by the user are in English, then Vocalytics transcribe them to English words and when 
            the words spoken by the user are not English, then Vocalytics translates and transcribes them to English. 
            Vocalytics supports 100 languages which are displayed in the home page. 
            To use this website, kindly login to the page. If you are not our registered user, then kindly register and then login. 
            Press the button "Start Recording" to record your voice for transcription. After speaking, press the button "Stop Recording". 
            Wait for few seconds and your transcribed words will be displayed on right. The detected language will be displayed 
            below it. Check out your History of Transcriptions and insights. If you are facing any issues or recommending some features, 
            kindly contact us. We are happy to hear from you.
        </h4>
        <h4>You can search for your transcriptions based on thw words or language from the history 
            of transcriptions page. In the Insights page you will be able to see top 
            10 frequent words transcribed by you, top 10 words transcribed by all users till now and 
            3 top unique phrases. If any information is found to be mistaken, kindly contact the admin 
            from the contact page
            
        </h4>
        <div class="footer">
                <p>&copy; 2024 Vocalytics. All rights reserved.</p>
            </div>
    </div>
</div>
    </div>
</template>

<script>
export default {

}
</script>

<style scoped>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Poppins', 'sans-serif';
}
.body{
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
    padding: 5%;
    border-radius: 10px;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
    width: 90%;
    min-height: 80vh;

    
  }
  .logo{
      color:rgb(1, 4, 161);
      text-align: center;
    }
    .content{
        margin-top:3%
    }
h4{
    text-align:justify ;
}
.footer{
text-align:center;
margin-top:5%;
}
</style>