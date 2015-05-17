# -*- coding:utf-8 -*-
import sys
import cgi
import urllib
import webapp2
import random
import glob, os
import re
import time

from google.appengine.api import users
from google.appengine.ext import ndb

#################################### MACRO ####################################
DEFAULT = "hello"
DATA_FILE = "data.txt"
DATA_FILE_1 = "data_1.txt"
DATA_FILE_2 = "data_2.txt"
DATA_FILE_3 = "data_3.txt"
DATA_FILE_4 = "data_4.txt"
IMG_NUMBER = 34
#data.txt의 마지막 줄에는 내용 없는 엔터가 필요하다. 마지막 줄 끝에 \n 이 입력되어야 하기 때문에.


#################################### GLOBAL VARIABLE ####################################
korIdx = 0
engIdx = 0

class StaticKeys :
    keys = ""
    keys_ENG = ""

#################################### HTML ####################################
# 2015.05.09
LIST_DB_T1_PAGE_HTML = """\
<!DOCTYPE html>
<html>
    <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" >

    <style type="text/css">
        body {margin-top: 50px;}
        #foot {
            position: relative;
            top: 100px;
            font-size: 10px;
            }
        p {
            font-size: 12px;
            }
        #dblist {
            position: relative;
            left: 50px;
            font-size: 15px;
            }
        #imgs {
            position: relative;
            top: 50px;
            left: 50px;
        }
        div#aimg{
            position: relative;
            margin-top: 150px;
        }



    </style>

    </head>
    <body id="t1_db_body">
    <script src="js/dbload.js"></script>
    
    <!-- loading animation -->
    <div class="host">
        <div class="loading loading-0"></div>
        <div class="loading loading-1"></div>
        <div class="loading loading-2"></div>
        <div align="center" class="progressNumber"><span id="progress"></span></div>
    </div>


        <div align="center">
            <form method="get" action="/t1">
                <div style="margin-top: 80px">
                    <input type="submit" value="돌아가기 / Go back">
                </div>
            </form>
        </div>
    </body>

    <footer>
        <div id="foot" align="center">
            <p>Taewon Kim & Gang il Yi<br>taewonnice@naver.com / giy.hands@gmail.com</p>
        </div>
    </footer>

</html>
"""

LIST_DB_T2_PAGE_HTML = """\
<!DOCTYPE html>
<html>
    <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" >

    <style type="text/css">
        body {margin-top: 50px;}
        #foot {
            position: relative;
            top: 100px;
            font-size: 10px;
            }
        p {
            font-size: 12px;
            }
        #dblist {
            position: relative;
            left: 50px;
            font-size: 12px;
            }


    </style>

    </head>
    <body id="body_list_t2">

    <div id = "dblist_t2" style="line-height: 0.0em; position: relative; left:50px; top:10px; width:1024px;" align="left">
    </div>
 

        <script src="js/t2_list.js"></script>
        <script>

            numOfSound = 31;

            var i;
            var temp_arr;
            var temp_span;
            var temp_pk, temp_pe;
            var temp_button_play, temp_button_stop;
            var space, space2;
                
        for (i = 0; i < list_t2.length; i++) {
                temp_arr = list_t2[i].split('_');
 
                temp_pk = document.createElement("p");
                temp_pk.style.display = "inline";
                temp_pk.id = "p" + (i + 1);
                temp_pk.innerHTML = temp_arr[0] + "&nbsp;&nbsp;&nbsp;&nbsp";
                document.getElementById("dblist_t2").appendChild(temp_pk);
                
                temp_button_play = document.createElement("button");
                temp_button_play.type = "button";
                temp_button_play.id = "play_" + (i + 1);
                temp_button_play.innerHTML = "Play";
                document.getElementById("dblist_t2").appendChild(temp_button_play);

                temp_button_stop = document.createElement("button");
                temp_button_stop.type = "button";
                temp_button_stop.id = "stop_" + (i + 1);
                temp_button_stop.innerHTML = "Stop";
                document.getElementById("dblist_t2").appendChild(temp_button_stop);

                temp_pe = document.createElement("p");
                temp_pe.id = "pe" + (i + 1);
                temp_pe.innerHTML = temp_arr[1];
                document.getElementById("dblist_t2").appendChild(temp_pe);
 
                space = document.createElement("p");
                space.innerHTML = "<br></br>"; 
                document.getElementById("dblist_t2").appendChild(space);
        }
        
        </script>
 
        <audio id="audioplay" preload="auto"> </audio>

        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
        <script>

        var audio = document.getElementById('audioplay');

        $(':button').click(
            function () {

            
            var id = $(this).attr('id');
        //    console.log("id: " + id);
            var id_num = id.split('_')[1];
        //    console.log("id_num: " + id_num);
           
            if (id.split('_')[0] == "play") {
                var path = 'audio/t2/'+id_num;
                var exp = ".mp3";

                $('#audioplay').attr('src', path + exp );
                audio.play();
        //        console.log('Play started : ' + $('#audioplay').attr('src'));
                }
            else {
                var path = 'audio/t2/'+id_num;
                var exp = ".mp3";

                $('#audioplay').attr('src', path + exp );
                audio.pause();
                audio.currentTime = 0;
        //        console.log('Play stopped : ' + $('#audioplay').attr('src'));
            
                }
            }
        );

        </script>
    
        <div align="center">
            <form method="get" action="/t2">
                <div style="margin-top: 130px">
                    <input type="submit" value="돌아가기 / Go back">
                </div>
            </form>
        </div>
    </body>

    <footer>
        <div id="foot" align="center">
            <p>Taewon Kim & Gang il Yi<br>taewonnice@naver.com / giy.hands@gmail.com</p>
        </div>
    </footer>

</html>
"""

