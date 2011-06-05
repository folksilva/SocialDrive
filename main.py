#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import logging, os

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util

ROOT_PATH = os.path.dirname(__file__)

class Message(db.Model):
    plate = db.StringProperty()
    text = db.StringProperty()
    when = db.DateTimeProperty(auto_now_add=True)

class Reply(db.Model):
    message = db.ReferenceProperty(Message,collection_name="replies")
    text = db.StringProperty()
    when = db.DateTimeProperty(auto_now_add=True)

# Página inicial
class MainPage(webapp.RequestHandler):
    def get(self):
        
        messages = None
        flash = None
        plate = None
        
        try:
            plate = self.request.get("p")
            key = self.request.get("m")
            flash = self.request.get("f")
            if key:
                message = db.get(key)
                if message:
                    messages = [message]
                    plate = message.plate
                else:
                    flash = "Não sei qual mensagem é essa. =("
            elif plate:
                messages = Message.all().filter("plate =", plate).order("-when")
                if messages.count(1) == 0:
                    flash = "Ninguém mandou uma mensagem para essa placa ainda. Seja o primeiro!"
        except:
            pass
        
        data = {
            "messages":messages,
            "flash":flash,
            "plate":plate,
        }
        
        path = os.path.join(ROOT_PATH, 'template.html')
        self.response.out.write(template.render(path, data))
    
    def post(self):
        
        try:
            plate = self.request.get("plate")
            text = self.request.get("msg")
            msg = Message()
            msg.plate = plate
            msg.text = text
            msg.put()
            self.redirect("/?p=%s#m%s" % (self.request.get("plate"),msg.key()), False)
        except:
            self.redirect("/?p=%s&f=Não consegui salvar a sua mensagem. =(" % self.request.get("plate"), False)

class ReplyMsg(webapp.RequestHandler):
    def post(self):
        try:
            message = self.request.get("m")
            text = self.request.get("t")
            reply = Reply()
            reply.message = db.get(message)
            reply.text = text
            reply.put()
            self.response.out.write("<script>parent.location.reload(true);</script>")
        except:
            self.response.set_status(500)
            self.response.out.write("<script>parent.document.getElementById('flash').innerHTML='Opss. O envio da resposta falhou. =(';</script>")

def main():    
    application = webapp.WSGIApplication([
            
            # Main.py
            
            ('/', MainPage), # GET Página inicial
            ('/reply',ReplyMsg) # POST salva uma reposta     
        ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()

