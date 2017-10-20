from django.db import models

class CrawlerLogMessage(models.Model):
    """
    Used to enable a nice logging system, that is visible in the admin backend.
    """

    """
    String to identify a log message of type 'DEBUG'.
    """
    DEBUG = 'DEBUG'

    """
    String to identify a log message of type 'ERROR'.
    """
    ERROR = 'ERROR'

    """
    String to identify a log message of type 'INFO'.
    """
    INFO = 'INFO'

    """
    List of message log types.
    """
    MESSAGE_TYPES = [
        (DEBUG, DEBUG),
        (ERROR, ERROR),
        (INFO, INFO)
    ]

    """
    String to identify an object of type 'Game'.
    """
    Game = 'Game'

    """
    String to identify an object of type 'GameParticipation'.
    """
    GameParticipation = 'GameParticipation'

    """
    String to identify an object of type 'Venue'.
    """
    Venue = 'Venue'

    """
    String to identify an object of type 'Referee'.
    """
    Referee = 'Referee'

    """
    List of message log types.
    """
    OBJECT_TYPES = [
        (Game, Game),
        (GameParticipation, GameParticipation),
        (Venue, Venue),
        (Referee, Referee)
    ]
    date = models.DateTimeField(auto_now=True)
    message = models.TextField(
        help_text='The message to be shown in the backend.'
    )

    message_type = models.CharField(
        choices=MESSAGE_TYPES,
        default=INFO,
        max_length=17,
        help_text='The type of log message.'
    )

    object_type = models.CharField(
        choices=MESSAGE_TYPES,
        null=True,
        blank=True,
        max_length=30,
        help_text='The type of related object, if there is one.'
    )
    object_id = models.IntegerField(
        blank=True,
        null=True,
        help_text='The id of the related object, if there is one.'
    )

    def __str__(self):
        return "{}: {}...".format(self.message_type, self.message[0:27])