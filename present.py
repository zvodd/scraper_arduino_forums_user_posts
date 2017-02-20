from arduino_forum_user_posts.db_api import PostEntry
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import desc, asc

from jinja2 import DictLoader, Environment


templates = {"page":
"""
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title></title>
	<link rel="stylesheet" href="">
</head>
<body>
<table>
	{% for post in posts %}
		<tr>
			<td>
			<div><a href="{{post.post_id}}"><h2>{{post.title|safe}}</h2></a></div>
			<div>{{post.description.decode('utf8') |safe}}</div>
			</td>
		</tr>
	{% endfor %}
</table>
</body>
</html>
"""
}
env = Environment(loader=DictLoader(templates))
tmpl = env.get_template("page")

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('dbfile')
	args = parser.parse_args()

	Session = sessionmaker()
	engine = create_engine('sqlite:///'+args.dbfile)
	Session.configure(bind=engine)

	import ipdb; #ipdb.set_trace()

	# work with the session
	session = Session()
	items = session.query(PostEntry).order_by(desc(PostEntry.id)).all()
	session.close()
	
	output = tmpl.render(posts=items)
	open("output.html", 'w').write(output)