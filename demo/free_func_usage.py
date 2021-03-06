__author__ = 'ivan'

import logging
import context_logging  # this `patches` logging with context stuff
context_logging.common_names_filename('common_logging_fields.json')


@context_logging.log_context(prefix='spell', spell='run_fast', machine='mean one')
def do_spell(spell=None):
    if spell is None:
        logging.warn('Casting random spell!',
                     additional_info='Dangerous!')
    else:
        logging.info('Casting spell \'{}\''.format(spell),
                     spell_value=spell)

@context_logging.log_context(prefix='sp', value='wind')
def main():
    wind = 'wind'
    logging.debug('He is Rincewind!', wind=wind)

    do_spell()
    do_spell('dissapear')


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    log_handler = logging.StreamHandler()
    formatter = context_logging.JsonFormatter()
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)

    main()
