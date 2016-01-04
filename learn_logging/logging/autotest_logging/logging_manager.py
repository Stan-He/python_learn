import logging
import os
import signal
import sys
import warnings
import re

# primary public APIs

#传入一个logging_config.LoggingConfig对象
def configure_logging(logging_config, **kwargs):
    """
    Configure the logging module using the specific configuration object, which
    should be an instance of logging_config.LoggingConfig (usually of a
    subclass).  Any keyword args will be passed to the object's
    configure_logging() method.

    Every entry point should call this method at application startup.
    """
    #loggingManager是一个类
    LoggingManager.logging_config_object = logging_config
    logging_config.configure_logging(**kwargs)


def get_logging_manager(manage_stdout_and_stderr=False, redirect_fds=False):
    """
    Create a LoggingManager that's managing sys.stdout and sys.stderr.

    Every entry point that wants to capture stdout/stderr and/or use
    LoggingManager to manage a stack of destinations should call this method
    at application startup.
    """
    #????看后面
    if redirect_fds:
        manager = FdRedirectionLoggingManager()
    else:
        manager = LoggingManager()
    if manage_stdout_and_stderr:
        manager.manage_stdout()
        manager.manage_stderr()
    return manager


# implementation follows

logger = logging.getLogger()


def _current_handlers():
    return set(logger.handlers)

#保存函数的code对象
_caller_code_to_skip_in_logging_stack = set()


def do_not_report_as_logging_caller(func):
    #装饰器，这个函数不进行log
    """Decorator to annotate functions we will tell logging not to log."""
    # These are not the droids you are looking for.
    # You may go about your business.
    _caller_code_to_skip_in_logging_stack.add(func.func_code)
    return func


# Copied from Python 2.4 logging/__init__.py Logger.findCaller and enhanced.
# The logging code remains the same and compatible with this monkey patching
# through at least Python version 2.6.2.
#貌似没什么意义，logging中的findcall，查找调用栈，获取当前的行号和函数名等
def _logging_manager_aware_logger__find_caller(unused):
    """
    Find the stack frame of the caller so that we can note the source
    file name, line number and function name.
    """
    f = sys._getframe(2).f_back
    rv = "(unknown file)", 0, "(unknown function)"
    while hasattr(f, "f_code"):
        co = f.f_code
        filename = os.path.normcase(co.co_filename)
        if filename == logging._srcfile:
            f = f.f_back
            continue
        # START additional code.
        #!!!如果我们找到的code对象保存在不log的stack里面，那么这个log就不report
        if co in _caller_code_to_skip_in_logging_stack:
            f = f.f_back
            continue
        # END additional code.
        rv = (filename, f.f_lineno, co.co_name)
        break
    return rv


if sys.version_info[:2] > (2, 7):
    warnings.warn('This module has not been reviewed for Python %s' %
                  sys.version)


# Monkey patch our way around logging's design...
# Monkey patch代表着在runtime的时候动态的替换掉原来模块中的方法、类、

#原来的find_caller函数
_original_logger__find_caller = logging.Logger.findCaller
#替换成autotest自己的find_caller，增加了可以主动不log code的功能
logging.Logger.findCaller = _logging_manager_aware_logger__find_caller


