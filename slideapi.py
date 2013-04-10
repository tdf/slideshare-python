#!/usr/bin/env python
#
# This file is part of the LibreOffice project.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import os, json, time, _cpwsgiserver3
from bottle import get, post, auth_basic, run, static_file, request
from bottle import debug, view, HTTPError, server_names, ServerAdapter
from subprocess import call

# config
#
# we understand:
# local_conf["users"], yielding {<username>: {"password": <password>, "description": <description>}, ... }
# local_conf["thumbnails"], yielding {"soffice": <path>, "convert": <path>, "thumbnail_size": <128x128>}
# local_conf["tags"], yielding [ <tagname>, ... ]
#
local_conf=json.loads(open('local.json').read()) if os.path.exists('local.json') else {}
root='filestore'

def validate_auth(user, password):
    if "users" in local_conf:
        user_dict = local_conf["users"]
        if user in user_dict and 'password' in user_dict[user]:
            return password == user_dict[user]['password']
    return False

# -------------------------------------------------------------------

def get_users():
    return {user: data['description'] for user, data in local_conf["users"].items()}

@get('/api/users/')
def users():
    return get_users()

@get('/users/')
@view('users')
def users():
    return dict(users=get_users())

# -------------------------------------------------------------------

def get_tags():
    return local_conf["tags"]

@get('/api/tags/')
def tags():
    return json.dumps(get_tags())

@get('/tags/')
@view('tags')
def tags():
    return dict(tags=get_tags())

# -------------------------------------------------------------------

def get_decks(user):
    path = "%s/%s/" % (root,user)
    if not os.path.isdir(path):
        return []
    return [deck for deck in os.listdir(path) if os.path.isdir(path+deck)]

def get_lastrev(user,deck):
    path = "%s/%s/%s/" % (root,user,deck)
    if not os.path.isdir(path):
        return 0
    # get last revision
    return int(sorted([rev for rev in os.listdir(path) if os.path.isdir(path+rev)], key=int)[-1])

@get('/api/users/<user>/')
def list_decks(user):
    return json.dumps(get_decks(user))

@get('/users/<user>/')
@view('decks')
def list_decks(user):
    return dict(decks=get_decks(user))

@get('/users/<user>/<deck>/thumbnail.png')
@get('/api/users/<user>/<deck>/thumbnail.png')
def get_thumbnail(user, deck):
    path = "%s/%s/%s/" % (root,user,deck)
    last_rev = get_lastrev(user,deck)
    # serve thumbnail from that rev, first slide
    return static_file('0.png', root=path+str(last_rev)+'/0/', mimetype='image/png')

# -------------------------------------------------------------------

def get_revs(user,deck):
    path = "%s/%s/%s/" % (root,user,deck)
    if not os.path.isdir(path):
        return []
    return sorted([rev for rev in os.listdir(path) if os.path.isdir(path+rev)], key=int)

@get('/api/users/<user>/<deck>/')
def list_revs(user,deck):
    return json.dumps(get_revs(user,deck))

@get('/users/<user>/<deck>/')
@view('revs')
def list_revs(user,deck):
    return dict(revs=get_revs(user,deck))

@post('/users/<user>/<deck>')
@post('/api/users/<user>/<deck>')
@auth_basic(validate_auth, realm='upload')
def upload_deck(user,deck):
    path = "%s/%s/%s/" % (root,user,deck)
    new_rev = get_lastrev(user,deck) + 1
    new_path = path+str(new_rev)

    if os.path.isdir(new_path):
        raise HTTPError(body='inconsistent repo, bailing out')

    if request.auth[0] != user:
        raise HTTPError(body='invalid user or insufficient rights, bailing out')

    os.makedirs(new_path)
    upload_path = new_path

    # TODO: Add all required parameters here
    tag     = request.forms.get('tag')
    content = request.files.get('file')
    # TODO: Create proper paths for uploads & Check for upload errors
    out = open(upload_path+'/deck.odp', 'wb')
    while True:
        bits = content.file.read(10240)
        if not bits:
            break
        out.write(bits)
    out.close()

    out = open(upload_path+'/meta.json', 'wb')
    json.dump({'tag': tag,
               'server_version': '1',
               'upload_filename': content.filename},
              out)

    thumbnail_size = '128x128'

    # override defaults by config
    if "thumbnails" in local_conf:
        thumbnails_dict = local_conf["thumbnails"]
        thumbnail_size = thumbnails_dict['thumbnail_size'] if 'thumbnail_size' in thumbnails_dict else thumbnail_size

    os.system('./convert_deck.sh '+upload_path+' '+thumbnail_size)
    return 'Success:'+tag+':'+content.filename