# 2015.05.12
LIST_DB_T3_PAGE_HTML = """\
<!DOCTYPE html>
<html>
    <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" >

    <style type="text/css">
        body {margin-top: 50px;}
        #foot {
            position: relative;
            top: 100px;
            font-size: 10px;
            }
        p {
            font-size: 12px;
            }
        #dblist {
            position: relative;
            left: 50px;
            font-size: 12px;
            }


    </style>

    </head>
    <body id="body_list_t3">

    <div id = "dblist_t3" style="line-height: 0.0em; position: relative; left:50px; top:10px; width:1024px;" align="left">
    </div>
 

        <script src="js/t3_list.js"></script>
        <script>

            numOfVoice = 6;
            numOfKind = 20;

            var i;
            var temp_arr;
            var temp_span;
            var temp_pk, temp_pe;
            var temp_button;
            var space, space2;
                
        for (i = 0; i < names_t3.length; i++) {
                temp_arr = names_t3[i].split('_');
 
                temp_pk = document.createElement("p");
                temp_pk.style.display = "inline";
                temp_pk.id = "p" + (i + 1);
                temp_pk.innerHTML = temp_arr[0] + "&nbsp;&nbsp;&nbsp;&nbsp";
                document.getElementById("dblist_t3").appendChild(temp_pk);
                
                for (j = 0; j < numOfVoice; j++) {
                    temp_button = document.createElement("button");
                    temp_button.type = "button";
                    temp_button.id = "sori_" + (i + 1) + "_person_" + (j + 1);
                    temp_button.innerHTML = "Person_" + (j + 1);
                    document.getElementById("dblist_t3").appendChild(temp_button);
                }

                temp_pe = document.createElement("p");
                temp_pe.id = "pe" + (i + 1);
                temp_pe.innerHTML = temp_arr[1];
                document.getElementById("dblist_t3").appendChild(temp_pe);
 
                space = document.createElement("p");
                space.innerHTML = "<br></br>"; 
                document.getElementById("dblist_t3").appendChild(space);
        }
        
        </script>
 
        <audio id="audioplay" preload="auto"> </audio>

        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
        <script>

        var audio = document.getElementById('audioplay');

        $(':button').click(
            function () {


            var id = $(this).attr('id');
        //    console.log("id: " + id);
            var id_sori = id.split('_')[1];
        //    console.log("id_sori: " + id_sori);
            var id_person = id.split('_')[3];
        //    console.log("id_person: " + id_person);
            var path = 'audio/t3/'+id_sori+'/'+id_person;
            var exp = ".mp3";

            $('#audioplay').attr('src', path + exp );
            audio.play();
        //    console.log('Play started : ' + $('#audioplay').attr('src'));
            } 
        );

        </script>
    
        <div align="center">
            <form method="get" action="/t3">
                <div style="margin-top: 130px">
                    <input type="submit" value="돌아가기 / Go back">
                </div>
            </form>
        </div>
    </body>

    <footer>
        <div id="foot" align="center">
            <p>Taewon Kim & Gang il Yi<br>taewonnice@naver.com / giy.hands@gmail.com</p>
        </div>
    </footer>

</html>
"""



FIND_PAGE_HTML = """\
<!DOCTYPE html>
<html>
    <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" >

    <style type="text/css">
        body {margin-top: 50px;}
        #foot {
            position: relative;
            top: 100px;
            font-size: 10px;
            }
        p {
            font-size: 12px;
            }


    </style>

    </head>
    <body>
        <div align="center">
            <form method="get" action="/t1">
                <div style="margin-top: 30px">
                    <input type="submit" value="돌아가기 / Go back">
                </div>
            </form>
        </div>
    </body>

    <footer>
        <div id="foot" align="center">
            <p>Taewon Kim & Gang il Yi<br>taewonnice@naver.com / giy.hands@gmail.com</p>
        </div>
    </footer>

</html>
"""

T0_PAGE_HTML = """\
<!DOCTYPE html>
<html>
    <head>
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" >
        <title>번역기_Main</title>

        <style type="text/css">
            body {
                position: relative;
                top: 50px;
                }
            #foot {
                position: relative;
                top: 400px;
                font-size: 10px;
                }
            p {
                font-size: 12px;
                }
            
            .bold
            {
                font-weight: bold;
            }

            .under
            {
                text-decoration: underline;
            }

            .red
            {
                color: red;
            }

            #title {
            font-size: 15px;
            }

            #menu {
            font-size: 12px;
            }

            #guide {
            font-size: 11px;
            }

            a {
            color: black;
            text-decoration: none;
            }

            a:hover {
//            color: #339966;
            color: #669999;
            }

        </style>

    </head>

    <body>
       <div id="title" style="position: relative; left: 20px; width: 600px;" align="left">
       <p>번역기</p>
       <hr>
       </div>
       
       <div id="menu" style="position: relative; top: 30px; left: 20px; width: 600px;" align="left">
       <span>
       <a href="../t1">번역기 1 (임대된 사무실) &nbsp | &nbsp Translator 1 (A rented office) </a>
       </span>
       <br>
       <br>
       <span>
       <a href="../t2">번역기 2 (사서) &nbsp | &nbsp Translator 2 (Librarian) </a>
       </span>
       <br>
       <br>
       <span>
       <a href="../t3">번역기 3 (도서박람회) &nbsp | &nbsp Translator 3 (Book Festival) </a>
       </span>

       </div>
       
       <div id="guide" style="position: relative; top: 380px; left:20px;" align="left">
       <span>
       * '번역기 2(사서)'와 '번역기3(도서박람회)'은 Internet Explore에서 정상 작동하지 않습니다. 
       구글 크롬 등 Web Audio API를 지원하는 브라우저가 필요합니다.
       </span><br>
      <span>
       ** '번역기 2(사서)'의 사용을 위해서는 내장 혹은 외장 마이크가 연결되어 있어야 하며,
       페이지 이동 후 상단 안내 메시지를 통해 브라우저에서의 장치 접근을 허용해 주어야 합니다.
       </span><br><br>

       <span>
       * Internet Explore doesn’t support 'Translator 2(Librarian)' and 'Translator 3(Book Festival)'.
       You need to use web browsers that support Web Audio API(Mozila Firefox, Google Chrome, etc.).
       </span><br>
       <span>
       ** Microphone(built-In or external) is needed to use 'Translator 2(Librarian)'.
       After page loaded, click ‘Allow’ in top guide message to allow browser to access your input device.
       </span>
       </div>


   </body>

    <footer>
        <div id="foot" style="position: relative; left: 20px;" align="left">
            <p>Taewon Kim & Gang il Yi<br>taewonnice@naver.com / giy.hands@gmail.com</p> 
        </div>
    </footer>

</html>
"""

