# coding=utf-8
r"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base import deserialize
from twilio.base import values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.page import Page
from twilio.rest.taskrouter.v1.workspace.task_queue.task_queue_cumulative_statistics import TaskQueueCumulativeStatisticsList
from twilio.rest.taskrouter.v1.workspace.task_queue.task_queue_real_time_statistics import TaskQueueRealTimeStatisticsList
from twilio.rest.taskrouter.v1.workspace.task_queue.task_queue_statistics import TaskQueueStatisticsList
from twilio.rest.taskrouter.v1.workspace.task_queue.task_queues_statistics import TaskQueuesStatisticsList


class TaskQueueList(ListResource):
    """  """

    def __init__(self, version, workspace_sid):
        """
        Initialize the TaskQueueList

        :param Version version: Version that contains the resource
        :param workspace_sid: The SID of the Workspace that contains the TaskQueue

        :returns: twilio.rest.taskrouter.v1.workspace.task_queue.TaskQueueList
        :rtype: twilio.rest.taskrouter.v1.workspace.task_queue.TaskQueueList
        """
        super(TaskQueueList, self).__init__(version)

        # Path Solution
        self._solution = {'workspace_sid': workspace_sid, }
        self._uri = '/Workspaces/{workspace_sid}/TaskQueues'.format(**self._solution)

        # Components
        self._statistics = None

    def stream(self, friendly_name=values.unset,
               evaluate_worker_attributes=values.unset, worker_sid=values.unset,
               limit=None, page_size=None):
        """
        Streams TaskQueueInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param unicode friendly_name: The friendly_name of the TaskQueue resources to read
        :param unicode evaluate_worker_attributes: The attributes of the Workers to read
        :param unicode worker_sid: The SID of the Worker with the TaskQueue resources to read
        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.taskrouter.v1.workspace.task_queue.TaskQueueInstance]
        """
        limits = self._version.read_limits(limit, page_size)

        page = self.page(
            friendly_name=friendly_name,
            evaluate_worker_attributes=evaluate_worker_attributes,
            worker_sid=worker_sid,
            page_size=limits['page_size'],
        )

        return self._version.stream(page, limits['limit'], limits['page_limit'])

    def list(self, friendly_name=values.unset,
             evaluate_worker_attributes=values.unset, worker_sid=values.unset,
             limit=None, page_size=None):
        """
        Lists TaskQueueInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param unicode friendly_name: The friendly_name of the TaskQueue resources to read
        :param unicode evaluate_worker_attributes: The attributes of the Workers to read
        :param unicode worker_sid: The SID of the Worker with the TaskQueue resources to read
        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.taskrouter.v1.workspace.task_queue.TaskQueueInstance]
        """
        return list(self.stream(
            friendly_name=friendly_name,
            evaluate_worker_attributes=evaluate_worker_attributes,
            worker_sid=worker_sid,
            limit=limit,
            page_size=page_size,
        ))

    def page(self, friendly_name=values.unset,
             evaluate_worker_attributes=values.unset, worker_sid=values.unset,
             page_token=values.unset, page_number=values.unset,
             page_size=values.unset):
        """
        Retrieve a single page of TaskQueueInstance records from the API.
        Request is executed immediately

        :param unicode friendly_name: The friendly_name of the TaskQueue resources to read
        :param unicode evaluate_worker_attributes: The attributes of the Workers to read
        :param unicode worker_sid: The SID of the Worker with the TaskQueue resources to read
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50

        :returns: Page of TaskQueueInstance
        :rtype: twilio.rest.taskrouter.v1.workspace.task_queue.TaskQueuePage
        """
        data = values.of({
            'FriendlyName': friendly_name,
            'EvaluateWorkerAttributes': evaluate_worker_attributes,
            'WorkerSid': worker_sid,
            'PageToken': page_token,
            'Page': page_number,
            'PageSize': page_size,
        })

        response = self._version.page(method='GET', uri=self._uri, params=data, )

        return TaskQueuePage(self._version, response, self._solution)

    def get_page(self, target_url):
        """
        Retrieve a specific page of TaskQueueInstance records from the API.
        Request is executed immediately

        :param str target_url: API-generated URL for the requested results page

        :returns: Page of TaskQueueInstance
        :rtype: twilio.rest.taskrouter.v1.workspace.task_queue.TaskQueuePage
        """
        response = self._version.domain.twilio.request(
            'GET',
            target_url,
        )

        return TaskQueuePage(self._version, response, self._solution)

    def create(self, friendly_name, target_workers=values.unset,
               max_reserved_workers=values.unset, task_order=values.unset,
               reservation_activity_sid=values.unset,
               assignment_activity_sid=values.unset):
        """
        Create the TaskQueueInstance

        :param unicode friendly_name: A string to describe the resource
        :param unicode target_workers: A string describing the Worker selection criteria for any Tasks that enter the TaskQueue
        :param unicode max_reserved_workers: The maximum number of Workers to reserve
        :param TaskQueueInstance.TaskOrder task_order: How Tasks will be assigned to Workers
        :param unicode reservation_activity_sid: The SID of the Activity to assign Workers when a task is reserved for them
        :param unicode assignment_activity_sid: The SID of the Activity to assign Workers once a task is assigned to them

        :returns: The created TaskQueueInstance
        :rtype: twilio.rest.taskrouter.v1.workspace.task_queue.TaskQueueInstance
        """
        data = values.of({
            'FriendlyName': friendly_name,
            'TargetWorkers': target_workers,
            'MaxReservedWorkers': max_reserved_workers,
            'TaskOrder': task_order,
            'ReservationActivitySid': reservation_activity_sid,
            'AssignmentActivitySid': assignment_activity_sid,
        })

        payload = self._version.create(method='POST', uri=self._uri, data=data, )

        return TaskQueueInstance(self._version, payload, workspace_sid=self._solution['workspace_sid'], )

    @property
    def statistics(self):
        """
        Access the statistics

        :returns: twilio.rest.taskrouter.v1.workspace.task_queue.task_queues_statistics.TaskQueuesStatisticsList
        :rtype: twilio.rest.taskrouter.v1.workspace.task_queue.task_queues_statistics.TaskQueuesStatisticsList
        """
        if self._statistics is None:
            self._statistics = TaskQueuesStatisticsList(
                self._version,
                workspace_sid=self._solution['workspace_sid'],
            )
        return self._statistics

    def get(self, sid):
        """
        Constructs a TaskQueueContext

        :param sid: The SID of the resource to

        :returns: twilio.rest.taskrouter.v1.workspace.task_queue.TaskQueueContext
        :rtype: twilio.rest.taskrouter.v1.workspace.task_queue.TaskQueueContext
        """
        return TaskQueueContext(self._version, workspace_sid=self._solution['workspace_sid'], sid=sid, )

    def __call__(self, sid):
        """
        Constructs a TaskQueueContext

        :param sid: The SID of the resource to

        :returns: twilio.rest.taskrouter.v1.workspace.task_queue.TaskQueueContext
        :rtype: twilio.rest.taskrouter.v1.workspace.task_queue.TaskQueueContext
        """
        return TaskQueueContext(self._version, workspace_sid=self._solution['workspace_sid'], sid=sid, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Taskrouter.V1.TaskQueueList>'


class TaskQueuePage(Page):
    """  """

    def __init__(self, version, response, solution):
        """
        Initialize the TaskQueuePage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param workspace_sid: The SID of the Workspace that contains the TaskQueue

        :returns: twilio.rest.taskrouter.v1.workspace.task_queue.TaskQueuePage
        :rtype: twilio.rest.taskrouter.v1.workspace.task_queue.TaskQueuePage
        """
        super(TaskQueuePage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of TaskQueueInstance

        :param dict payload: Payload response from the API

        :returns: twilio.rest.taskrouter.v1.workspace.task_queue.TaskQueueInstance
        :rtype: twilio.rest.taskrouter.v1.workspace.task_queue.TaskQueueInstance
        """
        return TaskQueueInstance(self._version, payload, workspace_sid=self._solution['workspace_sid'], )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Taskrouter.V1.TaskQueuePage>'


class TaskQueueContext(InstanceContext):
    """  """

    def __init__(self, version, workspace_sid, sid):
        """
        Initialize the TaskQueueContext

        :param Version version: Version that contains the resource
        :param workspace_sid: The SID of the Workspace with the TaskQueue to fetch
        :param sid: The SID of the resource to

        :returns: twilio.rest.taskrouter.v1.workspace.task_queue.TaskQueueContext
        :rtype: twilio.rest.taskrouter.v1.workspace.task_queue.TaskQueueContext
        """
        super(TaskQueueContext, self).__init__(version)

        # Path Solution
        self._solution = {'workspace_sid': workspace_sid, 'sid': sid, }
        self._uri = '/Workspaces/{workspace_sid}/TaskQueues/{sid}'.format(**self._solution)

        # Dependents
        self._statistics = None
        self._real_time_statistics = None
        self._cumulative_statistics = None

    def fetch(self):
        """
        Fetch the TaskQueueInstance

        :returns: The fetched TaskQueueInstance
        :rtype: twilio.rest.taskrouter.v1.workspace.task_queue.TaskQueueInstance
        """
        payload = self._version.fetch(method='GET', uri=self._uri, )

        return TaskQueueInstance(
            self._version,
            payload,
            workspace_sid=self._solution['workspace_sid'],
            sid=self._solution['sid'],
        )

    def update(self, friendly_name=values.unset, target_workers=values.unset,
               reservation_activity_sid=values.unset,
               assignment_activity_sid=values.unset,
               max_reserved_workers=values.unset, task_order=values.unset):
        """
        Update the TaskQueueInstance

        :param unicode friendly_name: A string to describe the resource
        :param unicode target_workers: A string describing the Worker selection criteria for any Tasks that enter the TaskQueue
        :param unicode reservation_activity_sid: The SID of the Activity to assign Workers when a task is reserved for them
        :param unicode assignment_activity_sid: The SID of the Activity to assign Workers when a task is assigned for them
        :param unicode max_reserved_workers: The maximum number of Workers to create reservations for the assignment of a task while in the queue
        :param TaskQueueInstance.TaskOrder task_order: How Tasks will be assigned to Workers

        :returns: The updated TaskQueueInstance
        :rtype: twilio.rest.taskrouter.v1.workspace.task_queue.TaskQueueInstance
        """
        data = values.of({
            'FriendlyName': friendly_name,
            'TargetWorkers': target_workers,
            'ReservationActivitySid': reservation_activity_sid,
            'AssignmentActivitySid': assignment_activity_sid,
            'MaxReservedWorkers': max_reserved_workers,
            'TaskOrder': task_order,
        })

        payload = self._version.update(method='POST', uri=self._uri, data=data, )

        return TaskQueueInstance(
            self._version,
            payload,
            workspace_sid=self._solution['workspace_sid'],
            sid=self._solution['sid'],
        )

    def delete(self):
        """
        Deletes the TaskQueueInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._version.delete(method='DELETE', uri=self._uri, )

    @property
    def statistics(self):
        """
        Access the statistics

        :returns: twilio.rest.taskrouter.v1.workspace.task_queue.task_queue_statistics.TaskQueueStatisticsList
        :rtype: twilio.rest.taskrouter.v1.workspace.task_queue.task_queue_statistics.TaskQueueStatisticsList
        """
        if self._statistics is None:
            self._statistics = TaskQueueStatisticsList(
                self._version,
                workspace_sid=self._solution['workspace_sid'],
                task_queue_sid=self._solution['sid'],
            )
        return self._statistics

    @property
    def real_time_statistics(self):
        """
        Access the real_time_statistics

        :returns: twilio.rest.taskrouter.v1.workspace.task_queue.task_queue_real_time_statistics.TaskQueueRealTimeStatisticsList
        :rtype: twilio.rest.taskrouter.v1.workspace.task_queue.task_queue_real_time_statistics.TaskQueueRealTimeStatisticsList
        """
        if self._real_time_statistics is None:
            self._real_time_statistics = TaskQueueRealTimeStatisticsList(
                self._version,
                workspace_sid=self._solution['workspace_sid'],
                task_queue_sid=self._solution['sid'],
            )
        return self._real_time_statistics

    @property
    def cumulative_statistics(self):
        """
        Access the cumulative_statistics

        :returns: twilio.rest.taskrouter.v1.workspace.task_queue.task_queue_cumulative_statistics.TaskQueueCumulativeStatisticsList
        :rtype: twilio.rest.taskrouter.v1.workspace.task_queue.task_queue_cumulative_statistics.TaskQueueCumulativeStatisticsList
        """
        if self._cumulative_statistics is None:
            self._cumulative_statistics = TaskQueueCumulativeStatisticsList(
                self._version,
                workspace_sid=self._solution['workspace_sid'],
                task_queue_sid=self._solution['sid'],
            )
        return self._cumulative_statistics

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Taskrouter.V1.TaskQueueContext {}>'.format(context)


class TaskQueueInstance(InstanceResource):
    """  """

    class TaskOrder(object):
        FIFO = "FIFO"
        LIFO = "LIFO"

    def __init__(self, version, payload, workspace_sid, sid=None):
        """
        Initialize the TaskQueueInstance

        :returns: twilio.rest.taskrouter.v1.workspace.task_queue.TaskQueueInstance
        :rtype: twilio.rest.taskrouter.v1.workspace.task_queue.TaskQueueInstance
        """
        super(TaskQueueInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'account_sid': payload.get('account_sid'),
            'assignment_activity_sid': payload.get('assignment_activity_sid'),
            'assignment_activity_name': payload.get('assignment_activity_name'),
            'date_created': deserialize.iso8601_datetime(payload.get('date_created')),
            'date_updated': deserialize.iso8601_datetime(payload.get('date_updated')),
            'friendly_name': payload.get('friendly_name'),
            'max_reserved_workers': deserialize.integer(payload.get('max_reserved_workers')),
            'reservation_activity_sid': payload.get('reservation_activity_sid'),
            'reservation_activity_name': payload.get('reservation_activity_name'),
            'sid': payload.get('sid'),
            'target_workers': payload.get('target_workers'),
            'task_order': payload.get('task_order'),
            'url': payload.get('url'),
            'workspace_sid': payload.get('workspace_sid'),
            'links': payload.get('links'),
        }

        # Context
        self._context = None
        self._solution = {'workspace_sid': workspace_sid, 'sid': sid or self._properties['sid'], }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context

        :returns: TaskQueueContext for this TaskQueueInstance
        :rtype: twilio.rest.taskrouter.v1.workspace.task_queue.TaskQueueContext
        """
        if self._context is None:
            self._context = TaskQueueContext(
                self._version,
                workspace_sid=self._solution['workspace_sid'],
                sid=self._solution['sid'],
            )
        return self._context

    @property
    def account_sid(self):
        """
        :returns: The SID of the Account that created the resource
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def assignment_activity_sid(self):
        """
        :returns: The SID of the Activity to assign Workers when a task is assigned for them
        :rtype: unicode
        """
        return self._properties['assignment_activity_sid']

    @property
    def assignment_activity_name(self):
        """
        :returns: The name of the Activity to assign Workers when a task is assigned for them
        :rtype: unicode
        """
        return self._properties['assignment_activity_name']

    @property
    def date_created(self):
        """
        :returns: The RFC 2822 date and time in GMT when the resource was created
        :rtype: datetime
        """
        return self._properties['date_created']

    @property
    def date_updated(self):
        """
        :returns: The RFC 2822 date and time in GMT when the resource was last updated
        :rtype: datetime
        """
        return self._properties['date_updated']

    @property
    def friendly_name(self):
        """
        :returns: The string that you assigned to describe the resource
        :rtype: unicode
        """
        return self._properties['friendly_name']

    @property
    def max_reserved_workers(self):
        """
        :returns: The maximum number of Workers to reserve
        :rtype: unicode
        """
        return self._properties['max_reserved_workers']

    @property
    def reservation_activity_sid(self):
        """
        :returns: The SID of the Activity to assign Workers once a task is reserved for them
        :rtype: unicode
        """
        return self._properties['reservation_activity_sid']

    @property
    def reservation_activity_name(self):
        """
        :returns: The name of the Activity to assign Workers once a task is reserved for them
        :rtype: unicode
        """
        return self._properties['reservation_activity_name']

    @property
    def sid(self):
        """
        :returns: The unique string that identifies the resource
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def target_workers(self):
        """
        :returns: A string describing the Worker selection criteria for any Tasks that enter the TaskQueue
        :rtype: unicode
        """
        return self._properties['target_workers']

    @property
    def task_order(self):
        """
        :returns: How Tasks will be assigned to Workers
        :rtype: TaskQueueInstance.TaskOrder
        """
        return self._properties['task_order']

    @property
    def url(self):
        """
        :returns: The absolute URL of the TaskQueue resource
        :rtype: unicode
        """
        return self._properties['url']

    @property
    def workspace_sid(self):
        """
        :returns: The SID of the Workspace that contains the TaskQueue
        :rtype: unicode
        """
        return self._properties['workspace_sid']

    @property
    def links(self):
        """
        :returns: The URLs of related resources
        :rtype: unicode
        """
        return self._properties['links']

    def fetch(self):
        """
        Fetch the TaskQueueInstance

        :returns: The fetched TaskQueueInstance
        :rtype: twilio.rest.taskrouter.v1.workspace.task_queue.TaskQueueInstance
        """
        return self._proxy.fetch()

    def update(self, friendly_name=values.unset, target_workers=values.unset,
               reservation_activity_sid=values.unset,
               assignment_activity_sid=values.unset,
               max_reserved_workers=values.unset, task_order=values.unset):
        """
        Update the TaskQueueInstance

        :param unicode friendly_name: A string to describe the resource
        :param unicode target_workers: A string describing the Worker selection criteria for any Tasks that enter the TaskQueue
        :param unicode reservation_activity_sid: The SID of the Activity to assign Workers when a task is reserved for them
        :param unicode assignment_activity_sid: The SID of the Activity to assign Workers when a task is assigned for them
        :param unicode max_reserved_workers: The maximum number of Workers to create reservations for the assignment of a task while in the queue
        :param TaskQueueInstance.TaskOrder task_order: How Tasks will be assigned to Workers

        :returns: The updated TaskQueueInstance
        :rtype: twilio.rest.taskrouter.v1.workspace.task_queue.TaskQueueInstance
        """
        return self._proxy.update(
            friendly_name=friendly_name,
            target_workers=target_workers,
            reservation_activity_sid=reservation_activity_sid,
            assignment_activity_sid=assignment_activity_sid,
            max_reserved_workers=max_reserved_workers,
            task_order=task_order,
        )

    def delete(self):
        """
        Deletes the TaskQueueInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._proxy.delete()

    @property
    def statistics(self):
        """
        Access the statistics

        :returns: twilio.rest.taskrouter.v1.workspace.task_queue.task_queue_statistics.TaskQueueStatisticsList
        :rtype: twilio.rest.taskrouter.v1.workspace.task_queue.task_queue_statistics.TaskQueueStatisticsList
        """
        return self._proxy.statistics

    @property
    def real_time_statistics(self):
        """
        Access the real_time_statistics

        :returns: twilio.rest.taskrouter.v1.workspace.task_queue.task_queue_real_time_statistics.TaskQueueRealTimeStatisticsList
        :rtype: twilio.rest.taskrouter.v1.workspace.task_queue.task_queue_real_time_statistics.TaskQueueRealTimeStatisticsList
        """
        return self._proxy.real_time_statistics

    @property
    def cumulative_statistics(self):
        """
        Access the cumulative_statistics

        :returns: twilio.rest.taskrouter.v1.workspace.task_queue.task_queue_cumulative_statistics.TaskQueueCumulativeStatisticsList
        :rtype: twilio.rest.taskrouter.v1.workspace.task_queue.task_queue_cumulative_statistics.TaskQueueCumulativeStatisticsList
        """
        return self._proxy.cumulative_statistics

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Taskrouter.V1.TaskQueueInstance {}>'.format(context)