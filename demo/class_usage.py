import logging
import context_logging  # this `patches` logging with context stuff

@context_logging.context_logger(prefix='hh')
class Hitchiker(object):

    # this class has a self.log and that log has a context
    def __init__(self):
        self.name = 'Ivan Mesic'
        self.log.add_to_context(the_answer=42)
        self.question = 'What is life, universe and everything?'
        self.answer = 42

    def yell(self):
        # output also contains the_answer
        self.log.warn('Zorg reciting a poem!')

    @context_logging.log_context(the_question='question')
    def when_is_the_towel_day(self):
        self.log.info('The towel day is held every year on 25 May')


def main():
    hitcher = Hitchiker()
    hitcher.yell()
    hitcher.when_is_the_towel_day()



if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    log_handler = logging.StreamHandler()
    formatter = context_logging.JsonFormatter()
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)

    main()
