<%inherit file="pyramid_blogr:templates/layout.mako"/>

<h1>${entry.title}</h1>
<hr/>
<p>${entry.body}</p>
<hr/>
<p>Created <strong title="${entry.created}">
${entry.created_in_words}</strong> ago</p>

<p><a href="${request.route_url('home')}">Go Back</a></p>