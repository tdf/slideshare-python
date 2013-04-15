%#generate HTML table of all decks
<table border="1">
%for groupname in groups:
  <tr>
    <td><a href="{{groupname}}/">{{groupname}}</a></td>
    <td><a href="{{groupname}}/"><img src="{{groupname}}/thumbnail.png"></a></td>
  </tr>
%end
</table>
