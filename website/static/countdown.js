document.addEventListener('DOMContentLoaded', function(){    
    var totalCount = document.getElementById("countdown").innerText.split(":")[1];
    console.log(totalCount)
    // if(totalCount.includes("None")){

    //     console.log("No Timer")
    // }
    // else{
                // Countdown initiate for one session - Comment Below
        localStorage.removeItem("saved_countdown");

        var saved_countdown = localStorage.getItem('saved_countdown');
        if(saved_countdown == null) {
            s = totalCount.trim();
            localStorage.setItem('saved_countdown', s);
        }
        else{
            s = saved_countdown;
        }
    
        var c = document.getElementById("count");
        
        var tick = function(){
            if(s > totalCount/2){
                c.setAttribute("class", "fw-bold text-success")
            }
            if(s < totalCount/2){
                c.setAttribute("class", "fw-bold text-warning")
            }
            if(s < totalCount/6){
                c.setAttribute("class", "fw-bold text-danger")
            }
            c.innerText = "Time Remaining : " + s;
            localStorage.setItem('saved_countdown', s);
        };
        
        var ready = function(){
        clearInterval(i);
        c.setAttribute("class", "fw-bold text-danger")
        c.innerText = "FINISH";
        document.getElementById('submit').click()
        };
        
        var realConfirm=window.confirm;
            window.confirm=function(){
            window.confirm=realConfirm;
            return true;
        };

        tick();
        
        var i = setInterval(function(){
            if(s>0){
                s--;
                tick();
            }
            else{
                ready()
            }
        }, 1000);    
    }
// }
, false);

// function countdown(s){

//     var c = document.getElementById("count");
     
//     var tick = function(){    
//        c.innerText = s;
//     };
     
//     var ready = function(){
//       clearInterval(i);
//       c.innerText = "ready";
//       document.getElementById('submit').click()
        
//     };
    
//     var realConfirm=window.confirm;
//         window.confirm=function(){
//         window.confirm=realConfirm;
//         return true;
//     };

//     tick();
    
//     var i = setInterval(function(){
//         if(s>0){
//             s--;
//             tick();
//         }
//         else{
//             ready()
//         }
//         // (s>0) ? function(){ s--;tick(); }() : ;
//     }, 1000);
    
    
// }