T1_PAGE_HTML = """\
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" >
        <title>번역기_1 (A rented office)</title>
        <style type="text/css">
            body {
                position: relative;
                top: 50px;
                }
            #foot {
                position: relative;
                top: 400px;
                font-size: 10px;
                }
            p {
                font-size: 12px;
                }
        </style>

    </head>

    <body>

        <div>
            <form method="get" action="/findData">
                <div align="center">
                    <input type="text" size="100" name="searchingWord">
                </div>
                <div style="position: relative; top: 50px" align="center">
                    <input type="submit" value="번역 / Translate">
                </div>
            </form>
            <div style="position: relative; top: 200px" align="center">
                <p>
                한국어와 영어 입력이 가능합니다.
                <br>
                한국어와 영어(숫자, 특수문자 포함)를 함께 사용하는 경우에는 이미지가 출력 됩니다.
                </p>
                <p>
                KOREAN and ENGLISH are both available.
                <br>
                If you enter words in KOREAN and ENGLISH(Numbers and special characters are included) at the same time,<br>random image will be displayed.
                </p>

            </div>
        </div>
    </body>

    <footer>
        <div id="foot" align="center">
        
            <form method="get" action="/listData_t1">
                <div style="margin-top: 30px">
                    <input type="submit" value="데이터베이스 / DataBase">
                </div>
            </form>

            <p>Taewon Kim & Gang il Yi<br>taewonnice@naver.com / giy.hands@gmail.com</p>

            <form method="get" action="/">
                <div style="margin-top: 30px; margin-bottom: 30px">
                    <input type="submit" value="Main">
                </div>
            </form>
 
        </div>


    </footer>

</html>
"""



