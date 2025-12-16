import os
import django
from pymongo import MongoClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes_project.settings")
django.setup()

from quotes.models import Author, Quote, Tag
from django.contrib.auth.models import User

client = MongoClient("mongodb://localhost:27017")
db = client.quotes

user = User.objects.first()

for item in db.quotes.find():
    author, _ = Author.objects.get_or_create(fullname=item['author'])
    quote = Quote.objects.create(
        quote=item['quote'],
        author=author,
        created_by=user
    )

    for tag in item['tags']:
        tag_obj, _ = Tag.objects.get_or_create(name=tag)
        quote.tags.add(tag_obj)
