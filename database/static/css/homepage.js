
  $(document).ready(function(){
    work();
    setInterval(function(){
      var element = document.getElementById("notifnum")
      var oldvalue = parseInt(element.innerHTML)
      $.ajax({
        type:"POST",
        url: '/main/is_there_notifications',
        data: {
             notifnum:oldvalue,
             csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(response){
          if(response.hasOwnProperty('notifnum')){
            //toastr["success"]("New notification")
            element.innerHTML = response["notifnum"]
            element.style.visibility = 'visible';
          }else{
            element.style.visibility = 'hidden';
            console.log("server responded Nothing new")
          }
          
        }
    });
    }, 1000);
   })
   function work(){
     toastr.options = {
       "closeButton": true,
       "debug": true,
       "newestOnTop": false,
       "progressBar": true,
       "positionClass": "toast-top-right",
       "preventDuplicates": false,
       "showDuration": "300",
       "hideDuration": "1000000",
       "timeOut": "5000",
       "extendedTimeOut": "1000",
       "showEasing": "swing",
       "hideEasing": "linear",
       "showMethod": "fadeIn",
       "hideMethod": "fadeOut"
       }
       $("#form-post").submit(function(e) {
         e.preventDefault();    
         var formData = new FormData(this);
         if($("#text-content").val()!=""){
           $.ajax({
             url: "/home/create_post",
             type: 'POST',
             data: formData,
             success: function (data) {
               toastr["success"]("Posted Successfully");
               var feeds = document.getElementById("feeds")
               document.getElementById("form-post").reset();
               $("#feeds").prepend(data["newpost"])
               //work(); // this is causing the multi post problem when submit
               
             },
             cache: false,
             contentType: false,
             processData: false
         });
         }else{
           toastr["error"]("Posting Failed Empty Post");
         }  
     });  
     
     // script concerned with posts
     $(document).on("click",".like",function(){
       var fbtn = $(this);
       if (fbtn.hasClass('like')) {
         console.log("like")
         $.ajax({
           type:"POST",
           url: "/main/like_post",
           data: {
                post_id:fbtn.val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
           },
           success: function(response){
               console.log("request sent")
           }
       });
         fbtn.removeClass('like').addClass('unlike');
         fbtn.html('<span id="like{{post.id}}span" class="bi bi-hand-thumbs-up-fill" style="color:#11C9EA">');
         var element = document.getElementById("num"+fbtn.val())
         var oldvalue = parseInt(element.innerHTML)
         element.innerHTML = oldvalue + 1
       } else {
         console.log("unlike")
         $.ajax({
             type:"POST",
             url: '/main/remove_like_post',
             data: {
                  post_id:fbtn.val(),
                  csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
             },
             success: function(response){
                 console.log("friend request have been removed")
                 fbtn.removeClass('unlike').addClass('like');
                 fbtn.html('<span id="like{{post.id}}span" class="bi bi-hand-thumbs-up-fill" style="color:None">');
                 var element = document.getElementById("num"+fbtn.val())
                 var oldvalue = parseInt(element.innerHTML)
                 console.log(oldvalue)
                 element.innerHTML = oldvalue - 1
                 
             }
         });
         
       }
   
     })
     $(document).on("click",".unlike",function(){
       var fbtn = $(this);
       if (fbtn.hasClass('unlike')) {
         console.log("unlike")
         $.ajax({
           type:"POST",
           url: '/main/remove_like_post',
           data: {
                post_id:fbtn.val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
           },
           success: function(response){
               console.log("request sent")
           }
       });
       fbtn.removeClass('unlike').addClass('like');
       fbtn.html('<span id="like{{post.id}}span" class="bi bi-hand-thumbs-up-fill" style="color:None">');
       var element = document.getElementById("num"+fbtn.val())
       var oldvalue = parseInt(element.innerHTML)
       console.log(oldvalue)
       element.innerHTML = oldvalue -1
       } else {
         console.log("unfriend")
         $.ajax({
             type:"POST",
             url: '/main/like_post',
             data: {
                  post_id:fbtn.val(),
                  csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
             },
             success: function(response){
               fbtn.removeClass('like').addClass('unlike');
               fbtn.html('<span id="like{{post.id}}span" class="bi bi-hand-thumbs-up-fill" style="color:#11C9EA">');
               var element = document.getElementById("num"+fbtn.val())
               var oldvalue = parseInt(element.innerHTML)
               console.log(oldvalue)
               element.innerHTML = oldvalue + 1
             }
         });
       
       }
   
     })
 
     $(document).on("click",".delete",function(){
       console.log("is called delete")
       var fbtn = $(this);
       $(fbtn).click(function(){
           console.log("remove-post ajax called")
           $.ajax({
             type:"POST",
             url: '/main/remove_post',
             data: {
                  post_id:fbtn.val(),
                  csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
             },
             success: function(response){
                 console.log("remove post request"+fbtn.val())
                 var element = document.getElementById("post-container"+fbtn.val())
                 var elementfooter = document.getElementById("post-footer"+fbtn.val())
                 var elementclose = document.getElementById("close-"+fbtn.val())
                 elementclose.click()
                 element.parentNode.removeChild(element);
                 elementfooter.parentNode.removeChild(elementfooter)
             }
           });
         });
     });
    return false
   }
   //Get the button
 var mybutton = document.getElementById("myBtn");
 
 // When the user scrolls down 20px from the top of the document, show the button
 window.onscroll = function() {scrollFunction()};
 
 function scrollFunction() {
   if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
     mybutton.style.display = "block";
   } else {
     mybutton.style.display = "none";
   }
 }
 
 // When the user clicks on the button, scroll to the top of the document
 function topFunction() {
   document.body.scrollTop = 0;
   document.documentElement.scrollTop = 0;
 }