class LoggingFile(object):

    """
    File-like object that will receive messages pass them to the logging
    infrastructure in an appropriate way.
    """
    #假装自己是一个文件，但实际是一个log，目的是将一个字符串，分行的输出到log中
    #如果是一个包含换行的string，会分成多个log下发出去
    def __init__(self, prefix='', level=logging.DEBUG,
                 logger=logging.getLogger()):
        """
        :param prefix - The prefix for each line logged by this object.
        """

        self._prefix = prefix
        self._level = level
        self._buffer = []
        self._logger = logger

    @do_not_report_as_logging_caller
    def write(self, data):
        """"
        Writes data only if it constitutes a whole line. If it's not the case,
        store it in a buffer and wait until we have a complete line.
        :param data - Raw data (a string) that will be processed.
        """
        #传入data，一个字符串，data进行分行
        #第一行和前一个buffer结合
        #最后一行继续放在buffer里，等待后续的log
        # splitlines() discards a trailing blank line, so use split() instead
        data_lines = data.split('\n')
        if len(data_lines) > 1:
            self._buffer.append(data_lines[0])
            self._flush_buffer()
        for line in data_lines[1:-1]:
            self._log_line(line)
        if data_lines[-1]:
            self._buffer.append(data_lines[-1])

    @do_not_report_as_logging_caller
    def writelines(self, lines):
        """"
        Writes itertable of lines

        :param lines: An iterable of strings that will be processed.
        """
        for data in lines:
            self.write(data)

    @do_not_report_as_logging_caller
    def _log_line(self, line):
        """
        Passes lines of output to the logging module.
        """
        self._logger.log(self._level, self._prefix + line)

    @do_not_report_as_logging_caller
    def _flush_buffer(self):
        if self._buffer:
            self._log_line(''.join(self._buffer))
            self._buffer = []

    @do_not_report_as_logging_caller
    def flush(self):
        self._flush_buffer()

    def isatty(self):
        return False


class SortingLoggingFile(LoggingFile):

    """
    File-like object that will receive messages and pass them to the logging
    infrastructure. It decides where to pass each line by applying a regex
    to it and seeing which level it matched.
    """

    def __init__(self, prefix='', level_list=[('ERROR', logging.ERROR),
                                              ('WARN', logging.WARN), ('INFO', logging.INFO),
                                              ('DEBUG', logging.DEBUG)], logger=logging.getLogger()):
        super(SortingLoggingFile, self).__init__(prefix=prefix, logger=logger)
        #生成一个新list[(re对象,40),(re对象，30)]
        self._level_list = [(re.compile(x), y) for x, y in level_list]

    @do_not_report_as_logging_caller
    def _log_line(self, line):
        #如果line中存在以上4个级别的re字段，则logging
        for pattern, level in self._level_list:
            if pattern.search(line):
                self._logger.log(level, self._prefix + line)
                break
        #否则添加一个UNMATCHED_LOG_LEVEL
        else:
            self._logger.log(logging.ERROR, 'UNMATCHED_LOG_LEVEL: ' +
                             self._prefix + line)


class _StreamManager(object):

    """
    Redirects all output for some output stream (normally stdout or stderr) to
    the logging module by replacing the file objects with a new LoggingFile
    that calls logging.log().
    """
    #将stdout和stderr中的所有内容重定向到log中去

    def __init__(self, stream, level, stream_setter):
        """
        :param stream: stream object to manage
        :param level: level at which data written to the stream will be logged
        :param stream_setter: function accepting a stream object that will
                replace the given stream in its original location.
        """
        self._stream = stream #需要manage的流
        self._level = level
        self._stream_setter = stream_setter #方法，接受一个流对象
        self._logging_stream = None

    def _replace_with_logger(self):
        #将logging流替换成LoggingFile对象，调用_stream_setter函数
        self._logging_stream = LoggingFile(level=self._level)
        self._stream_setter(self._logging_stream)

    def _restore_stream(self):
        self._stream_setter(self._stream)

    def flush(self):
        self._logging_stream.flush()

    def start_logging(self):
        """Start directing the stream to the logging module."""
        self._replace_with_logger()

    def stop_logging(self):
        """Restore the stream to its original settings."""
        self._restore_stream()

    def on_push_context(self, context):
        """
        Called when the logging manager is about to push a new context onto the
        stack and has changed logging settings.  The StreamHandler can modify
        the context to be saved before returning.
        """
        pass

    def on_restore_context(self, context):
        """
        Called when the logging manager is restoring a previous context.
        """
        pass


