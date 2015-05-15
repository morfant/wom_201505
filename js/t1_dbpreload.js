function showProgress(){

    var loadProgress = document.getElementById("progress");
    var loadProgressKind = document.getElementById("progressKind");

    loadProgress.innerHTML = j + "/" + numOfVoice;      
    loadProgressKind.innerHTML = i + "/" + numOfKind; 
    
}

    /*
    var body2 = document.getElementById("body_t2");
    if (body2){
        i = 1;
        j = 1;
        prePlay();

        $("#audioplay").bind('ended', function(){
            j++;
//            console.log("j :" + j);
            if (j == 7){
                i++;
//                console.log("i :" + i);
                j = 1;
            }

            if (i < 21) {
                prePlay();
            }else if (i == 21){
                $(".host").hide(1);
                console.log("T2_Preload audio files finished.");
            }
        });
    }
*/

}



window.addEventListener('load', showProgress);
