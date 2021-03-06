<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
    </head>
    <body>
        <div class="ui container" style="padding-top: 10px;">
        <table class="ui celled table">
            <thead>
                <th>Title</th>
                <th>Author</th>
                <th>#Likes</th>
                <th>#Comments</th>
                <th>Label</th>
                <th>Check</th>
            </thead>
            <tbody>
                %for row in good:
                <tr class="positive">
                    <td><a href="{{ row.url }}">{{ row.title }}</a></td>
                    <td>{{ row.author }}</td>
                    <td>{{ row.points }}</td>
                    <td>{{ row.comments }}</td>
                    <td>Good</td>
                    <td><a href="/add_label_recs/?label=good&id={{ row.id }}">Correct</a></td>
                </tr>
                %end
                %for row in maybe:
                <tr class="active">
                    <td><a href="{{ row.url }}">{{ row.title }}</a></td>
                    <td>{{ row.author }}</td>
                    <td>{{ row.points }}</td>
                    <td>{{ row.comments }}</td>
                    <td>Maybe</td>
                    <td><a href="/add_label_recs/?label=maybe&id={{ row.id }}">Correct</a></td>
                </tr>
                %end
                %for row in never:
                <tr class="negative">
                    <td><a href="{{ row.url }}">{{ row.title }}</a></td>
                    <td>{{ row.author }}</td>
                    <td>{{ row.points }}</td>
                    <td>{{ row.comments }}</td>
                    <td>No</td>
                    <td><a href="/add_label_recs/?label=never&id={{ row.id }}">Correct</a></td>
                </tr>
                %end
            </tbody>
        </table>
        </div>
    </body>
</html>