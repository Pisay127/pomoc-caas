import getpass
import os
import random
import string


def required_input(input_text, input_func=input):
    response = ''
    first_run = True
    while response == '':
        response = input_func('{0}{1}'.format(
            '✘ ' if not first_run else '', input_text))
        first_run = False

    return response


def yesno_input(input_text):
    response = ''
    while response != 'y' and response != 'n' and response == '':
        response = required_input(input_text).lower()

    return True if response == 'y' else False


def display_secret_key(secret_key):
    print('Generated secret key. This is just a prettified display of the key and not how it actually looks or set.')
    print('')
    print('    *********')

    for chunk_index in range(0, len(secret_key), 7):
        chunk_string = secret_key[chunk_index: chunk_index + 7].ljust(7, ' ')
        print('    *{0}*'.format(chunk_string))

    print('    *********')
    print('')


def generate_secret_key(key_length, display_key):
    string_choices = string.ascii_letters + string.digits + '!@$%^&*()-=_+[]\{\}<>,.?/'

    key_array = [random.SystemRandom().choice(string_choices)
                    for i in range(key_length)]
    secret_key = ''.join(key_array)

    if display_key:
        display_secret_key(secret_key)

    return secret_key


if __name__ == '__main__':
    print('gen-envvar.py')
    print('This utility generates a script file (Shell files for UNIX-like OSes, probably .bat for Windows though not sure) that create environment variables for critical service-related information such as usernames, passwords, and secret keys. This must be run before deploying the code in the dev machine.')
    print('---')
    print('The "caas" service uses PostgreSQL as the database backend. Each machine (dev or production) may have differing database names and credentials for this service. Please provide the following information to connect your local copy of this service to the PostgreSQL server you have set up for this service.')
    print('')
    db_name = required_input('Database name: ')
    db_username = required_input('Username (of the database user): ')
    db_password = required_input('Password: ', getpass.getpass)
    db_host = input(
        'Database host (leave blank for the default, \'localhost\'): ') or 'localhost'
    db_port = input(
        'Database port (leave blank for the default, \'5432\'): ') or '5432'
    print('Got it! Thanks!')

    print('---')
    print('This service also uses a secret key. The key is used for "securing signed data" (view the Django docs on `SECRET_KEY` for more information at https://docs.djangoproject.com/en/2.0/topics/signing/). This key must unique for each instance of this service. The longer the key, the harder for computers to guess it using brute force.')
    print('')
    key_length = int(input('Key length (preferably 50 or larger): '))
    print(' [*] Generating the secret key...')
    secret_key = generate_secret_key(
        key_length, yesno_input('Display key [Y/N]? '))
    print('Alright, got it!')

    service_dir = os.path.dirname(os.path.realpath(__file__))
    if os.name == 'posix':  # Yeah, we're in UNIX boiz.
        print(' [*] Generating export batch file...', end='')

        batch_file_path = '{0}/set-envvars.sh'.format(service_dir)
        batch_file = open(batch_file_path, 'w+')
        batch_file.write(
            '# This file is auto-generated. Do not modify unless you know what you are doing.\n')
        batch_file.write('\n')
        batch_file.write('echo " [*] Exporting variables."\n')
        batch_file.write('export POMOC_CAAS_DB_NAME="{0}"\n'.format(db_name))
        batch_file.write('export POMOC_CAAS_DB_USERNAME="{0}"\n'.format(db_username))
        batch_file.write('export POMOC_CAAS_DB_PASSWORD="{0}"\n'.format(db_password))
        batch_file.write('export POMOC_CAAS_DB_HOST="{0}"\n'.format(db_host))
        batch_file.write('export POMOC_CAAS_DB_PORT="{0}"\n'.format(db_port))
        batch_file.write('export POMOC_CAAS_SECRET_KEY="{0}"\n'.format(secret_key))
        batch_file.close()

        print(' done!')
        print('')
        print('DO NOT MODIFY `set-envvars.sh` unless you know what you are doing. To finish properly seting the environment variables, run `set-envvars.sh`. Make sure you are in the project root. For example:')
        print('')
        print('  $ cd /path/to/project/root')
        print('  $ chmod +x set-envvars.sh')
        print('  $ (source | .) ./set-envvars.sh')
        print('')
        print('NOTE: `set-envvars.sh` should NEVER be added to the Git repository. It must be ignored via .gitignore. This is because the path to the `user-core` project differs from one machine to another. This file is only assured to work in Linux and macOS.')
    # elif host_os == 'nt': # Do Windows equivalent of the UNIX-specific code.