class LoggingManager(object):

    """
    Manages a stack of logging configurations, allowing clients to conveniently
    add and remove logging destinations.  Also keeps a list of StreamManagers
    to easily direct streams into the logging module.
    """
    #管理一堆logging配置，允许clients方便的增删logging位置，另外保持一个StreamManger列表
    #用于streams redirect
    STREAM_MANAGER_CLASS = _StreamManager

    logging_config_object = None

    def __init__(self):
        """
        This class should not ordinarily be constructed directly (other than in
        tests).  Use the module-global factory method get_logging_manager()
        instead.
        """
        #使用全局函数get_logging_manager，不要多次init这个类
        if self.logging_config_object is None:
            raise RuntimeError('You must call configure_logging() before this')

        # _context_stack holds a stack of context dicts.  Each context dict
        # contains:
        # * old_handlers: list of registered logging Handlers
        # contexts may also be extended by _StreamHandlers
        self._context_stack = []
        self._streams = []
        self._started = False

    def manage_stream(self, stream, level, stream_setter):
        """
        Tells this manager to manage the given stream.  All data written to the
        stream will be directed to the logging module instead.  Must be called
        before start_logging().

        :param stream: stream to manage
        :param level: level to log data written to this stream
        :param stream_setter: function to set the stream to a new object
        """
        if self._started:
            raise RuntimeError('You must call this before start_logging()')
        self._streams.append(self.STREAM_MANAGER_CLASS(stream, level,
                                                       stream_setter))

    def _sys_stream_setter(self, stream_name):
        assert stream_name in ('stdout', 'stderr'), stream_name

        def set_stream(file_object):
            setattr(sys, stream_name, file_object)
        return set_stream

    def manage_stdout(self):
        self.manage_stream(sys.stdout, logging.INFO,
                           self._sys_stream_setter('stdout'))

    def manage_stderr(self):
        self.manage_stream(sys.stderr, self.logging_config_object.stderr_level,
                           self._sys_stream_setter('stderr'))

    def start_logging(self):
        """
        Begin capturing output to the logging module.
        """
        for stream_manager in self._streams:
            stream_manager.start_logging()
        self._started = True

    def stop_logging(self):
        """
        Restore output to its original state.
        """
        while self._context_stack:
            self._pop_context()

        for stream_manager in self._streams:
            stream_manager.stop_logging()

        self._started = False

    def _clear_all_handlers(self):
        for handler in _current_handlers():
            logger.removeHandler(handler)

    def _get_context(self):
        return {'old_handlers': _current_handlers()}

    def _push_context(self, context):
        for stream_manager in self._streams:
            stream_manager.on_push_context(context)
        self._context_stack.append(context)

    def _flush_all_streams(self):
        for stream_manager in self._streams:
            stream_manager.flush()

    def _add_log_handlers(self, add_handlers_fn):
        """
        Modify the logging module's registered handlers and push a new context
        onto the stack.
        :param add_handlers_fn: function to modify the registered logging
        handlers. Accepts a context dictionary which may be modified.
        """
        self._flush_all_streams()
        context = self._get_context()

        add_handlers_fn(context)

        self._push_context(context)

    class _TaggingFormatter(logging.Formatter):

        """
        Delegates to a given formatter, but prefixes each line of output with a
        tag.
        """

        def __init__(self, base_formatter, tag):
            self.base_formatter = base_formatter
            prefix = tag + ' : '
            self._fmt = base_formatter._fmt.replace('%(message)s',
                                                    prefix + '%(message)s')
            self.datefmt = base_formatter.datefmt

    def _add_tagging_formatter(self, tag):
        for handler in _current_handlers():
            tagging_formatter = self._TaggingFormatter(handler.formatter, tag)
            handler.setFormatter(tagging_formatter)

    def _do_redirect(self, stream=None, filename=None, level=None,
                     clear_other_handlers=False):
        """
        :param clear_other_handlers - if true, clear out all other logging
        handlers.
        """
        assert bool(stream) != bool(filename)  # xor
        if not self._started:
            raise RuntimeError('You must call start_logging() before this')

        def add_handler(context):
            if clear_other_handlers:
                self._clear_all_handlers()

            if stream:
                handler = self.logging_config_object.add_stream_handler(stream)
            else:
                handler = self.logging_config_object.add_file_handler(filename)

            if level:
                handler.setLevel(level)

        self._add_log_handlers(add_handler)

    def redirect(self, filename):
        """Redirect output to the specified file"""
        self._do_redirect(filename=filename, clear_other_handlers=True)

    def redirect_to_stream(self, stream):
        """Redirect output to the given stream"""
        self._do_redirect(stream=stream, clear_other_handlers=True)

    def tee_redirect(self, filename, level=None):
        """Tee output to the specified file"""
        self._do_redirect(filename=filename, level=level)

    def tee_redirect_to_stream(self, stream):
        """Tee output to the given stream"""
        self._do_redirect(stream=stream)

    def tee_redirect_debug_dir(self, debug_dir, log_name=None, tag=None):
        """
        Tee output to a full new set of debug logs in the given directory.
        """
        def add_handlers(context):
            if tag:
                self._add_tagging_formatter(tag)
                context['tag_added'] = True
            self.logging_config_object.add_debug_file_handlers(
                debug_dir, log_name=log_name)
        self._add_log_handlers(add_handlers)

    def _restore_context(self, context):
        for stream_handler in self._streams:
            stream_handler.on_restore_context(context)

        # restore logging handlers
        old_handlers = context['old_handlers']
        for handler in _current_handlers() - old_handlers:
            handler.close()
        self._clear_all_handlers()
        for handler in old_handlers:
            logger.addHandler(handler)

        if 'tag_added' in context:
            for handler in _current_handlers():
                tagging_formatter = handler.formatter
                handler.setFormatter(tagging_formatter.base_formatter)

    def _pop_context(self):
        self._flush_all_streams()
        context = self._context_stack.pop()
        self._restore_context(context)

    def undo_redirect(self):
        """
        Undo the last redirection (that hasn't yet been undone).

        If any subprocesses have been launched since the redirection was
        performed, they must have ended by the time this is called.  Otherwise,
        this will hang waiting for the logging subprocess to end.
        """
        if not self._context_stack:
            raise RuntimeError('No redirects to undo')
        self._pop_context()

    def restore(self):
        """
        Same as undo_redirect().  For backwards compatibility with
        fd_stack.
        """
        self.undo_redirect()


