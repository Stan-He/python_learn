import logging
import os
import sys
import time
from autotest.client.shared.settings import settings


class AllowBelowSeverity(logging.Filter):

    """
    Allows only records less severe than a given level (the opposite of what
    the normal logging level filtering does.
    """

    def __init__(self, level):
        self.level = level
    #这个filter很有趣，如果record.levelno小于self.level则filter成功
    #和name无关
    def filter(self, record):
        return record.levelno < self.level


class LoggingConfig(object):
    global_level = logging.DEBUG #10
    stdout_level = logging.INFO  #20
    stderr_level = logging.ERROR #40
    #log日志的格式在这里定义的
    #10.10总长度是10，显示最多10个字符：%10.10s
    file_formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)-5.5s|%(module)10.10s:%(lineno)4.4d| '
            '%(message)s',
        datefmt='%m/%d %H:%M:%S')

    #console的format格式，在哪用的？
    console_formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)-5.5s| %(message)s',
        datefmt='%H:%M:%S')

    def __init__(self, use_console=True):
        self.logger = logging.getLogger()
        self.global_level = logging.DEBUG
        self.use_console = use_console

    @classmethod
    def get_timestamped_log_name(cls, base_name):
        #log的名字
        return '%s.log.%s' % (base_name, time.strftime('%Y-%m-%d-%H.%M.%S'))

    @classmethod
    def get_autotest_root(cls):
        #返回autotest主目录的位置
        shared_dir = os.path.dirname(__file__)
        return os.path.abspath(os.path.join(shared_dir, '..', '..'))

    @classmethod
    def get_server_log_dir(cls):
        #读取配置文件中的serverlog位置,如果为空，这指向autotest/logs目录，这是scheduler的log位置
        server_log_dir = settings.get_value('SERVER', 'logs_dir', default='')
        if not server_log_dir:
            server_log_dir = os.path.join(cls.get_autotest_root(), 'logs')
        return server_log_dir

    def add_stream_handler(self, stream, level=logging.DEBUG):
        #self.logger增加一个handler，format是console_formatter
        handler = logging.StreamHandler(stream)
        handler.setLevel(level)
        handler.setFormatter(self.console_formatter)
        self.logger.addHandler(handler)
        return handler

    def add_console_handlers(self):
        #增加两个handler，指向，stdout和stderr

        #增加一个stdout,level=20的handler
        stdout_handler = self.add_stream_handler(sys.stdout,
                                                 level=self.stdout_level)
        # only pass records *below* STDERR_LEVEL to stdout, to avoid duplication
        #给这个handler一个奇怪的filter:level小于40的都通过
        stdout_handler.addFilter(AllowBelowSeverity(self.stderr_level))
        #增加一个level=40，指向stderr的handler
        self.add_stream_handler(sys.stderr, self.stderr_level)

    def add_file_handler(self, file_path, level=logging.DEBUG, log_dir=None):
        #在logger中增加一个file_handler，位置在log_dir/file_path

        if log_dir:
            file_path = os.path.join(log_dir, file_path)
        handler = logging.FileHandler(file_path)
        handler.setLevel(level)
        handler.setFormatter(self.file_formatter)
        self.logger.addHandler(handler)
        return handler

    def _add_file_handlers_for_all_levels(self, log_dir, log_name):
        #给一个logger添加四个file handler
        for level in (logging.DEBUG, logging.INFO, logging.WARNING,
                      logging.ERROR):
            file_name = '%s.%s' % (log_name, logging.getLevelName(level))
            self.add_file_handler(file_name, level=level, log_dir=log_dir)

    def add_debug_file_handlers(self, log_dir, log_name=None):
        raise NotImplementedError

    def _clear_all_handlers(self):
        #关闭所有的handler
        for handler in list(self.logger.handlers):
            self.logger.removeHandler(handler)
            # Attempt to close the handler. If it's already closed a KeyError
            # will be generated. http://bugs.python.org/issue8581
            try:
                handler.close()
            except KeyError:
                pass

    def configure_logging(self, use_console=True, verbose=False):
        self._clear_all_handlers()  # see comment at top of file
        self.logger.setLevel(self.global_level)

        if verbose:
            self.stdout_level = logging.DEBUG
        if use_console:
            self.add_console_handlers()


class TestingConfig(LoggingConfig):

    def add_stream_handler(self, *args, **kwargs):
        pass

    def add_file_handler(self, *args, **kwargs):
        pass

    def configure_logging(self, **kwargs):
        pass
