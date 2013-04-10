%#generate HTML table of all slides in one revision
<table border="1">
%for name, content in revmeta.items():
  <tr>
    <td>{{name}}</td>
    <td>{{content}}</td>
  </tr>
%end
</table>
<table border="1">
%for slide in slides:
  <tr>
    <td><a href="{{slide}}/slide.odp">Slide {{slide}}</a></td>
    <td><a href="{{slide}}/slide.odp"><img src="{{slide}}/thumbnail.png"></a></td>
  </tr>
%end
</table>