T2_PAGE_HTML = """\
<!DOCTYPE html>
<html>
    <head>
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" >
        <title>번역기_2 (Librarian)</title>

        <style type="text/css">
            body {
                position: relative;
                top: 50px;
                }
            #foot {
                position: relative;
                top: 400px;
                font-size: 10px;
                }
            p {
                font-size: 12px;
                }
            
            .bold
            {
                font-weight: bold;
            }

            .under
            {
                text-decoration: underline;
            }

            .red
            {
                color: red;
            }
  
            section
            {
                width: 120px;
            }

            section div{
                display: inline-block;
                width: 50px;
                height: 50px;
                background: yellow;
            }

            button{
                border : solid 1px #000000;
                border-radius : 17px;
                moz-border-radius : 17px;
                font-size : 10px;
                color : #000000;
                padding : 1px 10px;
               // background-color : #ffffff;
                background-color : rgba(255, 255, 255, 0.3);
            }

            .black{
              // background-color : #bbbbbb;
               background-color : rgba(55, 55, 55, 0.2);
               
            }
            .white{
              // background-color : #ffffff;
               background-color : rgba(255, 255, 255, 0.3);
            }

            .host{
              background:#FFF;
              width:45px; //15 * 3
              height:10px;
              margin: auto;
              padding-top:40px;

            }
            .loading{
              width:10px;
              height:10px;
              background:#FFF;
              border-radius:100%;
              float:left;
              margin-right:2.5px;
              margin-left:2.5px;
            }
            .loading-0{
                -webkit-animation:bounce 2.0s infinite;
                -webkit-animation-delay:.1s;
//                background:#009DC6;
                background:#000;
              
            }
            .loading-1{
                -webkit-animation:bounce 2.0s infinite;
                -webkit-animation-delay:.3s;
//                background:#e8b440;
                background:#000;
            }
            .loading-2{
                -webkit-animation:bounce 2.0s infinite ease;
                -webkit-animation-delay:.5s;
//                background:#b62327;
                background:#000;
            }
            @-webkit-keyframes bounce {
              0%, 100% {

                opacity:1;
              }
              60% {
                opacity:.0;
              }
            }

            .progressNumber {
                font-size : 12px;
            }

        </style>

    </head>

    <body id="body_t2" onload="show();">
    <script src="js/stopwatch.js"></script>
    <script src="js/audio_in.js"></script>
    <script src="js/audioHandle.js"></script>

    <!-- loading animation -->
    <div class="host">
        <div class="loading loading-0"></div>
        <div class="loading loading-1"></div>
        <div class="loading loading-2"></div>
        <div align="center" class="progressNumber"><span id="progress"></span></div>
    </div>


            <!-- audio meter -->
            <div style="position: relative; top: 150px;" align="center">
            <canvas id="audioDisplay" width="400" height="10"> </canvas>
            </div>



       <div>
           <div id="buttons" style="position: relative; top: 200px" align="center">
           <div id="recbutton" style="display: inline-block;">
           <button type="button" id="recStart">Rec&nbsp&nbsp&nbsp&nbsp&nbsp</button>
           </div>

           <div id="stopbutton" style="display: inline-block;">
           <button type="button" id="recStop">Stop(translate)&nbsp&nbsp&nbsp&nbsp&nbsp</button>
           </div>
         
        <div id="recdiv" style="position:relative; bottom:15px; left:12px; z-index:-1">
            <canvas id="recSymbol" width="10" height="10"> </canvas>
        </div>

        <div id="stopdiv" style="position:relative; bottom:15px; left:40px; z-index:-1">
            <canvas id="stopSymbol" width="10" height="10"> </canvas>
        </div>

        <script>
            // RED CIRCLE
            var c=document.getElementById("recSymbol");
            var ctx=c.getContext("2d");
            ctx.fillStyle="#FF0000";
            ctx.beginPath();
            ctx.arc(5, 5, 5, 0, 2.0*Math.PI);
            ctx.fill();

            // BLACK RECT
            var c=document.getElementById("stopSymbol");
            var ctx=c.getContext("2d");
            ctx.fillStyle="#000000";
            ctx.fillRect(0,0,10,10);

            var buttons = document.getElementById("buttons");
            var recbut = document.getElementById("recbutton");
            var stopbut = document.getElementById("stopbutton");
            var recSymbol = document.getElementById("recdiv");
            var stopSymbol = document.getElementById("stopdiv");
            

            recbut.appendChild(recSymbol);
            stopbut.appendChild(stopSymbol);
//            buttons.appendChild(stopSymbol);
//            buttons.appendChild(stopSymbol);
        </script>

           <div>
           <span id="rectime"></span>
           </div>

            <script>

            $(':button').mousedown(function() {

                if (buttonActivated == 1) {
                $(this).removeClass('white');
                $(this).addClass('black');
                };
                });       
 
            $(':button').mouseup(function() {

                if (buttonActivated == 1) {
                $(this).removeClass('black');
                $(this).addClass('white');
                };
                });       

            numOfSound = 32;
            var isRecPushed = 0;
            var isPlaying = 0;
            var buttonActivated = 0;

            $('#recStart').click(
                function () {
                    if (buttonActivated == 1) {

//                $(".host").hide();
                        if (isPlaying == 1 && isRecPushed == 0) stopAudio();
                       
                            var path = 'audio/t2/';
                            var exp = ".mp3";
                            var playFileName = Math.floor((Math.random() * numOfSound) + 1);
                            url = path + playFileName + exp;

                            if (isRecPushed == 0){
                                getData(url);
                            
                                // audio input connect
                                getInput(1); //out to right

                                $(this).addClass("red");

                                //Timer
                                start();
            //                    console.log('rec Started.');
                            }

                            isRecPushed = 1;
            //                console.log("isRecPushed: 1");
                           
                }
            } 
       );

            $('#recStop').click(
                function () {

            if (buttonActivated == 1) {
 
 //               $(".host").show();

                //Timer
                stop();
                reset();

                $('#recStart').removeClass("bold under red");

                // audio input disconnect
                audioInput.disconnect();
                inputPoint.disconnect();
                javascriptNode.disconnect();
                

                if (isRecPushed == 1){

                    playAudio(-1, 1);
                   console.log('Play started : ' + url);
                    
                    isPlaying = 1;
//                    console.log("isPlaying: 1");
                    isRecPushed = 0;
//                    console.log("isRecPushed: 1");

                }else{
                    isPlaying = 0;
//                    console.log("isPlaying: 0");
                    stopAudio();
                    console.log('Stoped.');
                } 
              }
            }
            );
            </script>



<div style="display: block; position: relative; top: 00px">
<p>번역되는 소리는 2014년 은평구립도서관에서 발생한 소리입니다. The translated sound was generated at Eunpyeong District Library in 2014.</p>
<p>녹음(Rec)버튼을 누르고 소리를 인풋하세요. Press the rec button and make some sound into mic.</p>
<p>정지(Stop)버튼을 누르면 소리가 번역되어집니다. If you press the stop button, your input sound will be translated and be heard.</p>
</div>




    </div>
    </body>

    <footer>
        <div id="foot" align="center">

            <form method="get" action="/listData_t2">
                <div style="margin-top: 30px">
                    <input type="submit" value="데이터베이스 / DataBase">
                </div>
            </form>

            <p>Taewon Kim & Gang il Yi<br>taewonnice@naver.com / giy.hands@gmail.com</p>

            <form method="get" action="/">
                <div style="margin-top: 30px; margin-bottom: 30px">
                    <input type="submit" value="Main">
                </div>
            </form>
 
        </div>
    </footer>

</html>
"""


