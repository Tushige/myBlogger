'''
This file contains the controller class for blog submit page
'''
from base import BaseHandler
from blog_model import Blog
from cache import Cache

# handler class for '/newpost' - page for submitting a new post
class NewpostHandler(BaseHandler):
    # render the template with given params
    def render_newpost(self, subject='', content='', error=''):
        self.render('newpost.html', subject=subject, content=content, user=self.user,error=error)

    def get(self, param_username):
        # welcome user if active user matches user in url
        if self.user is not None and self.user.username==param_username:
            self.render_newpost()
        # blog submission is only allowed if user is logged in
        else:
            return self.redirect('/')

    # user submits form
    def post(self, param_username):
        # retrieve submission fields
        subject = self.request.get('subject')
        content = self.request.get('content')
        username = self.user.username
        profile_name = self.user.profile_name
        # check that all required fields are filled in
        if subject and content:
            newBlog = Blog.createBlog(subject=subject,
                                      content=content,
                                      username=username,
                                      profile_name=profile_name)
            newBlog.content = newBlog.content.replace('\\n', '<br>')
            # flush the cache on db write
            Cache.flush()
            key = newBlog.put()
            self.redirect("/entry/%s" % str(key.id()))
        else:
            error = 'Please submit both subject and content'
            self.render_newpost(subject=subject, content=content, error=error)