class _FdRedirectionStreamManager(_StreamManager):

    """
    Like StreamManager, but also captures output from subprocesses by modifying
    the underlying file descriptors.

    For the underlying file descriptors, we spawn a subprocess that writes all
    input to the logging module, and we point the FD to that subprocess.  As a
    result, every time we redirect output we need to spawn a new subprocess to
    pick up the new logging settings (without disturbing any existing processes
    using the old logging subprocess).

    If, one day, we could get all code using utils.run() and friends to launch
    subprocesses, we'd no longer need to handle raw FD output, and we could
    get rid of all this business with subprocesses.  Another option would be
    to capture all stray output to a single, separate destination.
    """
    #继承了StreamManager，同时获取subprocess的输出，
    #打开一个子线程，去管道中读取父进程的log，目的是为了用子进程去获得最新的logging配置
    #如果有一天我们都是通过utils.run执行命令，就不需要这个奇怪的方法收集log

    def __init__(self, stream, level, stream_setter):
        if not hasattr(stream, 'fileno'):
            # with fake, in-process file objects, subprocess output won't be
            # captured. this should never happen in normal use, since the
            # factory methods will only pass sys.stdout and sys.stderr.
            raise ValueError("FdRedirectionLoggingManager won't work with "
                             "streams that aren't backed by file "
                             "descriptors")

        super(_FdRedirectionStreamManager, self).__init__(stream, level,
                                                          stream_setter)
        #self._fd直接指向stream的句柄
        self._fd = stream.fileno()
        self._fd_copy_stream = None

    def _point_stream_handlers_to_copy(self):
        """
        point logging StreamHandlers that point to this stream to a safe
        copy of the underlying FD. otherwise, StreamHandler output will go
        to the logging subprocess, effectively getting doubly logged.
        """

        #安全复制一个文件句柄
        fd_copy = os.dup(self._fd)
        #打开这个文件
        self._fd_copy_stream = os.fdopen(fd_copy, 'w')
        self._redirect_logging_stream_handlers(self._stream,
                                               self._fd_copy_stream)

    def _restore_stream_handlers(self):
        """ point logging StreamHandlers back to the original FD """
        #关闭那个用来用来复制的stream，把复制的handler又指回来
        self._redirect_logging_stream_handlers(self._fd_copy_stream,
                                               self._stream)
        self._fd_copy_stream.close()

    def _redirect_logging_stream_handlers(self, old_stream, new_stream):
        """
        Redirect all configured logging StreamHandlers pointing to
        old_stream to point to new_stream instead.
        """
        #将所有指向old_stream的handler重定向到新的stream中去
        #查找所有当前存在的handler，如果是StreamHandler，如果stream有fd
        #如果fd等于old_stream，那么删除旧的handler，添加一个新的StreamHandler，但是stream没有停
        for handler in _current_handlers():
            points_to_stream = (isinstance(handler, logging.StreamHandler) and
                                hasattr(handler.stream, 'fileno') and
                                handler.stream.fileno() == old_stream.fileno())
            if points_to_stream:
                logger.removeHandler(handler)
                handler.close()  # doesn't close the stream, just the handler

                new_handler = logging.StreamHandler(new_stream)
                new_handler.setLevel(handler.level)
                new_handler.setFormatter(handler.formatter)
                for log_filter in handler.filters:
                    new_handler.addFilter(log_filter)
                logger.addHandler(new_handler)

    def start_logging(self):
        super(_FdRedirectionStreamManager, self).start_logging()
        self._point_stream_handlers_to_copy()

    def stop_logging(self):
        super(_FdRedirectionStreamManager, self).stop_logging()
        self._restore_stream_handlers()

    def _spawn_logging_subprocess(self):
        """
        Spawn a subprocess to log all input to the logging module with the
        current settings, and direct output to it.
        """

        #Par将当前的log写入管道 write -->  child从管道中读取log，log出去
        read_end, write_end = os.pipe()
        pid = os.fork()
        if pid:  # parent
            #
            os.close(read_end)
            os.dup2(write_end, self._fd)  # point FD to the subprocess
            os.close(write_end)
            return pid
        else:  # child
            try:
                os.close(write_end)
                # ensure this subprocess doesn't hold any pipes to others
                os.close(1)
                os.close(2)
                self._run_logging_subprocess(read_end)  # never returns
            except Exception:
                # don't let exceptions in the child escape
                try:
                    logging.exception('Logging subprocess died:')
                finally:
                    os._exit(1)

    def _run_logging_subprocess(self, read_fd):
        """
        Always run from a subprocess.  Read from read_fd and write to the
        logging module until EOF.
        """
        signal.signal(signal.SIGTERM, signal.SIG_DFL)  # clear handler
        input_file = os.fdopen(read_fd, 'r')
        for line in iter(input_file.readline, ''):
            logging.log(self._level, line.rstrip('\n'))
        os._exit(0)

    def _context_id(self):
        return '%s_context' % id(self)

    def on_push_context(self, context):
        # adds a context dict for this stream, $id_context, with the following:
        # * old_fd: FD holding a copy of the managed FD before launching a new
        #   subprocess.
        # * child_pid: PID of the logging subprocess launched
        fd_copy = os.dup(self._fd)
        child_pid = self._spawn_logging_subprocess()
        my_context = {'old_fd': fd_copy, 'child_pid': child_pid}
        context[self._context_id()] = my_context

    def on_restore_context(self, context):
        my_context = context[self._context_id()]

        # shut down subprocess
        child_pid = my_context['child_pid']
        try:
            os.close(self._fd)
            os.waitpid(child_pid, 0)
        except OSError:
            logging.exception('Failed to cleanly shutdown logging subprocess:')

        # restore previous FD
        old_fd = my_context['old_fd']
        os.dup2(old_fd, self._fd)
        os.close(old_fd)


class FdRedirectionLoggingManager(LoggingManager):

    """
    A simple extension of LoggingManager to use FdRedirectionStreamManagers,
    so that managed streams have their underlying FDs redirected.
    """

    STREAM_MANAGER_CLASS = _FdRedirectionStreamManager

    def start_logging(self):
        super(FdRedirectionLoggingManager, self).start_logging()
        # spawn the initial logging subprocess
        self._push_context(self._get_context())

    def undo_redirect(self):
        # len == 1 would mean only start_logging() had been called (but no
        # redirects had occurred)
        if len(self._context_stack) < 2:
            raise RuntimeError('No redirects to undo')
        super(FdRedirectionLoggingManager, self).undo_redirect()
