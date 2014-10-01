%#generate HTML table of all decks
<table border="1">
%for deckname in decks:
  <tr>
    <td><a href="{{deckname}}/">{{deckname}}</a></td>
    <td><a href="{{deckname}}/"><img src="{{deckname}}/thumbnail.png"></a></td>
  </tr>
%end
</table>

<form action="/users/{{user}}/decks/" method="post" enctype="multipart/form-data">
<h1>Upload new deck</h1>
<p>Name <input name="name" type="text"/>
    <input name="file" type="file"/>
    tag <input name='tag' type='text'/>
    <input type="submit" value='Upload'/></p>
</form>