T3_PAGE_HTML = """\
<!DOCTYPE html>
<html>
    <head>
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" >
        <title>번역기_3 (Book Festival)</title>

        <style type="text/css">
            body {
                position: relative;
                top: 50px;
                }
            #foot {
                position: relative;
                top: -100px;
                font-size: 10px;
                }
            p {
                font-size: 12px;
                }

            #divider {
                position: absolute;
                left: 460px;
                }
            #button_play{
                position: relative;
                left: 70px;
                -moz-border-radius: 10px;
                -webkit-border-radius: 10px;
                border-radius: 10px;
                }
            
            button{
                border : solid 1px #000000;
                border-radius : 17px;
                moz-border-radius : 17px;
                font-size : 10px;
                color : #000000;
                padding : 1px 10px;
                background-color : #ffffff;
            }

            .black{
               background-color : #bbbbbb;
            }
            .white{
               background-color : #ffffff;
            }

       </style>

    </head>

    <body id="body_t3">

       <div id = "plist" style="line-height: 0.0em; position: relative; left:50px; top:10px; width:1024px;" align="left">
       </div>
        
        <script src="js/t3_list.js"></script>
        <script>

            var i;
            var temp_span;
            var temp_p;
            var temp_button;
            var space;

            for (i = 0; i < names_t3.length; i++) {

                temp_p = document.createElement("p");
//                temp_p.style.display = "block";
                temp_p.id = "p" + (i + 1);
                temp_p.innerHTML = names_t3[i];

                temp_button = document.createElement("button");
                temp_button.type = "button";
                temp_button.id = "sori_" + (i + 1);
                temp_button.innerHTML = "PLAY";
 
                space = document.createElement("p");
                space.innerHTML = "<br> "; 

               
                document.getElementById("plist").appendChild(temp_p);
                document.getElementById("plist").appendChild(temp_button);
                document.getElementById("plist").appendChild(space);

           }

        </script>

            <audio id="audioplay" preload="auto"> </audio>

            <script>

                numOfVoice = 6;
                numOfKind = 20;

            var audio = document.getElementById('audioplay');

            $(':button').mousedown(function() {
                $(this).removeClass('white');
                $(this).addClass('black');
                });       
 
            $(':button').mouseup(function() {
                $(this).removeClass('black');
                $(this).addClass('white');
                });       
            
            $(':button').click(
                function () {


                var id = $(this).attr('id');
                //console.log("id: " + id);
                var id_num = id.split('_')[1];
                //console.log("id_num: " + id_num);
                var path = 'audio/t3/'+id_num+'/';
                var exp = ".mp3";
                var playFileName = Math.floor((Math.random() * numOfVoice) + 1);

                $('#audioplay').attr('src', path + playFileName + exp );
                audio.play();
                console.log('Play started : ' + $('#audioplay').attr('src'));
                } 
            );

            </script>
 
            <div id="actorlist" style="position: relative; left:620px; bottom: 600px; width: 330px" align="right">
                <p>
                * 배우(목소리로만 연기하는 배우)
                <br>
                <br>
                Person 1_Markus Kalmbach/Linz, Austria/Publisher
                <br>
                <br>
                Person 2_Knut Diers/Hanova, Germany/Journalist
                <br>
                <br>
                Person 3_Dirk Lambach/Kassel, Germany/Major in geography
                <br>
                <br>
                Person 4_Burghard Lutter/Duisburg, Germany/Electrochemistry
                <br>
                <br>
                Person 5_Lucas Declauser/Meran, Italy/Information technologies
                <br>
                <br>
                Person 6_Remy Holler/Vancouver, Canada/Marketing strategist 
                <br>
                <br>
                </p>
            </div>

            <div id="comment" style="position: relative; left:690px; bottom: 500px; width: 260px" align="right">
            <hr>
            <p>*&nbsp</p>
                <p style="font-size: 10px;">
                2014 독일 프랑크푸르트 도서전을 관람하기 위해
                <br>같은 숙소에 머물렀던 사람들입니다.
                <br><br>
                They(voice actors) stayed at the same hostel to visit
                <br>
                Frankfurt Book Fair in germany in 2014.
                <br><br>
                </p>
            </div>



    
    </body>

    <footer style="width:1024px;">


        <div id="foot" align="left" style="position: relative; left:50px;">

           <form method="get" action="/listData_t3">
                <div style="margin-top: 10px">
                    <input type="submit" value="데이터베이스 / DataBase">
                </div>
            </form>

            <p>Taewon Kim & Gang il Yi<br>taewonnice@naver.com / giy.hands@gmail.com</p>

            <form method="get" action="/">
                <div style="margin-top: 30px">
                    <input type="submit" value="Main">
                </div>
            </form>
 
        </div>
    </footer>

</html>
"""


PLAYSOUND_PAGE_HTML = """\
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" >
        <title>번역기_1_playing</title>

        <style type="text/css">
            body {
                position: relative;
                top: 50px;
                }
            #foot {
                position: relative;
                top: 400px;
                font-size: 10px;
                }
            p {
                font-size: 12px;
                }
        </style>

    </head>

    <body>
        <div>
            <form method="get" action="/t1">
                <div>
                    <audio controls>
                        <source src="horse.ogg" type="audio/ogg">
                            Your browser does not support the audio element.
                    </audio>
                </div>
                <div style="position: relative; top: 50px" align="center">
                    <input type="submit" value="돌아가기 / BACK">
                </div>
            </form>
            <div style="position: relative; top: 200px" align="center">
                <p>
                2015 번역기 1(작업중)
                <br><br><br>
                한국어와 영어 입력이 가능합니다.
                <br>
                한국어와 영어(숫자, 특수문자 포함)를 함께 사용하는 경우에는 이미지가 출력 됩니다.
                </p>
                <p>
                KOREAN and ENGLISH are both available.
                <br>
                If you enter words in KOREAN and ENGLISH(Numbers and special characters are included) at the same time,<br>random image will be displayed.
                </p>

            </div>
        </div>
    </body>

    <footer>
        <div id="foot" align="center">
            <p>Taewon Kim & Gang il Yi<br>taewonnice@naver.com / giy.hands@gmail.com</p>
        </div>
    </footer>

</html>
"""



#################################### NDB CLASS ####################################
class WOM(ndb.Model) :
    keyword = ndb.StringProperty(indexed=True)
    content = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    idx = ndb.IntegerProperty(indexed=True)

class WOM_ENG(ndb.Model) :
    keyword = ndb.StringProperty(indexed=True)
    content = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    idx = ndb.IntegerProperty(indexed=True)

#################################### PAGES ####################################
class DelDB(webapp2.RequestHandler) :
    def get(self) :
        clearExistingDB()
        self.response.write("DB is deleted.")

class FillDB_ALL(webapp2.RequestHandler) :
    def get(self) :
        StaticKeys.keys = ""
        StaticKeys.keys_ENG = ""
        clearExistingDB()
        readAllDataFileToNdb()
        self.response.write("DB is filled.")

class FillDB_1(webapp2.RequestHandler) :
    def get(self) :
        readFileToNdb(1)
        self.response.write("DB is filled with data_1.")

class FillDB_2(webapp2.RequestHandler) :
    def get(self) :
        readFileToNdb(2)
        self.response.write("DB is filled with data_2.")

class FillDB_3(webapp2.RequestHandler) :
    def get(self) :
        readFileToNdb(3)
        self.response.write("DB is filled with data_3.")

class FillDB_4(webapp2.RequestHandler) :
    def get(self) :
        readFileToNdb(4)
        self.response.write("DB is filled with data_4.")

class SetupDB(webapp2.RequestHandler) :
    def get(self) :
        StaticKeys.keys = ""
        StaticKeys.key_ENG = ""

        StaticKeys.keys = makeKeyList()
        StaticKeys.keys_ENG = makeKeyList_ENG()

        # print StaticKeys.keys
        # print StaticKeys.keys_ENG

        print len(StaticKeys.keys)
        print len(StaticKeys.keys_ENG)


        self.response.write("DB is set.")