@get('/users/<user>/<deck>/<rev:int>/thumbnail.png')
@get('/api/users/<user>/<deck>/<rev:int>/thumbnail.png')
def get_thumbnail(user, deck, rev):
    path = "%s/%s/%s/%d/" % (root,user,deck,rev)
    # serve thumbnail from that rev, first slide
    return static_file('0.png', root=path+'/0/', mimetype='image/png')

@get('/users/<user>/<deck>/<rev:int>/deck.odp')
@get('/api/users/<user>/<deck>/<rev:int>/deck.odp')
def send_deck(user, deck, rev):
    path = "%s/%s/%s/%d/" % (root,user,deck,rev)
    return static_file(deck+'.odp', root=path, mimetype='text/xml')

# -------------------------------------------------------------------

def get_slides(user,deck,rev):
    path = "%s/%s/%s/%d/" % (root,user,deck,rev)
    if not os.path.isdir(path):
        return []
    return sorted([slide for slide in os.listdir(path) if os.path.isdir(path+slide)], key=int)

def get_revmeta(user,deck,rev):
    path = "%s/%s/%s/%d/" % (root,user,deck,rev)
    comment = open(path+'comment').read() if os.path.exists(path+'comment') else ''
    meta = json.loads(open(path+'meta.json').read()) if os.path.exists(path+'meta.json') else {}
    return {'CreationDate': time.strftime("%a, %d %b %Y %H:%M:%S GMT",
                                          time.gmtime(os.stat(path).st_ctime)),
            'CommitComment': comment,
            'Meta': meta}

@get('/api/users/<user>/<deck>/<rev:int>/')
def list_slides(user, deck, rev):
    return json.dumps(get_slides(user,deck,rev))

@get('/users/<user>/<deck>/<rev:int>/')
@view('slides')
def list_slides(user, deck, rev):
    return dict(slides=get_slides(user,deck,rev), revmeta=get_revmeta(user,deck,rev))

@get('/users/<user>/<deck>/<rev:int>/<slide:int>/thumbnail.png')
@get('/api/users/<user>/<deck>/<rev:int>/<slide:int>/thumbnail.png')
def get_thumbnail(user, deck, rev, slide):
    path = "%s/%s/%s/%d/%d/" % (root,user,deck,rev,slide)
    return static_file(str(slide)+'.png', root=path, mimetype='image/png')

@get('/api/users/<user>/<deck>/<rev:int>/meta.json')
def list_revmeta(user,deck,rev):
    return get_revmeta(user,deck,rev)

# -------------------------------------------------------------------

def get_slidemeta(user,deck,rev,slide):
    path = "%s/%s/%s/%d/%d/" % (root,user,deck,rev,slide)
    return json.loads(open(path+'meta.json').read()) if os.path.exists(path+'meta.json') else {}

@get('/api/users/<user>/<deck>/<rev:int>/<slide:int>/meta.json')
def list_slidemeta(user, deck, rev, slide):
    return get_slidemeta(user, deck, rev, slide)

@get('/users/<user>/<deck>/<rev:int>/<slide:int>/slide.odp')
@get('/api/users/<user>/<deck>/<rev:int>/<slide:int>/slide.odp')
def send_slide(user, deck, rev, slide):
    path = "%s/%s/%s/%d/%d/" % (root,user,deck,rev,slide)
    return static_file(str(slide)+'.odp', root=path, mimetype='text/xml')

@get('/')
def home_page():
    return '<html><body>Welcome</body></html>'

# -------------------------------------------------------------------

class SSLInterface(ServerAdapter):
    def run(self, handler):
        server = _cpwsgiserver3.CherryPyWSGIServer((self.host, self.port), handler)
        cert = 'bottletest.pem'
        server.ssl_certificate = cert
        server.ssl_private_key = cert
        try:
            server.start()
        finally:
            server.stop()

server_names['sslinterface'] = SSLInterface

def main():
    debug(True)
    run(host='localhost', port=8080, reloader=True, quiet=False, server='sslinterface')

if __name__ == "__main__":
    main()
