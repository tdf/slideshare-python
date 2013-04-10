%#generate HTML table of all tags
<table border="1">
  <tr>
    <th>Tag name</th>
  </tr>
%for tag in tags:
  <tr>
    <td><a href="{{tag}}/">{{tag}}</a></td>
  </tr>
%end
</table>
