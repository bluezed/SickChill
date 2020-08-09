import markdown2

from ..sickbeard import helpers
from .. import logger
from .common import PageTemplate
from .home import Home
from .routes import Route


@Route('/changes(/?.*)', name='changelog')
class HomeChangeLog(Home):
    def __init__(self, *args, **kwargs):
        super(HomeChangeLog, self).__init__(*args, **kwargs)

    def index(self, *args, **kwargs):
        # noinspection PyBroadException
        try:
            changes = helpers.getURL('https://sickchill.github.io/sickchill-news/CHANGES.md', session=helpers.make_session(), returns='text')
        except Exception:
            logger.debug('Could not load changes from repo, giving a link!')
            changes = _('Could not load changes from the repo. [Click here for CHANGES.md]({changes_url})').format(
                changes_url='https://sickchill.github.io/sickchill-news/CHANGES.md'
            )

        t = PageTemplate(rh=self, filename="markdown.mako")
        data = markdown2.markdown(changes if changes else _("The was a problem connecting to github, please refresh and try again"), extras=['header-ids'])

        return t.render(title=_("Changelog"), header=_("Changelog"), topmenu="system", data=data, controller="changes", action="index")