class ListDB_T1(webapp2.RequestHandler) :
    def get(self) :

        lenOfKORWords = ""
        lenOfENGWords = ""
        lenOfKORWords = len(StaticKeys.keys)
        lenOfENGWords = len(StaticKeys.keys_ENG)

        if lenOfKORWords == 0 :
            print ("len of KOR words is 0")
            StaticKeys.keys = ""
            StaticKeys.keys = makeKeyList()
            lenOfKORWords = len(StaticKeys.keys)
            if lenOfKORWords == 0 :
                self.response.write("KOREAN DB has to be filled first.<br> Or KOREAN DB is empty.<br>")
            print ("After makeKeyList(), lenOfKORWords : %s" % lenOfKORWords)
            # print StaticKeys.keys

        if lenOfENGWords == 0 :
            StaticKeys.key_ENG = ""
            print ("len of ENG words is 0")
            StaticKeys.keys_ENG = makeKeyList_ENG()
            lenOfENGWords = len(StaticKeys.keys_ENG)
            if lenOfENGWords == 0 :
                self.response.write("<br>ENGLISH DB has to be filled first.<br> Or ENGLISH DB is empty.<br>")
            print ("After makeKeyList(), lenOfENGWords : %s" % lenOfENGWords)
            # print StaticKeys.keys_ENG

        # list Data base

        self.response.write("<div id=\"dblist\">")
        self.response.write("<br>")

        skt = time.time()
        # list kor DB
        for i in range(0, lenOfKORWords):
            womquery = WOM.query(WOM.idx == i)
            queryReturn = womquery.fetch(1)
#            print queryReturn
#            print queryReturn[0].keyword + " : "
            self.response.write(queryReturn[0].keyword + " : <br>")
     
            resultContentList = queryReturn[0].content.split(' _ ')
            lenOfContentList = len(resultContentList)
            for j in range(0, lenOfContentList) :
#                print "- " + resultContentList[j] + "\n"
                self.response.write("- " + resultContentList[j] + "<br>")

            print ("koridx: ", i)

            self.response.write("<br>")
        ekt = time.time()
        korDur = ekt - skt
        print ("korDur: ", korDur)

        

        est = time.time()
        # list eng DB
        for i in range(0, lenOfENGWords):
            womquery = WOM_ENG.query(WOM_ENG.idx == i)
            queryReturn = womquery.fetch(1)
#            print queryReturn
#            print queryReturn[0].keyword + " : "

            self.response.write(queryReturn[0].keyword + " : <br>")
     
            resultContentList = queryReturn[0].content.split(' _ ')
            lenOfContentList = len(resultContentList)
            for j in range(0, lenOfContentList) :
#                print "- " + resultContentList[j] + "\n"
                self.response.write("- " + resultContentList[j] + "<br>")

            print ("engidx: ", i)
            self.response.write("<br>")

        eet = time.time()
        engDur = eet - ekt
        print ("engDur: ", engDur)
        self.response.write("</div>")
         
 
        # list imgs in DB
        self.response.write("<div id=\"imgs\">")
        self.response.write("<br>")
       
        ist = time.time()
        for i in range(1, IMG_NUMBER) :
            self.response.out.write('<br>')
            self.response.out.write('<div id=\"aimg\" align = "left"> <img src=/img/' + str(i) + '.png height = "400" width = "400"/></div>')
            self.response.out.write('<br>')
        
        self.response.write("</div>")
       
        iet = time.time()
        imgDur = iet - ist
        print ("imgDur: ", imgDur)
        self.response.out.write(LIST_DB_T1_PAGE_HTML)


class ListDB_T2(webapp2.RequestHandler) :
    def get(self) :
        self.response.out.write(LIST_DB_T2_PAGE_HTML)


class ListDB_T3(webapp2.RequestHandler) :
    def get(self) :
        self.response.out.write(LIST_DB_T3_PAGE_HTML)


class FindDB(webapp2.RequestHandler) :
    def get(self) :
        lenOfKORWords = ""
        lenOfENGWords = ""
        lenOfKORWords = len(StaticKeys.keys)
        lenOfENGWords = len(StaticKeys.keys_ENG)
        print ("lenOfKORWords : %s" % lenOfKORWords)
        print ("lenOfENGWords : %s" % lenOfENGWords)
        #os.system('say wait')
        #print sys.platform
        # imgPrinted = False
        toFindstr = ' '
        # numOfmatch = 0
        #print keys
        toFind = self.request.get('searchingWord') #unicode
        if toFind == "" :
            # print ("nothing is in.")
            randImgDisplay(self, IMG_NUMBER)
        else :
            if lenOfKORWords == 0 :
                print ("len of KOR words is 0")
                StaticKeys.keys = ""
                StaticKeys.keys = makeKeyList()
                lenOfKORWords = len(StaticKeys.keys)
                if lenOfKORWords == 0 :
                    self.response.write("KOREAN DB has to be filled first.<br> Or KOREAN DB is empty.<br>")
                print ("After makeKeyList(), lenOfKORWords : %s" % lenOfKORWords)
                # print StaticKeys.keys

            if lenOfENGWords == 0 :
                StaticKeys.key_ENG = ""
                print ("len of ENG words is 0")
                StaticKeys.keys_ENG = makeKeyList_ENG()
                lenOfENGWords = len(StaticKeys.keys_ENG)
                if lenOfENGWords == 0 :
                    self.response.write("<br>ENGLISH DB has to be filled first.<br> Or ENGLISH DB is empty.<br>")
                print ("After makeKeyList(), lenOfENGWords : %s" % lenOfENGWords)
                # print StaticKeys.keys_ENG


            if lenOfKORWords != 0 and lenOfENGWords != 0 :
                toFindstr = toFind.encode('utf-8')
                toFindstrList = toFindstr.split(' ')
                resultSentence = " "

                isKoreanToListResult = isKoreanToList(toFindstrList)

                if isKoreanToListResult == 0 : #All kor words
                    if isExactlyMatchToList(toFindstrList, StaticKeys.keys) and len(toFindstrList) == 1:
                        for word in toFindstrList: #split by space
                            result = randDBOutInMatchingWord(WOM, word)
                            self.response.write('<div align = "center", padding-top: 50px>' \
                            + result + '</div>')
                            resultEng = randDBOutInRandomWord(WOM_ENG, lenOfENGWords)
                            self.response.write('<div align = "center", padding-top: 50px>' \
                            + resultEng + '</div>')

                    else :
                        resultSentence = randDBOutInRandomWord(WOM, lenOfKORWords)
                        self.response.write('<div align = "center", padding-top: 50px>' \
                        + resultSentence + '</div>')
                        resultSentence = randDBOutInRandomWord(WOM_ENG, lenOfENGWords)
                        self.response.write('<div align = "center", padding-top: 50px>' \
                        + resultSentence + '</div>')


                elif isKoreanToListResult == 1 : #All eng words
                    if isExactlyMatchToList(toFindstrList, StaticKeys.keys_ENG) and len(toFindstrList) == 1:
                        for word in toFindstrList: #split by space
                            resultEng = randDBOutInRandomWord(WOM, lenOfKORWords)
                            self.response.write('<div align = "center", padding-top: 50px>' \
                            + resultEng + '</div>')
                            result = randDBOutInMatchingWord(WOM_ENG, word)
                            self.response.write('<div align = "center", padding-top: 50px>' \
                            + result + '</div>')

                    else :
                        resultSentence = randDBOutInRandomWord(WOM, lenOfKORWords)
                        self.response.write('<div align = "center", padding-top: 50px>' \
                        + resultSentence + '</div>')
                        resultSentence = randDBOutInRandomWord(WOM_ENG, lenOfENGWords)
                        self.response.write('<div align = "center", padding-top: 50px>' \
                        + resultSentence + '</div>')

                elif isKoreanToListResult == 2 : #kor + eng
                    randImgDisplay(self, IMG_NUMBER)

        self.response.out.write(FIND_PAGE_HTML)



