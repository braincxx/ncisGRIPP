$(function() {
	
   $(".input input").focus(function() {
      $(this).parent(".input").each(function() {
         $("label", this).css({
			"color": "#FFFFFF",
			"opacity": "0",
            "line-height": "0px",
            "font-size": "10px",
            "font-weight": "100",
            "top": "16px"
         })
         $(".spin", this).css({
            "width": "100%"
         })
      });
   }).blur(function() {
      $(".spin").css({
         "width": "0px"
      })
      if ($(this).val() == "") {
         $(this).parent(".input").each(function() {
            $("label", this).css({
               "line-height": "60px",
               "font-size": "19px",
               "font-weight": "300",
               "top": "10px",
			   "opacity": "1",
               "color": "#808080"
            })
         });

      }
   });

   $(".button").click(function(e) {
      var pX = e.pageX,
         pY = e.pageY,
         oX = parseInt($(this).offset().left),
         oY = parseInt($(this).offset().top);

      $(this).append('<span class="click-efect x-' + oX + ' y-' + oY + '" style="margin-left:' + (pX - oX) + 'px;margin-top:' + (pY - oY) + 'px;"></span>')
      $('.x-' + oX + '.y-' + oY + '').animate({
         "width": "500px",
         "height": "500px",
         "top": "-250px",
         "left": "-250px",

      }, 600);   
      $("button", this).addClass('active');
   })

	/* Button */
   $(".alt-2").click(function() {
      if (!$(this).hasClass('material-button')) {	  
		$(".materialContainer").css({
			"top": "30%"})
		
         $(".shape").css({
            "width": "100%",
            "height": "300%",
            "transform": "rotate(0deg)"
         })

         setTimeout(function() {
            $(".overbox").css({
               "overflow": "initial"
            })
         }, 600)

         $(this).animate({
            "width": "45px", /* x size of circle */
            "height": "45px" /* y */ 
         }, 500, function() {
            $(".box").removeClass("back");

            $(this).removeClass('active')
         });

         $(".overbox .title").fadeOut(300);
         $(".overbox .input").fadeOut(300);
         $(".overbox .input input").css({"font-size": "17px"})
         $(".overbox .button").fadeOut(300);

         $(".alt-2").addClass('material-buton');
      }

   })

   $(".material-button").click(function() {

      if ($(this).hasClass('material-button')) {
         setTimeout(function() {
            $(".overbox").css({
               "overflow": "hidden"
            })
            $(".box").addClass("back");
         }, 200)
         $(".materialContainer").css({"top": "35%"})

         $(this).addClass('active').animate({
            "width": "900px",
            "height": "900px"
         });

         setTimeout(function() {
            $(".shape").css({
               "width": "90%", /* locate of plus */
               "height": "75%",
               "top": "-6%",
               "transform": "rotate(45deg)"
            })
			$(".material-button").css({"width": "45px", "height": "45px"})
            $(".overbox .title").fadeIn(300);
            $(".overbox .input").fadeIn(300);
            $(".overbox .button").fadeIn(300);
         }, 700)

         $(this).removeClass('material-button');

      }

      if ($(".alt-2").hasClass('material-buton')) {
         $(".materialContainer").css({"top": "50%"})
         $(".alt-2").removeClass('material-buton');
         $(".alt-2").addClass('material-button');
      }

   });

});