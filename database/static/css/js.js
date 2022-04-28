// let div = document.createElement("div");
// let p = document.createElement("p");
// let span = document.createElement("span");
// div.append(p);
// div.prepend(span);

const { get } = require("lodash");







function append_to_div(add_com, data){
    document.getElementById(add_com).innerText += data;
}

document.getElementById("combutton").addEventListener('click',function(){

    var comment=document.getElementById("datacomment");
    var value = comment.value.trim();
              
            if(!value){
                alert("Name Cannot be empty!");  }
            else{

                append_to_div("ad" ,value+"/n");
                comment.value=";"
            }

});



function likebutton(){
    let heart=document.querySelector('.heart');
    // let likes=document.querySelector('.likes');
    var like=parseInt(document.getElementById('likes'));
    if(heart.src.match("heart.png")){
        heart.src="heart_red.png";
       likes.innerHTML=like+1;
       
    }
    else
        heart.src="heart.png";
        likes.innerHTML="";

    }