################################### 2014_12 ~ 1 ####################################
class Translator_Main(webapp2.RequestHandler) :
    # print (sys.getdefaultencoding())
    def get(self) :
        self.response.out.write(T0_PAGE_HTML)

class Translator_1(webapp2.RequestHandler) :
    # print (sys.getdefaultencoding())
    def get(self) :
        self.response.out.write(T1_PAGE_HTML)

class Translator_2(webapp2.RequestHandler) :
    # print (sys.getdefaultencoding())
    def get(self) :
        self.response.out.write(T2_PAGE_HTML)

class Translator_3(webapp2.RequestHandler) :
    # print (sys.getdefaultencoding())
    def get(self) :
        self.response.out.write(T3_PAGE_HTML)

class playSound(webapp2.RequestHandler) :
    # print (sys.getdefaultencoding())
    def get(self) :
        self.response.out.write(PLAYSOUND_PAGE_HTML)




#################################### FUNCTIONS ####################################
def randImgDisplay(target, maxImgNum) :
    ranImgNum = random.randint(1, maxImgNum)
    target.response.out.write('<div align = "center", padding-top: 100px>\
        <img src=/img/' + str(ranImgNum) + '.png height = "400" width = "400"/></div>')


def isExactlyMatch(word, DBList) :
    # print len(DBList)
    lenOfDB = len(DBList)
    for j in range(0, lenOfDB) :
        # print wordList[i]
        print j
        print DBList[j]
        if DBList[j] == word :
            print "Exactly same!!"
            return True
        else:
            if j == (lenOfDB - 1) :
                print "Not same!!"
                return False

def isExactlyMatchToList(wordList, DBList) :
    same = 0
    # print len(DBList)
    # print len(wordList)
    lenOfWordList = len(wordList)
    lenOfDB = len(DBList)
    for i in range(0, lenOfWordList) :
        for j in range(0, lenOfDB) :
            # print wordList[i]
            # print j
            # print DBList[j]
            if DBList[j] == wordList[i] :
                same = same + 1
                break
        # print ("same : %s " % same)

    if same == lenOfWordList :
        print "Exactly same!!"
        return True
    else :
        print "Not same!!"
        return False


def randDBOutInRandomWord(dataBase, DBLength) :
    print ("DBLength : %s" % DBLength)
    randomIdx = random.randint(0, DBLength - 1)
    print ("randomIdx : %s" % randomIdx)
    womquery = dataBase.query(dataBase.idx == randomIdx)
    queryReturn = womquery.fetch(1)
    # print queryReturn
    resultContentList = queryReturn[0].content.split(' _ ')
    # print resultContentList
    randomResult = resultContentList[random.randint(0, len(resultContentList) - 1)]
    randomResultStr = randomResult.encode('utf-8')
    return randomResultStr


def randDBOutInMatchingWord(dataBase, matchingWord) :
    womquery = dataBase.query(dataBase.keyword == matchingWord)
    queryReturn = womquery.fetch(1)
    resultContentList = queryReturn[0].content.split(' _ ')
    randomResult = resultContentList[random.randint(0, len(resultContentList) - 1)]
    randomResultStr = randomResult.encode('utf-8')
    return randomResultStr

def coin() :
    return random.randint(1, 2)

def makeKey(wordToTrans = DEFAULT) :
    return ndb.Key("Words", wordToTrans)

def clearExistingDB() :
    allwomqueries = WOM.query().fetch(9999, keys_only = True)
    allwomqueries_ENG = WOM_ENG.query().fetch(9999, keys_only = True)
    #'_multi' 함수의 인자인 keys 를 만들기 위해서는 keys_only 옵션을 이용해서 entity가 아니라 key만 return 되도록 해야 한다.
    ndb.delete_multi(allwomqueries)
    ndb.delete_multi(allwomqueries_ENG)
    ndb.get_context().clear_cache()

