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