#print 'Content-Type: text/plain'
#print ''
#print 'hello, world!'

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db
import cgi
import os

class Greeting(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline = True)
    date = db.DateTimeProperty(auto_now_add = True)

class MainPage(webapp.RequestHandler):
    def get(self):
        #self.response.out.write('''
        #    <!DOCTYPE html>
        #    <html>
        #        <head>
        #            <meta charset="utf-8">
        #            <title>guestbook</title>
        #            <link type="text/css" rel="stylesheet" href="stylesheets/guestbook.css">
        #        </head>
        #        <body>
        #            <div id="header">
        #                <h1>''')

        user = users.get_current_user()

        #if user:
        #    self.response.headers['Content-Type'] = 'text/plain'
        #    self.response.out.write('hello, <span>' + user.nickname() + '</span>! welcome to <span>guestbook</span>!</h1>')
        #    self.response.out.write('<a id="login_link" href="%s">log out</a>' % users.create_logout_url(self.request.uri))
        #else:
        #    self.response.out.write('hello, <span>anonymous person</span>! welcome to <span>guestbook</span>!</h1>')
        #    self.response.out.write('<a id="login_link" href="%s">log in</a>' % users.create_login_url(self.request.uri))

        #self.response.out.write('''
        #            </div>
        #            <div id="guestbook_form">
        #                <form action="/sign" method="post">
        #                    <textarea id="guestbook_content" name="content" placeholder="i want to say......"></textarea>
        #                    <input id="guestbook_submit" type="submit" value="paste">
        #                    by <span><b>''')
        if user:
            #self.response.out.write(user.nickname())
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'log out'
        else:
            #self.response.out.write('anonymous person')
            url = users.create_login_url(self.request.uri)
            url_linktext = 'log in'
        #self.response.out.write('''
        #                    </b></span>
        #                </form>
        #            </div>
        #            <div id="guestbook_wall">''')

        #greetings = db.GqlQuery('select * from Greeting order by date desc limit 10')
        greetings_query = Greeting.all().order('-date')
        greetings = greetings_query.fetch(10)

        #for greeting in greetings:
        #    self.response.out.write('<div class="guestbook_entry">')
        #    if greeting.author:
        #        self.response.out.write('<span><b>%s</b></span>' % greeting.author.nickname())
        #    else:
        #        self.response.out.write('<span>an anonymous person</span>')
        #    self.response.out.write(' said:<blockquote>%s</blockquote></div>' % cgi.escape(greeting.content))
        
        #self.response.out.write('''
        #            </div>
        #            <div id="footer">
        #                <p>&copy;guestbook. powered by gae. designed by chenjenping.</p>
        #            </div>
        #        </body>
        #    </html>''')

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
            'greetings': greetings
        }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class Guestbook(webapp.RequestHandler):
    def post(self):
        #self.response.out.write('''
        #    <!DOCTYPE html>
        #    <html>
        #        <head>
        #            <meta charset="utf-8">
        #            <title>guestbook</title>
        #        </head>
        #        <body>
        #            you wrote:
        #            <pre>''')
        #self.response.out.write(cgi.escape(self.request.get('content')))
        #self.response.out.write('''
        #            </pre>
        #        </body>
        #    </html>''')

        greeting = Greeting()

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()
        self.redirect('/')

class Intro(webapp.RequestHandler):
    def get(self):
        template_values = {
        }
        path = os.path.join(os.path.dirname(__file__), 'intro.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/sign', Guestbook),
                                      ('/intro', Intro)],
                                     debug = True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
