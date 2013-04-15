%#generate HTML table of all decks
<table border="1">
  <tr>
    <th colspan=2><b>Decks</b></th>
  </tr>
%for deckname in decks:
  <tr>
    <td><a href="decks/{{deckname}}/">{{deckname}}</a></td>
    <td><a href="decks/{{deckname}}/"><img src="decks/{{deckname}}/thumbnail.png"></a></td>
  </tr>
%end
  <tr>
    <th colspan=2><b>Groups</b></th>
  </tr>
%for groupname in groups:
  <tr>
    <td><a href="groups/{{groupname}}/">{{groupname}}</a></td>
    <td><a href="groups/{{groupname}}/"><img src="groups/{{groupname}}/thumbnail.png"></a></td>
  </tr>
%end
</table>
