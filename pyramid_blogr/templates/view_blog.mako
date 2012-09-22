<%inherit file="pyramid_blogr:templates/layout.mako"/>

<h1>${entry.title}</h1>
<hr/>
<p>${entry.body}</p>
<hr/>
<p>Created <strong title="${entry.created}">
${entry.created_in_words}</strong> ago</p>

<p><a href="${request.route_url('home')}">Go Back</a> ::
<a href="${request.route_url('blog_action', action='edit',
_query=(('id',entry.id),))}">Edit Entry</a>

</p>