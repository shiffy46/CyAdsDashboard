from django.db import models

# Create your models here.
class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Language(models.Model):
    """
    Model representing a Language (e.g. English, French, Japanese, etc.)
    """
    name = models.CharField(max_length=200, help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

from django.urls import reverse # Used to generate URLs by reversing the URL patterns

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)


    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

import uuid # Required for unique book instances

class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CatalogAuthor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalog_author'


class CatalogBook(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    isbn = models.CharField(max_length=13)
    author = models.ForeignKey(CatalogAuthor, models.DO_NOTHING, blank=True, null=True)
    language = models.ForeignKey('CatalogLanguage', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalog_book'


class CatalogBookGenre(models.Model):
    book = models.ForeignKey(CatalogBook, models.DO_NOTHING)
    genre = models.ForeignKey('CatalogGenre', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'catalog_book_genre'
        unique_together = (('book', 'genre'),)


class CatalogBookinstance(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=1)
    book = models.ForeignKey(CatalogBook, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalog_bookinstance'


class CatalogGenre(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'catalog_genre'


class CatalogLanguage(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'catalog_language'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ProcessorAdFoundWatchlog(models.Model):
    attempt = models.IntegerField()
    request_timestamp = models.BigIntegerField()
    ad_source = models.CharField(max_length=50)
    ad_duration = models.IntegerField()
    ad_skip_duration = models.IntegerField()
    ad_system = models.CharField(max_length=255)
    ad_video = models.ForeignKey('ProcessorVideos', models.DO_NOTHING)
    batch = models.ForeignKey('ProcessorBatch', models.DO_NOTHING)
    bot = models.ForeignKey('ProcessorBots', models.DO_NOTHING)
    video_watched = models.ForeignKey('ProcessorVideos', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'processor_ad_found_watchlog'


class ProcessorBatch(models.Model):
    start_timestamp = models.BigIntegerField()
    completed_timestamp = models.BigIntegerField()
    time_taken = models.IntegerField()
    total_bots = models.IntegerField()
    server_hostname = models.CharField(max_length=30)
    server_container = models.CharField(max_length=30)
    external_ip = models.CharField(max_length=30)
    status = models.CharField(max_length=20)
    synced = models.IntegerField()
    processed = models.IntegerField()
    total_requests = models.IntegerField()
    total_ads_found = models.IntegerField()
    video_list_size = models.IntegerField()
    remarks = models.CharField(max_length=255)
    location = models.ForeignKey('ProcessorLocations', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'processor_batch'


class ProcessorBots(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'processor_bots'


class ProcessorCategories(models.Model):
    cat_id = models.IntegerField()
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'processor_categories'


class ProcessorChannels(models.Model):
    channel_id = models.TextField()
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'processor_channels'


class ProcessorLocations(models.Model):
    state_name = models.CharField(max_length=100)
    state_symbol = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'processor_locations'


class ProcessorVideos(models.Model):
    url = models.TextField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    keywords = models.TextField()
    watched_as_ad = models.IntegerField()
    watched_as_video = models.IntegerField()
    category = models.ForeignKey(ProcessorCategories, models.DO_NOTHING)
    channel = models.ForeignKey(ProcessorChannels, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'processor_videos'
