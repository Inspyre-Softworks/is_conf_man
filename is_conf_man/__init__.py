#!/usr/bin/env python3

import PySimpleGUI as gui


class ConfManError(Exception):
    pass


class NoInputError(ConfManError):
    @staticmethod
    def message():
        print('No file selected!')


config = None
backup_path = None

def version():
    from os import path
    filepath = path.dirname(__file__)
    print(filepath)


def load_config(file):
    import configparser

    parser = configparser.ConfigParser()
    parser.read(file)
    return parser


def check_exists(path, saving=False):
    import os
    conf_dir = path
    print(f'{conf_dir}')

    if not os.path.exists(conf_dir):
        os.makedirs(conf_dir)
        return None
    else:
        from pathlib import Path
        import PySimpleGUI as gui
        filepath = conf_dir + 'config.ini'
        conf_file = Path(filepath)
        if not saving:
            if conf_file.is_file():
                confirm = gui.PopupYesNo(f'Detected file in input directory. Should I load this config file? [{conf_file}]')
                if confirm.lower() == 'yes':
                    load_config(conf_file)
                    show()
                    return True
                else:
                    return False
        else:
            if conf_file.is_file():
                return True
            else:
                return False


def check_overwrite(file):
    import ntpath

    confirm = gui.PopupYesNo(f'The file {ntpath.basename(file)} already exists. Overwrite?')

    if confirm.lower() == 'yes':
        return True
    else:
        return False


def backup_prev(file):
    import shutil
    from datetime import datetime

    time_now = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

    backup_name = time_now + '_backup_config.ini'

    shutil.copyfile(file, backup_path + '/' + backup_name)




def save_config(config, no_backup=False, dest=None):
    global backup_path
    print(config.sections())
    import os
    filepath = os.getcwd()

    if dest is None:
        filepath = filepath + '/conf/'
    else:
        filepath = dest

    backup_path = filepath + '/backup'

    if not os.path.exists(backup_path):
        os.makedirs(backup_path)

    file = str(filepath + 'config.ini')

    if check_exists(filepath, saving=True):
        if check_overwrite(file):
            print('Saving...')
            backup_prev(file)

    with open(file, 'w') as configfile:
        config.write(configfile)


def theme(config):
    theme_set = config.get('gui_settings', 'theme')
    return theme_set


def grabby(config):
    grab = config.get('gui_settings', 'grab_anywhere')
    print(type(grab))
    return grab.lower() in ['true', '1', 't', 'y', 'yes', 'affirmative',
                            'positive']  # Use 'grab' string to return a True or False bool


def show(conf=None, dest=None):
    global config
    """
    Show the desired configparser.ConfigParser() object in a GUI window. You can then edit said .ini file

    :param conf:
    :return:
    """

    if conf is None:
        run()
    else:
        config = conf

    print(config.sections())
    layout = []
    for section in config.sections():
        f_layout = []
        section_title = str(section).replace('_', ' ')
        print(config.options(section=section))
        for option in config.options(section=section):
            if option == "theme":
                f_layout += [[gui.Text(option, justification='left', pad=(50, 5)),
                              gui.Combo(gui.theme_list(), key=str(f'{section}.{option}'),default_value=theme(config),
                                        enable_events=True),
                              gui.Button('Preview', key='preview_theme')]]
            else:
                f_layout += [gui.Text(option, justification='left', pad=(50, 5)),
                             gui.InputText(config.get(section=section, option=option),
                                           justification='right',
                                           pad=(50, 5),
                                           key=str(f'{section}.{option}'))],

            frame = [[gui.Frame(f'{str(section_title).title()}', layout=f_layout)]]

        layout += frame
    layout += [[gui.Button('OK', key='ok'), gui.Button('Apply', key='apply'), gui.Button('Exit', key='exit')]]
    print(config.get('gui_settings', 'grab_anywhere'))
    gui.theme(theme(config))
    window = gui.Window('Test Config Window', layout=layout, size=(500, 500), element_justification='center',
                        grab_anywhere=grabby(config))

    theme_changed = False

    while True:
        event, vals = window.read(timeout=100)

        if event is None or event == 'exit':
            window.close()
            exit()

        if event == 'gui_settings.theme':
            theme_changed = True

        if event == 'preview_theme':
            gui.theme(vals['gui_settings.theme'])
            gui.PopupOK(f'This is a preview of {vals["gui_settings.theme"]}')

        if event == 'apply':
            gui.theme(vals['gui_settings.theme'])
            window.refresh()
            print('window refreshed')

        if event == 'apply' or event == 'ok':
            print(vals)
            for setting in vals:
                val = vals[setting]
                print(val)
                spl_setting = setting.split(sep='.')
                if val != config.get(spl_setting[0], spl_setting[1]):
                    print('value changed')
                    print(val)
                    print(spl_setting[0])
                    if spl_setting[0] == 'gui_settings':
                        if spl_setting[1] == 'grab_anywhere':
                            print(f'the val is {val}')
                            if val == 'True':
                                window.grab_any_where_on()
                            else:
                                window.grab_any_where_off()
                        print('It is grab anywhere')
                config[spl_setting[0]][spl_setting[1]] = val
            confirm = gui.PopupYesNo('Are you sure you want to save config?', title='Confirm Save')
            if confirm.lower() == 'yes':
                if theme_changed:
                    gui.PopupOK('Since you changed theme settings you should restart the program.')
                print('Saving')
                if dest is None:
                    save_config(config)
                else:
                    save_config(config, dest=dest)
            else:
                print('Cancelled')


def run(file=None):
    global config
    import os
    path = os.getcwd()
    if file is None:
        if not check_exists(path) is None:
            file = gui.PopupGetFile(
                'Pick a config file',
                default_path=path,
                file_types=(
                    ('Config Files', '*.ini'),
                )
            )
    config = load_config(file)
    show(config)

    if file == '':
        raise NoInputError


if __name__ == '__main__':
    try:
        run(conf_file)
    except NoInputError:
        NoInputError.message()
        raise
