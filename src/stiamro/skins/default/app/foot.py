from datetime import datetime
from zope.viewlet.viewlet import ViewletBase
from zope.app.applicationcontrol.applicationcontrol import applicationController

class FootViewlet(ViewletBase):
    @property
    def started(self):
        stamp = applicationController.getStartTime()
        try:
            stamp = datetime.fromtimestamp(stamp)
        except (ValueError, TypeError), err:
            return stamp
        else:
            return stamp.strftime('%d%m%Y%H%M')
