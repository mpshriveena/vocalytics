<template>
    <div class="body">
      <div class="inbody">
        <div class="block1">
          <h2 class="logo"><strong><i class='bx bx-microphone'></i> Vocalytics</strong></h2>
      <br>
      <div class="parent-container">
          <div class="button-block">
            <div class="buttonb">
          <button @click="startRecording" :disabled="recording"><i class='bx bxs-microphone'></i>Start Recording</button>
      <button @click="stopRecording" :disabled="!recording"><i class='bx bxs-microphone-off' ></i>Stop Recording</button>
    </div>
    <div class="status">
      <p v-if="recording">
  Recording your speech...
  <div class="spinner-grow spinner-grow-sm" role="status">
  <span class="visually-hidden">Loading...</span>
</div>
</p>
      <p v-if="processing">
  Your speech is being processed. Please wait...
  <div class="spinner-border spinner-border-sm" role="status">
  <span class="visually-hidden">Loading...</span>
</div>
</p>
</div>
</div>
    </div>
      <div class="languages-container">
        <h5> Supported Languages</h5>
        <br>
    <div class="language-line" v-for="(line, index) in languageLines" :key="index">
      <p v-for="language in line" :key="language" class="language-item">{{ language }}</p>
    </div>
  </div>
    </div>
    <div class="block2">
      <h4><strong>Transcription</strong></h4>
      <br>
      <p>Your transcribed speech will be given below..</p>
      <br><br>
      <div class="transcription-block">
        
      <p v-if="transcription">{{ transcription }}</p>
    </div>
      <p v-if="detected_language">Detected Language: {{ detected_language }}</p>
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
    data() {
      return {
        mediaRecorder: null,
        audioChunks: [],
        recording: false,
        processing: false,
        transcription: '',
        detected_language:'',
        user_id: JSON.parse(localStorage.getItem('user_info')).user_id,
        languages: [
        "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Assamese", "Azerbaijani", "Bashkir", "Basque", "Belarusian",
        "Bengali", "Bosnian", "Breton", "Bulgarian", "Burmese", "Castilian", "Catalan", "Chinese", "Croatian", "Czech",
        "Danish", "Dutch", "English", "Estonian", "Faroese", "Finnish", "Flemish", "French", "Galician", "Georgian",
        "German", "Greek", "Gujarati", "Haitian Creole", "Hausa", "Hawaiian", "Hebrew", "Hindi", "Hungarian", "Icelandic",
        "Indonesian", "Italian", "Japanese", "Javanese", "Kannada", "Kazakh", "Khmer", "Korean", "Lao", "Latin",
        "Latvian", "Lithuanian", "Luxembourgish", "Macedonian", "Malagasy", "Malay", "Malayalam", "Maltese", "Maori", "Marathi",
        "Mongolian", "Nepali", "Norwegian", "Occitan", "Punjabi", "Pashto", "Persian", "Polish", "Portuguese", "Romanian",
        "Russian", "Sanskrit", "Serbian", "Shona", "Sindhi", "Sinhala", "Slovak", "Slovenian", "Somali", "Spanish",
        "Sundanese", "Swahili", "Swedish", "Tagalog", "Tajik", "Tamil", "Tatar", "Telugu", "Thai", "Tibetan",
        "Turkish", "Turkmen", "Ukrainian", "Urdu", "Uzbek", "Vietnamese", "Welsh", "Wolof", "Yiddish", "Yoruba"
      ]
      };
    },
    computed: {
    languageLines() {
      // Split the languages into chunks of 10
      const chunkSize = 10;
      let result = [];
      for (let i = 0; i < this.languages.length; i += chunkSize) {
        result.push(this.languages.slice(i, i + chunkSize));
      }
      return result;
    }
  },
    methods: {
      async startRecording() {
        this.audioChunks = [];
        this.recording = true;
        this.transcription = '';
        this.detected_language = '';
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          this.mediaRecorder = new MediaRecorder(stream);
  
          this.mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
              this.audioChunks.push(event.data);
            }
          };
  
          this.mediaRecorder.start();
        } catch (error) {
          console.error('Error accessing audio devices:', error);
        }
      },
  
      async stopRecording() {
        if (this.mediaRecorder) {
          this.recording = false;
          
          this.mediaRecorder.stop();
          this.processing = true;
          this.mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
            console.log(audioBlob)
            const formData = new FormData();
            formData.append('audio', audioBlob, 'audio.wav');
            formData.append('user_id', JSON.parse(localStorage.getItem('user_info')).user_id);
            console.log(formData)
            for (let pair of formData.entries()) {
                console.log(`${pair[0]}, ${pair[1]}`);
            }
            try {
              const accesstoken = localStorage.getItem("access_token");
              const response = await axios.post('https://0e59-59-182-251-46.ngrok-free.app/transcribe', formData, {
                headers: {
                  'Content-Type': 'multipart/form-data',
                  Authorization: `Bearer ${accesstoken}`
                }
              });
              this.processing = false;
              this.toast.success("Transcribed Successfully");
              this.transcription = response.data.transcription;
              console.log(this.transcription)
              this.detected_language = response.data.detected_language;
              console.log(this.detected_language)
            } catch (error) {
              console.error('Error:', error.response ? error.response.data : error.message);
            }
          };
        }
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
    padding: 2%;
  
  }
  .inbody{
    background: rgba(255, 255, 255, 1);
    padding: 10px;
    border-radius: 10px;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
    width: 100%;
    min-height: 80vh; 
    overflow: auto;
    display:flex;
    column-gap: 5%;
  }
  .logo{
      color:rgb(1, 4, 161);
    }
  .block1{
  text-align: left;
  padding:20px;
  width:50%;
  height: 60vh;
  border-radius: 10px;
  background: transparent;
  border: 2px solid rgb(255, 255, 255);
  }
  .block2{
  text-align: left;
  padding:20px;
  width:50%;
  height: 60vh;
  border-radius: 10px;
  background: transparent;
  border: 2px solid rgb(255, 255, 255);
  }
  .transcription-block{
  background:rgb(214, 214, 214);
  min-height:100%;
  border-radius: 20px;
  padding:5%;
  }
  .languages-container {
  padding: 10px;
  max-width: 1000px;
  margin: 0 auto;
  }
  
  .language-line {
  display: flex;
  flex-wrap: wrap;
  gap: 4px; 
  }
  
  .language-item {
  display: inline-flex; 
  flex-shrink: 0; 
  padding: 5px; 
  text-align: center;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 12px;
  background-color: #f9f9f9;
  white-space: nowrap;
  margin: 2px;
  }
  .parent-container {
  display: flex;
  justify-content: center; 
  height: 40%; 
  }
  .button-block {
  background: rgb(231, 231, 231);
  height: auto; 
    min-height: 0; 
  width: 90%;
  border-radius: 40px;
  display: flex;
  flex-direction: column; 
  align-items: center; 
  justify-content: center; 
  padding: 20px; 
  box-sizing: border-box;
  }
  
  .buttonb {
  display: flex;
  flex-direction: row; 
  column-gap: 10%; 
  }
  
  .status {
  margin-top: 20px; 
  text-align: center;
  }
  
  .button-block button {
  width:210px;
  border: none;      
  border-radius: 20px;    
  color: white;       
  padding: 10px 20px;  
  cursor: pointer;        
  font-size: 16px;    
  display: flex;
  align-items: center; 
  }
  .button-block button:first-of-type {
  background: transparent; 
  border: 2px solid green;
  color: green; 
  }
  
  .button-block button:last-of-type {
  background: transparent; 
  border: 2px solid red; 
  color: red; 
  }
  
  .button-block .spinner-border {
  margin-left: 10px; 
  }
  .button-block button:disabled {
  opacity: 0.5; 
  cursor: not-allowed; 
  }
  @media screen and (max-width: 768px) {
  .inbody {
    flex-direction: row; 
  }
  
  .block1, .block2 {
    width: 100%; 
    margin: 0 0 20px; 
  }
  
  .button-block {
    display: flex;
    flex-direction: column;
    align-items: center; 
    width: 100%; 
    box-sizing: border-box; 
  min-height:30vh;
  }
  
  .button-block button {
    width: 100%; 
    margin: 10px 0; 
  }
  
  .languages-container {
    flex-direction: column; 
    align-items: center;
    height:200px;
    margin-top: 50%; 
  }
  .buttonb{
    flex-direction: column;
  }
  .block1 {
      flex-direction: column;
    }
    
    .block2 {
      order: 2; 
      margin-top: 20px; 
    }
  
  }
  </style>