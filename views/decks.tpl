%#generate HTML table of all decks
<table border="1">
%for deckname in decks:
  <tr>
    <td><a href="{{deckname}}/">{{deckname}}</a></td>
    <td><a href="{{deckname}}/"><img src="{{deckname}}/thumbnail.png"></a></td>
  </tr>
%end
</table>
