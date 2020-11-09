"""Some predefined users and tweets."""

from .models import User, Tweet

USERS = [
    User(id=1, name='Mady'),
    User(id=2, name='Moses')
]

TWEETS = [
    Tweet(id=1, user=USERS[1],
          text='But why is it that I, a lecturer, cannot bear to be lectured?'),
    Tweet(id=2, user=USERS[0],
          text='*Straightens at once to hit him in the face.*'),
    Tweet(id=3, user=USERS[1],
          text="Do you think that any Christian in the twentieth century has the right to speak of Jewish Pharisees? From a Jewish standpoint, you know, this hasn't been one of your best periods."),
    Tweet(id=4, user=USERS[1],
          text='"No," I said violently.'),
    Tweet(id=5, user=USERS[0],
          text='I now naturally turn to Berdyaev.'),
    Tweet(id=6, user=USERS[1],
          text='Foo to all those categories!')
]