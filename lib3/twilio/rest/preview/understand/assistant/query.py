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


class QueryList(ListResource):
    """ PLEASE NOTE that this class contains preview products that are subject
    to change. Use them with caution. If you currently do not have developer
    preview access, please contact help@twilio.com. """

    def __init__(self, version, assistant_sid):
        """
        Initialize the QueryList

        :param Version version: Version that contains the resource
        :param assistant_sid: The unique ID of the parent Assistant.

        :returns: twilio.rest.preview.understand.assistant.query.QueryList
        :rtype: twilio.rest.preview.understand.assistant.query.QueryList
        """
        super(QueryList, self).__init__(version)

        # Path Solution
        self._solution = {'assistant_sid': assistant_sid, }
        self._uri = '/Assistants/{assistant_sid}/Queries'.format(**self._solution)

    def stream(self, language=values.unset, model_build=values.unset,
               status=values.unset, limit=None, page_size=None):
        """
        Streams QueryInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param unicode language: An ISO language-country string of the sample.
        :param unicode model_build: The Model Build Sid or unique name of the Model Build to be queried.
        :param unicode status: A string that described the query status. The values can be: pending_review, reviewed, discarded
        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.preview.understand.assistant.query.QueryInstance]
        """
        limits = self._version.read_limits(limit, page_size)

        page = self.page(
            language=language,
            model_build=model_build,
            status=status,
            page_size=limits['page_size'],
        )

        return self._version.stream(page, limits['limit'])

    def list(self, language=values.unset, model_build=values.unset,
             status=values.unset, limit=None, page_size=None):
        """
        Lists QueryInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param unicode language: An ISO language-country string of the sample.
        :param unicode model_build: The Model Build Sid or unique name of the Model Build to be queried.
        :param unicode status: A string that described the query status. The values can be: pending_review, reviewed, discarded
        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.preview.understand.assistant.query.QueryInstance]
        """
        return list(self.stream(
            language=language,
            model_build=model_build,
            status=status,
            limit=limit,
            page_size=page_size,
        ))

    def page(self, language=values.unset, model_build=values.unset,
             status=values.unset, page_token=values.unset, page_number=values.unset,
             page_size=values.unset):
        """
        Retrieve a single page of QueryInstance records from the API.
        Request is executed immediately

        :param unicode language: An ISO language-country string of the sample.
        :param unicode model_build: The Model Build Sid or unique name of the Model Build to be queried.
        :param unicode status: A string that described the query status. The values can be: pending_review, reviewed, discarded
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50

        :returns: Page of QueryInstance
        :rtype: twilio.rest.preview.understand.assistant.query.QueryPage
        """
        data = values.of({
            'Language': language,
            'ModelBuild': model_build,
            'Status': status,
            'PageToken': page_token,
            'Page': page_number,
            'PageSize': page_size,
        })

        response = self._version.page(method='GET', uri=self._uri, params=data, )

        return QueryPage(self._version, response, self._solution)

    def get_page(self, target_url):
        """
        Retrieve a specific page of QueryInstance records from the API.
        Request is executed immediately

        :param str target_url: API-generated URL for the requested results page

        :returns: Page of QueryInstance
        :rtype: twilio.rest.preview.understand.assistant.query.QueryPage
        """
        response = self._version.domain.twilio.request(
            'GET',
            target_url,
        )

        return QueryPage(self._version, response, self._solution)

    def create(self, language, query, tasks=values.unset, model_build=values.unset,
               field=values.unset):
        """
        Create the QueryInstance

        :param unicode language: An ISO language-country string of the sample.
        :param unicode query: A user-provided string that uniquely identifies this resource as an alternative to the sid. It can be up to 2048 characters long.
        :param unicode tasks: Constraints the query to a set of tasks. Useful when you need to constrain the paths the user can take. Tasks should be comma separated task-unique-name-1, task-unique-name-2
        :param unicode model_build: The Model Build Sid or unique name of the Model Build to be queried.
        :param unicode field: Constraints the query to a given Field with an task. Useful when you know the Field you are expecting. It accepts one field in the format task-unique-name-1:field-unique-name

        :returns: The created QueryInstance
        :rtype: twilio.rest.preview.understand.assistant.query.QueryInstance
        """
        data = values.of({
            'Language': language,
            'Query': query,
            'Tasks': tasks,
            'ModelBuild': model_build,
            'Field': field,
        })

        payload = self._version.create(method='POST', uri=self._uri, data=data, )

        return QueryInstance(self._version, payload, assistant_sid=self._solution['assistant_sid'], )

    def get(self, sid):
        """
        Constructs a QueryContext

        :param sid: A 34 character string that uniquely identifies this resource.

        :returns: twilio.rest.preview.understand.assistant.query.QueryContext
        :rtype: twilio.rest.preview.understand.assistant.query.QueryContext
        """
        return QueryContext(self._version, assistant_sid=self._solution['assistant_sid'], sid=sid, )

    def __call__(self, sid):
        """
        Constructs a QueryContext

        :param sid: A 34 character string that uniquely identifies this resource.

        :returns: twilio.rest.preview.understand.assistant.query.QueryContext
        :rtype: twilio.rest.preview.understand.assistant.query.QueryContext
        """
        return QueryContext(self._version, assistant_sid=self._solution['assistant_sid'], sid=sid, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Preview.Understand.QueryList>'


class QueryPage(Page):
    """ PLEASE NOTE that this class contains preview products that are subject
    to change. Use them with caution. If you currently do not have developer
    preview access, please contact help@twilio.com. """

    def __init__(self, version, response, solution):
        """
        Initialize the QueryPage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param assistant_sid: The unique ID of the parent Assistant.

        :returns: twilio.rest.preview.understand.assistant.query.QueryPage
        :rtype: twilio.rest.preview.understand.assistant.query.QueryPage
        """
        super(QueryPage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of QueryInstance

        :param dict payload: Payload response from the API

        :returns: twilio.rest.preview.understand.assistant.query.QueryInstance
        :rtype: twilio.rest.preview.understand.assistant.query.QueryInstance
        """
        return QueryInstance(self._version, payload, assistant_sid=self._solution['assistant_sid'], )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Preview.Understand.QueryPage>'


class QueryContext(InstanceContext):
    """ PLEASE NOTE that this class contains preview products that are subject
    to change. Use them with caution. If you currently do not have developer
    preview access, please contact help@twilio.com. """

    def __init__(self, version, assistant_sid, sid):
        """
        Initialize the QueryContext

        :param Version version: Version that contains the resource
        :param assistant_sid: The unique ID of the Assistant.
        :param sid: A 34 character string that uniquely identifies this resource.

        :returns: twilio.rest.preview.understand.assistant.query.QueryContext
        :rtype: twilio.rest.preview.understand.assistant.query.QueryContext
        """
        super(QueryContext, self).__init__(version)

        # Path Solution
        self._solution = {'assistant_sid': assistant_sid, 'sid': sid, }
        self._uri = '/Assistants/{assistant_sid}/Queries/{sid}'.format(**self._solution)

    def fetch(self):
        """
        Fetch the QueryInstance

        :returns: The fetched QueryInstance
        :rtype: twilio.rest.preview.understand.assistant.query.QueryInstance
        """
        payload = self._version.fetch(method='GET', uri=self._uri, )

        return QueryInstance(
            self._version,
            payload,
            assistant_sid=self._solution['assistant_sid'],
            sid=self._solution['sid'],
        )

    def update(self, sample_sid=values.unset, status=values.unset):
        """
        Update the QueryInstance

        :param unicode sample_sid: An optional reference to the Sample created from this query.
        :param unicode status: A string that described the query status. The values can be: pending_review, reviewed, discarded

        :returns: The updated QueryInstance
        :rtype: twilio.rest.preview.understand.assistant.query.QueryInstance
        """
        data = values.of({'SampleSid': sample_sid, 'Status': status, })

        payload = self._version.update(method='POST', uri=self._uri, data=data, )

        return QueryInstance(
            self._version,
            payload,
            assistant_sid=self._solution['assistant_sid'],
            sid=self._solution['sid'],
        )

    def delete(self):
        """
        Deletes the QueryInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._version.delete(method='DELETE', uri=self._uri, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Preview.Understand.QueryContext {}>'.format(context)


class QueryInstance(InstanceResource):
    """ PLEASE NOTE that this class contains preview products that are subject
    to change. Use them with caution. If you currently do not have developer
    preview access, please contact help@twilio.com. """

    def __init__(self, version, payload, assistant_sid, sid=None):
        """
        Initialize the QueryInstance

        :returns: twilio.rest.preview.understand.assistant.query.QueryInstance
        :rtype: twilio.rest.preview.understand.assistant.query.QueryInstance
        """
        super(QueryInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'account_sid': payload.get('account_sid'),
            'date_created': deserialize.iso8601_datetime(payload.get('date_created')),
            'date_updated': deserialize.iso8601_datetime(payload.get('date_updated')),
            'results': payload.get('results'),
            'language': payload.get('language'),
            'model_build_sid': payload.get('model_build_sid'),
            'query': payload.get('query'),
            'sample_sid': payload.get('sample_sid'),
            'assistant_sid': payload.get('assistant_sid'),
            'sid': payload.get('sid'),
            'status': payload.get('status'),
            'url': payload.get('url'),
            'source_channel': payload.get('source_channel'),
        }

        # Context
        self._context = None
        self._solution = {'assistant_sid': assistant_sid, 'sid': sid or self._properties['sid'], }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context

        :returns: QueryContext for this QueryInstance
        :rtype: twilio.rest.preview.understand.assistant.query.QueryContext
        """
        if self._context is None:
            self._context = QueryContext(
                self._version,
                assistant_sid=self._solution['assistant_sid'],
                sid=self._solution['sid'],
            )
        return self._context

    @property
    def account_sid(self):
        """
        :returns: The unique ID of the Account that created this Query.
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def date_created(self):
        """
        :returns: The date that this resource was created
        :rtype: datetime
        """
        return self._properties['date_created']

    @property
    def date_updated(self):
        """
        :returns: The date that this resource was last updated
        :rtype: datetime
        """
        return self._properties['date_updated']

    @property
    def results(self):
        """
        :returns: The natural language analysis results which include the Task recognized, the confidence score and a list of identified Fields.
        :rtype: dict
        """
        return self._properties['results']

    @property
    def language(self):
        """
        :returns: An ISO language-country string of the sample.
        :rtype: unicode
        """
        return self._properties['language']

    @property
    def model_build_sid(self):
        """
        :returns: The unique ID of the Model Build queried.
        :rtype: unicode
        """
        return self._properties['model_build_sid']

    @property
    def query(self):
        """
        :returns: The end-user's natural language input.
        :rtype: unicode
        """
        return self._properties['query']

    @property
    def sample_sid(self):
        """
        :returns: An optional reference to the Sample created from this query.
        :rtype: unicode
        """
        return self._properties['sample_sid']

    @property
    def assistant_sid(self):
        """
        :returns: The unique ID of the parent Assistant.
        :rtype: unicode
        """
        return self._properties['assistant_sid']

    @property
    def sid(self):
        """
        :returns: A 34 character string that uniquely identifies this resource.
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def status(self):
        """
        :returns: A string that described the query status. The values can be: pending_review, reviewed, discarded
        :rtype: unicode
        """
        return self._properties['status']

    @property
    def url(self):
        """
        :returns: The url
        :rtype: unicode
        """
        return self._properties['url']

    @property
    def source_channel(self):
        """
        :returns: The communication channel where this end-user input came from
        :rtype: unicode
        """
        return self._properties['source_channel']

    def fetch(self):
        """
        Fetch the QueryInstance

        :returns: The fetched QueryInstance
        :rtype: twilio.rest.preview.understand.assistant.query.QueryInstance
        """
        return self._proxy.fetch()

    def update(self, sample_sid=values.unset, status=values.unset):
        """
        Update the QueryInstance

        :param unicode sample_sid: An optional reference to the Sample created from this query.
        :param unicode status: A string that described the query status. The values can be: pending_review, reviewed, discarded

        :returns: The updated QueryInstance
        :rtype: twilio.rest.preview.understand.assistant.query.QueryInstance
        """
        return self._proxy.update(sample_sid=sample_sid, status=status, )

    def delete(self):
        """
        Deletes the QueryInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._proxy.delete()

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Preview.Understand.QueryInstance {}>'.format(context)
