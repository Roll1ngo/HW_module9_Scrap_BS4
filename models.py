from mongoengine import *

connect(
    db='HWMongoDB',
    host='mongodb+srv://Vladislav_B:dIvg5BCNadnWGk7E@hwmongobase.o1jywze.mongodb.net/?retryWrites=true&w=majority'
)


class Author(Document):
    meta = {'collection': 'authors'}
    fullname = StringField(max_length=100, required=True, unique=True)
    born_date = StringField(max_value=30)
    born_location = StringField()
    description = StringField()


class Quote(Document):
    meta = {'collection': 'quotes'}
    author = ReferenceField(Author)
    tags = ListField(StringField(max_length=50))
    quote = StringField()
