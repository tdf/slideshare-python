%#generate HTML table of all revisions
<table border="1">
%for rev in revs:
  <tr>
    <td><a href="{{rev}}/">Revision {{rev}}</a></td>
    <td><a href="{{rev}}/deck.odp"><img src="{{rev}}/thumbnail.png"></a></td>
  </tr>
%end
</table>
