<html>
<head>
 <meta charset="utf-8"/>
 <title>SlideShare Python</title>
 <link rel="stylesheet" href="http://code.jquery.com/ui/1.10.2/themes/smoothness/jquery-ui.css" />
 <script src="http://code.jquery.com/jquery-1.9.1.js"></script>
 <script src="http://code.jquery.com/ui/1.10.2/jquery-ui.js"></script>
 <style>
   #src-deck { list-style-type: none; margin: 0; padding: 0; height: 60%}
   #src-deck li { margin: 3px 3px 3px 0; padding: 1px; float: left; width: 100px; height: 90px; font-size: 4em; text-align: center; }
   #drop-target { list-style-type: none; margin: 0; padding: 0; height: 60%}
   #drop-target li { margin: 3px 3px 3px 0; padding: 1px; float: left; width: 100px; height: 90px; font-size: 4em; text-align: center; }
   .slide {
       position: relative;
	   border: 1px solid #d3d3d3;
	   font-weight: normal;
	   color: #555555;
   }
   .slide-number { position: relative; font-size: 0.5em; position: absolute; bottom: 0; right: 0; }

   h1 { padding: .2em; margin: 0; }
   #decks { float:left; width: 500px; margin-right: 2em; }
   #slidegroup { width: 200px; float: left; margin-top: 1em; }
   #slidegroup ul { margin: 0; padding: 1em 0 1em 3em; }
 </style>
 <script>
   $(function() {
     var $accordion = $( "#accordion" );
     $.getJSON('../../api/users/{{user}}/decks/', function(jsonData) {
       $.each(jsonData, function(){
         var src_deck = this;
         var $curr_deck = $accordion.append("<h2><a href='#'>" + src_deck + "</a></h2><div><ul id='src-deck'></ul></div>").find("div > ul").last();
         $.getJSON('../../api/users/{{user}}/decks/' + src_deck + '/', function(jsonData) {
           var last_rev = jsonData[jsonData.length-1];
           $.getJSON('../../api/users/{{user}}/decks/' + src_deck + '/' + last_rev + '/', function(jsonData) {
             $.each(jsonData, function(){
               $curr_deck.append("<li class='slide' style='background: #e6e6e6 url(../../users/{{user}}/decks/" + src_deck + "/" + last_rev + "/" + this + "/thumbnail.png) 50% 50% repeat-x;'><div class='slide-number'>" + this + "</div></li>").children().last().draggable({
                 cancel: "a.ui-icon",
                 appendTo: "body",
                 revert: "invalid",
                 containment: "document",
                 helper: "clone",
                 cursor: "move",
                 start: function(event, ui) {
                    ui.helper.css({ height: 100, width: 100 });
                 },
               });;
             });
           });
         });
       });
       $accordion.accordion();
     });
     var trash_icon = "<a href='link/to/trash/script/when/we/have/js/off' title='Delete this slide' class='ui-icon ui-icon-trash'>Delete Slide</a>";
     $( "#slidegroup ul" ).droppable({
       activeClass: "ui-state-default",
       hoverClass: "ui-state-hover",
       accept: ":not(.ui-sortable-helper)",
       drop: function( event, ui ) {
           $( this ).find( ".placeholder" ).remove();
           ui.draggable.clone().hide().append( trash_icon ).
           click(function( event ) {
             var $item = $( this ),
             $target = $( event.target );
             if ( $target.is( "a.ui-icon-trash" ) ) {
               $item.fadeOut( 750, function() {
                 $( this ).remove();
               });
             }
             return false;
           }).appendTo( this ).fadeIn();
       }
     });
     $( "#decks" ).width("45%");
     $( "#slidegroup" ).width("45%");
   });
 </script>
</head>
<body>
 <div id="decks">
  <h1 class="ui-widget-header">Decks</h1>
  <div id="accordion">
  </div>
 </div>
 <div id="slidegroup">
  <h1 class="ui-widget-header">New Group</h1>
  <div class="ui-widget-content">
    <ul id="drop-target">
      <li class="placeholder" style="font-size: 1em; text-align: center;">Drag your slides here!</li>
    </ul>
  </div>
 </div>

</body>
</html>
