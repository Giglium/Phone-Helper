#!/usr/bin/python

import bottle, sys
from bottle.ext.i18n import I18NPlugin, I18NMiddleware, i18n_defaults, i18n_view, i18n_template
from bottle import Bottle, run, route, static_file, request
from phone_helper import PhoneHelper

phone_helper = PhoneHelper()

i18n_defaults(bottle.SimpleTemplate, bottle.request)


def get():
    app = bottle.Bottle()

    @app.route('/')
    @app.route('/index')
    def index():
        data = phone_helper.read_settings()
        if not data['error']:
            return i18n_template('index', warning=False)
        else:
            return i18n_template('index', warning=True)

    @app.route('/shutdown')
    def shutdown():
        sys.stderr.close()
        return

    @app.route('/upload')
    @app.route('/fileupload')
    @i18n_view('upload', error=False, success=False)
    def upload():
        return {}

    @app.route('/fileupload', method='POST')
    def file_upload():
        data = request.files.getall('data')
        error = phone_helper.file_upload(data)
        if not error:
            return i18n_template('upload', error=False, success=True)
        else:
            return i18n_template('upload', error=True, success=False)

    @app.route('/settings')
    @app.route('/save')
    def settings():
        data = phone_helper.read_settings()
        if not data['error']:
            return i18n_template('settings', success=False, data=data)
        else:
            data = {'phonePrefix': '', 'columsTitle': '', 'shifter': False, 'validName': '', 'discardName': '',
                    'createDiscardSheet': False}
            return i18n_template('settings', success=False, data=data)

    @app.route('/save', method='POST')
    def save_settings():
        data = {'phonePrefix': request.forms.get('phonePrefix'), 'columsTitle': request.forms.get('columsTitle'),
                'validName': request.forms.get('validName'), 'discardName': request.forms.get('discardName')}

        shifter = request.forms.get('shifter')
        create_discard_sheet = request.forms.get('createDiscardSheet')

        if shifter == 'on':
            data['shifter'] = True
        else:
            data['shifter'] = False

        if create_discard_sheet == 'on':
            data['createDiscardSheet'] = True
        else:
            data['createDiscardSheet'] = False

        phone_helper.save_settings(data)

        return i18n_template('settings', success=True, data=data)

    @app.route('/files')
    def files():
        data = phone_helper.file_list()
        return i18n_template('files', success=False, input_files=data['input'], output_files=data['output'],
                             archive_files=data['archive'])

    @app.route('/statistic/<filename>')
    def statistic(filename):
        return phone_helper.get_statistic(filename)

    @app.route('/delete/<filename:path>')
    def delete(filename):
        phone_helper.delete_file(filename)
        return bottle.redirect("/files")

    @app.route('/job')
    def job():
        phone_helper.run_job()
        data = phone_helper.file_list()
        return i18n_template('files', success=True, input_files=data['input'], output_files=data['output'],
                             archive_files=data['archive'])

    # Static resource route
    @app.route('/static/<filename:path>', name='static')
    def server_static(filename):
        return static_file(filename, root=phone_helper.STATIC_FOLDER)

    @app.route('/fonts/<filename>', name='fonts')
    def server_font(filename):
        return static_file(filename, root=phone_helper.FONTS_DIR)

    @app.route('/download/<filename:path>', name='download')
    def server_download(filename):
        return static_file(filename, root=phone_helper.PARENT_FOLDER, download=True)

    bottle.SimpleTemplate.defaults["get_url"] = app.get_url

    lang_app = bottle.Bottle()

    @lang_app.route('/')
    def sub():
        return bottle.template("current language is {{lang()}}")

    app.mount(app=lang_app, prefix='/lang', skip=None)

    return I18NMiddleware(app, I18NPlugin(domain='messages', default='en', locale_dir='./views'))


if __name__ == '__main__':
    bottle.run(app=get(), host='localhost', port='1024', quiet=False, reloader=True, debug=True)
