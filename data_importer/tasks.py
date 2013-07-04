#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

try:
    from celery.task import task
except ImportError:
    from celery.decorators import task


class DataImpoterTask(Task):
    """
    This tasks is executed by Celery.
    """
    name = 'flowbot.add_pending_jobs_to_flowbot'
    queue = settings.DATA_IMPORTER_QUEUE
    time_limit = 60 * 15

    def run(self, flowbot=FlowBot.get_instance(), **kwargs):
        logger = self.get_logger(**kwargs)
        lock_id = "%s-lock" % (self.name)
        errors = []

        if acquire_lock(lock_id):
            jobs_queryset = Job.objects.filter(state='not sent', transaction__cancelled=False).order_by('id')
            for job in jobs_queryset:
                try:
                    job.add_to_flowbot(flowbot=flowbot)
                except FlowBotConnectionError:
                    pass  # we want to ignore connection errors
                except (Exception, FlowBotError) as e:
                    errors.append(unicode(e))

                if errors:
                    logger.error(unicode(errors))

            count_jobs = jobs_queryset.count()
            release_lock(lock_id)
            logger.info("TASK FINISH: %s %s" % (lock_id, datetime.now()))
            return count_jobs

        else:
            logger.info('TASK LOCKED ADDPENDINGJOB- %s' % (datetime.now()))
            return 0