def readFileToNdb(numOfDB) :
    global korIdx
    global engIdx
    
    if numOfDB == 1:
        f = open(DATA_FILE_1, 'r')
    elif numOfDB == 2:
        f = open(DATA_FILE_2, 'r')
    elif numOfDB == 3:
        f = open(DATA_FILE_3, 'r')
    elif numOfDB == 4:
        f = open(DATA_FILE_4, 'r')

    key_list = []
    lines = f.readlines()
    for line in lines:
        #print type(line)
        tline = line.split(" : ") #: 으로 나누는 것과 ' : '으로 나누는 것은 dic이 되었을 때 결과값이 다르다.
        key = tline[0]
        #print key
        escapeNvalue = tline[1][:(len(tline[1]) - 1)] #마지막 문자인 '\n'을 제거한다.
        #print escapeNvalue

        if isKorean(key) :
            wom = WOM(parent = makeKey(key))
            wom.keyword = key
            wom.content = escapeNvalue
            wom.idx = korIdx
            wom.put()
            korIdx = korIdx + 1

        else :
            wom = WOM_ENG(parent = makeKey(key))
            wom.keyword = key
            wom.content = escapeNvalue
            wom.idx = engIdx
            wom.put()
            engIdx = engIdx + 1
    f.close()

def readAllDataFileToNdb() :
    korIdx = 0
    engIdx = 0
    key_list = []
    f = open(DATA_FILE, 'r')
    lines = f.readlines()
    for line in lines:
        # print type(line)
        # print line
        tline = line.split(" : ") #: 으로 나누는 것과 ' : '으로 나누는 것은 dic이 되었을 때 결과값이 다르다.
        key = tline[0]
        # print key
        escapeNvalue = tline[1][:(len(tline[1]) - 1)] #마지막 문자인 '\n'을 제거한다.
        #print escapeNvalue

        if isKorean(key) :
            wom = WOM(parent = makeKey(key))
            wom.keyword = key
            wom.content = escapeNvalue
            wom.idx = korIdx
            wom.put()
            korIdx = korIdx + 1


        else :
            wom = WOM_ENG(parent = makeKey(key))
            wom.keyword = key
            wom.content = escapeNvalue
            wom.idx = engIdx
            wom.put()
            engIdx = engIdx + 1
    f.close()

    print ("korIdx : %s" % korIdx)
    print ("engIdx : %s" % engIdx)


#정규표현식을 이용하여 한글이 포함되어 있는지를 판단한다.
def isKorean(word) :
    return bool(re.search(r'(([\x7f-\xfe])+)', word))

def isKoreanToWord(word) :
    if bool(re.search(r'(([\x7f-\xfe])+)', word)) :
        if bool(re.search(r'(([^\x7f-\xfe])+)', word)) :
            #mixed
            print "The word is korean + english"
            return 2 #kor + eng
        else :
            #korean
            print "The word is korean"
            return 0 #All kor

    else :
        #english or number or special key...
        print "The word is english"
        return 1 #All eng

def isKoreanToList(wordList) :
    numOfWord = len(wordList)
    # print numOfWord
    kor = 0
    eng = 0
    mixed = 0
    if numOfWord != 0 :
        for word in wordList :
            isKoreanResult = isKoreanToWord(word)

            if isKoreanResult == 0 :
                kor = kor + 1
                # print ("kor : %s " % kor)
            elif isKoreanResult == 1 :
                eng = eng + 1
                # print ("eng : %s " % eng)
            else :
                mixed = mixed + 1

        if mixed != 0 :
            print "The wordlist is Mixed"
            return 2 #kor + eng
        elif eng == 0 and kor > 0:
            print "The wordlist is korean"
            return 0 #kor
        elif kor == 0 and eng > 0 :
            print "The wordlist is english"
            return 1 #All eng
        else :
            print "The wordlist is Mixed"
            return 2 #kor + eng


# def isKoreanToList(wordList) :
#     numOfWord = len(wordList)
#     # print numOfWord
#     kor = 0
#     eng = 0
#     if numOfWord != 0 :
#         for word in wordList :
#             if isKorean(word) :
#                 kor = kor + 1
#                 # print ("kor : %s " % kor)
#             else :
#                 eng = eng + 1
#                 # print ("eng : %s " % eng)

#         if eng == 0 :
#             print "The wordlist is korean"
#             return 0 #All kor

#         elif kor == 0 :
#             print "The wordlist is ENGLISH"
#             return 1 #All eng

#         else :
#             print "The wordlist is korean + ENGLISH"
#             return 2 #kor + eng



#긴 단어부터, 뒷 철자부터 정열된 keyList 를 만든다.
def makeKeyList() :
    womquery = WOM.query().order(-WOM.keyword)
    key_list = []
    for wom in womquery :
        key = wom.keyword.encode('utf-8')
        #print key
        key_list.append(key) # make key list
    return key_list

def makeKeyList_ENG() :
    womquery = WOM_ENG.query().order(-WOM_ENG.keyword)
    key_list = []
    for wom in womquery :
        key = wom.keyword.encode('utf-8')
        # print key
        key_list.append(key) # make key list
    # print ("key_list : %s" % key_list)
    return key_list

#targetFolder에 들어있는 특정 확장자 파일의 갯수를 돌려준다.
#Not using at online version yet. 
def getFileNum(targetFolder, extension) :
    listOfFiles = glob.glob(targetFolder + '/*.' + extension)
    return len(listOfFiles)



application = webapp2.WSGIApplication([
    ('/delData', DelDB),
    ('/fillData', FillDB_ALL),
    ('/fillData_1', FillDB_1),
    ('/fillData_2', FillDB_2),
    ('/fillData_3', FillDB_3),
    ('/fillData_4', FillDB_4),
    ('/setData', SetupDB),
    ('/findData', FindDB),
    ('/listData_t1', ListDB_T1),
    ('/listData_t2', ListDB_T2),
    ('/listData_t3', ListDB_T3),

    ('/', Translator_Main),
    ('/t1', Translator_1),
    ('/t2', Translator_2),
    ('/t3', Translator_3),

    ('/playSound', playSound)    


    ], debug=True)








