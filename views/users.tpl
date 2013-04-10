%#generate HTML table of all users
<table border="1">
  <tr>
    <th>Username</th>
    <th>Description</th>
  </tr>
%for user, desc in users.items():
  <tr>
    <td><a href="{{user}}/">{{user}}</a></td>
    <td><a href="{{user}}/">{{desc}}</a></td>
  </tr>
%end
</table>
