try:
    import autotest.common as common
except ImportError:
    import common

import os
from autotest.client.shared import logging_config
from autotest.client.shared.settings import settings


class ClientLoggingConfig(logging_config.LoggingConfig):
    """
    1.首先调用super(ClientLoggingConfig, self).configure_logging，生成两个handler指向stdout和stderr
    2.然后如果有result dir，调用add_debug_file_handlers，生成4个filehandler,指向resultdir/debug/
    3.在test.py中会调用job.logging.tee_redirect_debug_dir(self.debugdir,log_name=self.tagged_testname)
        这是manager的函数，会再次调用到add_debug_file_handlers函数，在debugdir里面重新创建4个filehandler
    """





    def add_debug_file_handlers(self, log_dir, log_name=None):
        #增加4个handler指向4个级别
        if not log_name:
            log_name = settings.get_value('CLIENT', 'default_logging_name',
                                          type=str, default='client')
        self._add_file_handlers_for_all_levels(log_dir, log_name)
    #这个方法将对logging进行配置，job.py中传入的值为：result_dir=self.resultdir
    #verbose=option.verbose
    def configure_logging(self, results_dir=None, verbose=False):
        super(ClientLoggingConfig, self).configure_logging(
            use_console=self.use_console,
            verbose=verbose)

        if results_dir:
            #如果存在resultdir，在resultdir下，创建debug
            log_dir = os.path.join(results_dir, 'debug')
            if not os.path.exists(log_dir):
                os.mkdir(log_dir)
            self.add_debug_file_handlers(log_dir)
