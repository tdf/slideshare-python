#!/usr/bin/env python
#
# This file is part of the LibreOffice project.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import os, json
from bottle import get, post, auth_basic, run, static_file, request, debug
from subprocess import call


# -----

@get('/api/users/')
def users():
    return "<a href='test/'>User Test</a>"

@get('/api/topics/')
def topics():
    return "<a href='test/'>Topic Test</a>"

@get('/api/users/test/')
def test():
    return "<a href='deck1/'>deck1</a><br/><a href='deck2/'>deck2</a>"

@get('/api/users/test/deck1/')
def deck1():
    return "<a href='1/'>revision 1</a><br/><a href='2/'>revision 2</a>"

@get('/api/users/test/<deck>/<rev:int>/')
def list_deck(deck, rev):
    return "<a href='checkinDate'>checkin data</a><br/><a href='checkinComment'>checkin comment</a><br/><a href='deck.fodp'>deck.fodp</a><br/><a href='1/'>slide 1</a>"

@get('/api/users/test/<deck>/<rev:int>/checkinDate')
def send_checkinDate(deck,rev):
    return '2013-04-01 for '+deck+', rev '+str(rev)

@get('/api/users/test/<deck>/<rev:int>/checkinComment')
def send_checkinComment(deck,rev):
    return 'Riiiiight on for '+deck+', rev '+str(rev)

@get('/api/users/test/<deck>/<rev:int>/<slide:int>/keywords.json')
def send_keywords(deck, rev, slide):
    return {'Author': 'Joe User',
            'Title':  'The great slideshow'}

local_conf=json.loads(open('local.json').read()) if os.path.exists('local.json') else {}
def validate_auth(user, password):
    if "users" in local_conf:
        user_dict = local_conf["users"]
        if user in user_dict and 'password' in user_dict[user]:
            return password == user_dict[user]['password']
    return False

# eventually use ssl here - http://dgtool.blogspot.de/2011/12/ssl-encryption-in-python-bottle.html
@post('/api/upload')
@auth_basic(validate_auth, realm='upload')
def upload_file():
    upload_path = '/tmp'
    soffice = 'soffice'
    convert = 'convert'
    thumbnail_size = '128x128'

    # override defaults by config
    if "thumbnails" in local_conf:
        thumbnails_dict = local_conf["thumbnails"]
        upload_path = thumbnails_dict['upload_path'] if 'upload_path' in thumbnails_dict else upload_path
        soffice = thumbnails_dict['soffice'] if 'soffice' in thumbnails_dict else soffice
        convert = thumbnails_dict['convert'] if 'convert' in thumbnails_dict else convert
        thumbnail_size = thumbnails_dict['thumbnail_size'] if 'thumbnail_size' in thumbnails_dict else thumbnail_size

    # TODO: Add all required parameters here
    tag     = request.forms.get('tag')
    content = request.files.get('file')
    # TODO: Create proper paths for uploads & Check for upload errors
    out = open(upload_path+'/'+content.filename, 'wb')
    while True:
        bits = content.file.read(10240)
        if not bits:
            break
        out.write(bits)
    out.close()
    call([soffice, '--headless', '--convert-to', 'pdf', '--outdir', upload_path, upload_path+'/'+content.filename])
    call([convert, '-resize', thumbnail_size, upload_path+'/'+os.path.splitext(content.filename)[0]+'.pdf', upload_path+'/'+os.path.splitext(content.filename)[0]+'.png'])
    return 'Success:'+tag+':'+content.filename

#-----

@get('/api/users/test/<deck>/<rev:int>/deck.fodp')
def send_deck(deck, rev):
    return static_file(deck+'.fodp', root='decks/'+deck+'/'+str(rev), mimetype='text/xml')

@get('/api/users/test/<deck>/<rev:int>/<slide:int>/')
def list_slide(deck,rev,slide):
    return "<a href='thumbnail.png'>thumbnail</a><br/><a href='slide.fodp'>slide "+str(slide)+"</a><br/><a href='keywords.json'>keywords</a>"

@get('/api/users/test/<deck>/<rev:int>/<slide:int>/slide.fodp')
def send_slide(deck, rev, slide):
    return static_file(str(slide)+'.fodp', root='decks/'+deck+'/'+str(rev), mimetype='text/xml')

@get('/api/users/test/<deck>/<rev:int>/<slide:int>/thumbnail.png')
def send_thumbnail(deck, rev, slide):
    return static_file(str(slide)+'.png', root='decks/'+deck+'/'+str(rev), mimetype='image/png')

def main():
    debug(True)
    run(host='localhost', port=8080, reloader=True, quiet=False)

if __name__ == "__main__":
    main()
