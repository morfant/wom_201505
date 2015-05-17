var preloadCount = 0;


function preload(url) {
  source = context.createBufferSource();
  request = new XMLHttpRequest();

  request.open('GET', url, true);

  request.responseType = 'arraybuffer';

  request.onload = function() {
      preloadCount++;
      console.log("preloadCount : " + preloadCount);

      var loadProgress = document.getElementById("progress");
      loadProgress.innerHTML = preloadCount + "/" + numOfSound;      
      
      if(preloadCount == numOfSound){
          console.log("All files loaded.");
          $(".host").hide(1);
          buttonActivated = 1;
          console.log("buttonActivated: " + buttonActivated);
      }
  }


  request.send();
}


function getData(url) {
  source = context.createBufferSource();
  request = new XMLHttpRequest();

  request.open('GET', url, true);

  request.responseType = 'arraybuffer';

  request.onload = function() {
    var audioData = request.response;

    context.decodeAudioData(audioData, function(buffer) {
        source.buffer = buffer;
        console.log("Data loaded.");
      },

      function(e){"Error with decoding audio data" + e.err});
  }

  request.send();
}


function prePlay(){

    var loadProgressComment = document.getElementById("comment");
    var loadProgress = document.getElementById("progress");
    var loadProgressKind = document.getElementById("progressKind");
    loadProgressComment.innerHTML = "sound files preloading...";      
    loadProgress.innerHTML = j + "/" + numOfVoice;      
    loadProgressKind.innerHTML = i + "/" + numOfKind; 
    
    var src = "./audio/t3/" + i + "/" + j + ".mp3";
    $('#audioplay').attr('src', src);
    audio.play();
}


function preload() {
    var body = document.getElementById("t1_db_body");
    if (body){
    
    console.log("hhhhhh");
    }
}



window.addEventListener('loadstart', preload );
