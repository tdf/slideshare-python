import os
from bottle import route, run, static_file, request
from subprocess import call


# -----

@route('/api/users/')
def users():
    return "<a href='test/'>User Test</a>"

@route('/api/topics/')
def topics():
    return "<a href='test/'>Topic Test</a>"

@route('/api/users/test/')
def test():
    return "<a href='deck1/'>deck1</a><br/><a href='deck2/'>deck2</a>"

@route('/api/users/test/deck1/')
def deck1():
    return "<a href='1/'>revision 1</a><br/><a href='2/'>revision 2</a>"

@route('/api/users/test/<deck>/<rev:int>/')
def list_deck(deck, rev):
    return "<a href='checkinDate'>checkin data</a><br/><a href='checkinComment'>checkin comment</a><br/><a href='deck.fodp'>deck.fodp</a><br/><a href='1/'>slide 1</a>"

@route('/api/users/test/<deck>/<rev:int>/checkinDate')
def send_checkinDate(deck,rev):
    return '2013-04-01 for '+deck+', rev '+str(rev)

@route('/api/users/test/<deck>/<rev:int>/checkinComment')
def send_checkinComment(deck,rev):
    return 'Riiiiight on for '+deck+', rev '+str(rev)

@route('/api/users/test/<deck>/<rev:int>/<slide:int>/keywords.json')
def send_keywords(deck, rev, slide):
    return {'Author': 'Joe User',
            'Title':  'The great slideshow'}

@route('/upload', method='POST')
def upload_file():
    upload_path = '/tmp'
    soffice = '/dump2/libo/libo2/install/program/soffice.bin'
    convert = 'convert'
    thumbnail_size = '128x128'
    # TODO: Add all required parameters here
    tag     = request.forms.get('tag')
    file    = request.files.get('file')
    # TODO: Create proper paths for uploads & Check for upload errors
    file.save(upload_path)
    call([soffice, '--convert-to', 'pdf', '--outdir', upload_path, upload_path+'/'+file.filename])
    call([convert, '-resize', thumbnail_size, upload_path+'/'+os.path.splitext(file.filename)[0]+'.pdf', upload_path+'/'+os.path.splitext(file.filename)[0]+'.jpg'])
    return 'Success:'+tag+':'+file.filename


#-----

@route('/api/users/test/<deck>/<rev:int>/deck.fodp')
def send_deck(deck, rev):
    return static_file(deck+'.fodp', root='decks/'+deck+'/'+str(rev), mimetype='text/xml')

@route('/api/users/test/<deck>/<rev:int>/<slide:int>/')
def list_slide(deck,rev,slide):
    return "<a href='thumbnail.png'>thumbnail</a><br/><a href='slide.fodp'>slide "+str(slide)+"</a><br/><a href='keywords.json'>keywords</a>"

@route('/api/users/test/<deck>/<rev:int>/<slide:int>/slide.fodp')
def send_slide(deck, rev, slide):
    return static_file(str(slide)+'.fodp', root='decks/'+deck+'/'+str(rev), mimetype='text/xml')

@route('/api/users/test/<deck>/<rev:int>/<slide:int>/thumbnail.png')
def send_thumbnail(deck, rev, slide):
    return static_file(str(slide)+'.png', root='decks/'+deck+'/'+str(rev), mimetype='image/png')

run(host='localhost', port=8080, reloader=True)
