# coding=utf-8
r"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base.version import Version
from twilio.rest.studio.v2.flow import FlowList
from twilio.rest.studio.v2.flow_validate import FlowValidateList


class V2(Version):

    def __init__(self, domain):
        """
        Initialize the V2 version of Studio

        :returns: V2 version of Studio
        :rtype: twilio.rest.studio.v2.V2.V2
        """
        super(V2, self).__init__(domain)
        self.version = 'v2'
        self._flows = None
        self._flow_validate = None

    @property
    def flows(self):
        """
        :rtype: twilio.rest.studio.v2.flow.FlowList
        """
        if self._flows is None:
            self._flows = FlowList(self)
        return self._flows

    @property
    def flow_validate(self):
        """
        :rtype: twilio.rest.studio.v2.flow_validate.FlowValidateList
        """
        if self._flow_validate is None:
            self._flow_validate = FlowValidateList(self)
        return self._flow_validate

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Studio.V2>'