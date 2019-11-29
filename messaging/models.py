from django.db import models
from django.utils import timezone
from requests import Session


class Messenger(models.Model):
    ruler_name = models.CharField(max_length=64)
    username = models.CharField(max_length=64)
    # password needed in plaintext to be sent to game server
    password = models.CharField(max_length=64)
    active = models.BooleanField(default=False)


class Message(models.Model):
    category = models.CharField(max_length=64)
    subject = models.TextField()
    body = models.TextField()
    active = models.BooleanField(default=False)

    def personalize(self, player, field):
        ruler = player['leader']
        nation = player['nation']
        new_text = getattr(self, field)
        if '[[ruler]]' in new_text:
            new_text = new_text.replace('[[ruler]]', ruler)
        if '[[nation]]' in self.body:
            new_text = new_text.replace('[[nation]]]', nation)
        return new_text

    def send(self, contact, messenger):
        with Session() as s:
            login_payload = {
                'email': messenger.username,
                'password': messenger.password,
                'loginform': 'login'
            }
            s.post('https://politicsandwar.com/login/', data=login_payload, headers={'User-Agent': 'Mozilla/5.0'})

            body = self.personalize(self.body, contact)
            subject = self.personalize(self.subject, contact)
            payload = {
                'newconversation': 'true',
                'receiver': contact['leader'],
                'carboncopy': '',
                'subject': subject,
                'body': body,
                'sndmsg': 'Send+Message'
            }
            s.post('https://politicsandwar.com/inbox/message/', data=payload, headers={'User-Agent': 'Mozilla/5.0'})
            self.log(contact, messenger)

    def log(self, contact, messenger):
        # Dict keys for the contact come directly from the PW Nations API
        new_log = MessageLog(recipient_id=contact['nationid'], recipient_ruler=contact['leadername'],
                             messenger_id=messenger.nation_id, messenger_ruler=messenger.ruler,
                             message_category=self.category)
        new_log.save()


class MessageLog(models.Model):
    recipient_id = models.IntegerField()
    recipient_ruler = models.CharField(max_length=64)
    messenger_id = models.SmallIntegerField()
    # not a foreign key to messenger, so that messengers can be removed without messing up their associated logs
    messenger_ruler = models.CharField(max_length=64)
    date = models.DateTimeField(default=timezone.now)
    message_category = models.CharField(max_length=64)
