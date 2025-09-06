let mediaRecorder;
let audioChunks = [];

const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const audioPlayback = document.getElementById('audioPlayback');

startBtn.addEventListener('click', async () => {
  // Request microphone access
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);

  // Collect audio data
  mediaRecorder.ondataavailable = event => {
    if (event.data.size > 0) {
      audioChunks.push(event.data);
    }
  };

  // When recording stops, create an audio file
  mediaRecorder.onstop = () => {
    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
    audioChunks = []; // reset for next recording
    const audioUrl = URL.createObjectURL(audioBlob);
    audioPlayback.src = audioUrl;

    // Optional: upload to server
    // const formData = new FormData();
    // formData.append('audio', audioBlob, 'recording.webm');
    // fetch('/upload-audio', { method: 'POST', body: formData });
  };

  mediaRecorder.start();
  startBtn.disabled = true;
  stopBtn.disabled = false;
});

stopBtn.addEventListener('click', () => {
  mediaRecorder.stop();
  startBtn.disabled = false;
  stopBtn.disabled = true;
});