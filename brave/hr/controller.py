# encoding: utf-8

from __future__ import unicode_literals

from web.auth import authenticated, user
from web.core import Controller

from brave.hr.util import StartupMixIn
from brave.hr.auth.controller import AuthenticationMixIn
from brave.hr.auth.model import Ticket

log = __import__('logging').getLogger(__name__)


class RootController(Controller, StartupMixIn, AuthenticationMixIn):
    def index(self):
        if authenticated:
            return 'brave.hr.template.index', dict()

        return 'brave.hr.template.welcome', dict()

    def search(self, character=None, submit=False):
        if not character:
            return 'brave.hr.template.search', dict()
        
        char = Ticket.objects(character__name__istartswith=character).first()
        if not char:
            return 'brave.hr.template.search', dict(success=False, character=character)

        char = Ticket.authenticate(char.token)[1]

        return 'brave.hr.template.search', dict(success=True, eligible='eligible' in char.tags, character=char.character.name)
