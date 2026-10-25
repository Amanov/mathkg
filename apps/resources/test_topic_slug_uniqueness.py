import importlib

from django.apps import apps
from django.db import IntegrityError, connection, transaction
from django.test import TestCase, TransactionTestCase

_slug_migration = importlib.import_module(
    'apps.resources.migrations.0043_unique_topic_slugs'
)
merge_duplicate_slugs = _slug_migration.merge_duplicate_slugs
from apps.resources.models import MenuItem, Resource, SubSubtopic, Subtopic, Topic
from apps.resources.taxonomy_slugs import get_or_create_subsubtopic
from apps.resources.views.topics import get_scoped_or_404


class MixedTopicPageTests(TestCase):
    def setUp(self):
        geometry = Topic.objects.create(title='Геометрия', slug='geometry')
        trigonometry = Subtopic.objects.create(
            topic=geometry, title='Тригонометрия', slug='trigonometry',
        )
        SubSubtopic.objects.create(subtopic=trigonometry, title='Аралаш', slug='mixed')

        statistics = Topic.objects.create(title='Дата', slug='statistics')
        for slug, title in (('analysing', 'Талдоо'), ('representing', 'Көрсөтүү')):
            subtopic = Subtopic.objects.create(topic=statistics, title=title, slug=slug)
            SubSubtopic.objects.create(subtopic=subtopic, title='Аралаш', slug='mixed')

    def test_three_mixed_urls_return_200(self):
        pages = (
            ('/resources/topic/geometry/trigonometry/mixed/', 'Тригонометрия'),
            ('/resources/topic/statistics/analysing/mixed/', 'Маалымат'),
            ('/resources/topic/statistics/representing/mixed/', 'Маалымат'),
        )
        for path, needle in pages:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, path)
            self.assertContains(response, needle)

    def test_bad_slug_is_404(self):
        paths = (
            '/resources/topic/geometry/trigonometry/no-such-page/',
            '/resources/topic/geometry/no-such-subtopic/mixed/',
            '/resources/topic/no-such-topic/trigonometry/mixed/',
        )
        for path in paths:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 404, path)


class ScopedSlugCreationTests(TestCase):
    def test_second_mixed_leaf_reuses_the_row(self):
        topic = Topic.objects.create(title='Геометрия', slug='geometry-create')
        subtopic = Subtopic.objects.create(
            topic=topic, title='Тригонометрия', slug='trigonometry-create',
        )
        first, created_first = get_or_create_subsubtopic(subtopic, 'mixed', 'Аралаш')
        second, created_second = get_or_create_subsubtopic(subtopic, 'mixed', 'Аралаш')
        self.assertTrue(created_first)
        self.assertFalse(created_second)
        self.assertEqual(first.pk, second.pk)
        self.assertEqual(
            SubSubtopic.objects.filter(subtopic=subtopic, slug='mixed').count(), 1,
        )

    def test_duplicate_insert_is_rejected(self):
        topic = Topic.objects.create(title='Дата', slug='statistics-create')
        subtopic = Subtopic.objects.create(
            topic=topic, title='Талдоо', slug='analysing-create',
        )
        SubSubtopic.objects.create(subtopic=subtopic, title='Аралаш', slug='mixed')
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                SubSubtopic.objects.create(
                    subtopic=subtopic, title='Башка аралаш', slug='mixed',
                )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Subtopic.objects.create(
                    topic=topic, title='Талдоо 2', slug='analysing-create',
                )


class MergeDuplicateSlugTests(TransactionTestCase):
    # Schema edits cannot run inside TestCase's transaction on SQLite.
    # Reload the migrated rows afterwards so later tests still see them.
    serialized_rollback = True
    def _drop_unique(self, model, name):
        # SQLite rebuilds the table from Meta, so the constraint has to
        # leave the model before remove_constraint, or the index stays.
        constraint = next(item for item in model._meta.constraints if item.name == name)
        model._meta.constraints = [
            item for item in model._meta.constraints if item.name != name
        ]
        with connection.schema_editor() as editor:
            editor.remove_constraint(model, constraint)
        return constraint

    def _restore_unique(self, model, constraint):
        if constraint not in model._meta.constraints:
            model._meta.constraints.append(constraint)
        with connection.schema_editor() as editor:
            editor.add_constraint(model, constraint)

    def test_merge_repoints_links_and_the_page_does_not_500(self):
        subtopic_constraint = self._drop_unique(
            Subtopic, 'personal_subtopic_topic_slug_uniq',
        )
        subsubtopic_constraint = self._drop_unique(
            SubSubtopic, 'personal_subsubtopic_subtopic_slug_uniq',
        )
        try:
            topic = Topic.objects.create(title='Дата', slug='statistics-merge')
            older = Subtopic.objects.create(topic=topic, title='Талдоо', slug='analysing')
            newer = Subtopic.objects.create(
                topic=topic, title='Талдоо көчүрмө', slug='analysing',
            )
            older_page = SubSubtopic.objects.create(
                subtopic=older, title='Аралаш', slug='mixed',
            )
            newer_page = SubSubtopic.objects.create(
                subtopic=newer, title='Аралаш көчүрмө', slug='mixed',
            )
            resource = Resource.objects.create(
                title='merge-keep-me.pdf',
                file='resources/files/merge-keep-me.pdf',
                category='worksheet',
                topic=topic,
                subtopic=newer,
                subsubtopic=newer_page,
            )
            menu = MenuItem.objects.create(
                title='Аралаш', topic=topic, subtopic=newer, subsubtopic=newer_page,
            )

            kept = get_scoped_or_404(Subtopic, topic=topic, slug='analysing')
            self.assertEqual(kept.pk, older.pk)
            response = self.client.get(
                '/resources/topic/statistics-merge/analysing/mixed/',
            )
            self.assertEqual(response.status_code, 200)

            merge_duplicate_slugs(apps, None)

            self.assertEqual(
                Subtopic.objects.filter(topic=topic, slug='analysing').count(), 1,
            )
            self.assertFalse(Subtopic.objects.filter(pk=newer.pk).exists())
            self.assertFalse(SubSubtopic.objects.filter(pk=newer_page.pk).exists())
            self.assertEqual(
                SubSubtopic.objects.filter(subtopic=older, slug='mixed').get().pk,
                older_page.pk,
            )
            resource.refresh_from_db()
            menu.refresh_from_db()
            self.assertTrue(Resource.objects.filter(pk=resource.pk, title='merge-keep-me.pdf').exists())
            self.assertEqual(resource.subtopic_id, older.pk)
            self.assertEqual(resource.subsubtopic_id, older_page.pk)
            self.assertEqual(menu.subtopic_id, older.pk)
            self.assertEqual(menu.subsubtopic_id, older_page.pk)

            merge_duplicate_slugs(apps, None)
            self.assertEqual(
                Subtopic.objects.filter(topic=topic, slug='analysing').count(), 1,
            )
            again = self.client.get('/resources/topic/statistics-merge/analysing/mixed/')
            self.assertEqual(again.status_code, 200)
            self.assertContains(again, 'merge-keep-me.pdf')
        finally:
            self._restore_unique(SubSubtopic, subsubtopic_constraint)
            self._restore_unique(Subtopic, subtopic_constraint)


class UniqueSlugMigrationShapeTests(TestCase):
    def test_dedupe_is_its_own_migration(self):
        migration = _slug_migration.Migration
        self.assertTrue(migration.atomic)
        self.assertEqual(
            [op.__class__.__name__ for op in migration.operations],
            ['RunPython'],
        )
        self.assertIs(migration.operations[0].code, merge_duplicate_slugs)

        subtopic = importlib.import_module(
            'apps.resources.migrations.0045_subtopic_topic_slug_uniq'
        )
        subsubtopic = importlib.import_module(
            'apps.resources.migrations.0046_subsubtopic_subtopic_slug_uniq'
        )
        self.assertEqual(
            subtopic.Migration.dependencies,
            [('personal', '0044_wave6_packs')],
        )
        self.assertEqual(
            subsubtopic.Migration.dependencies,
            [('personal', '0045_subtopic_topic_slug_uniq')],
        )
        self.assertEqual(
            subtopic.Migration.operations[0].state_operations[0].constraint.name,
            'personal_subtopic_topic_slug_uniq',
        )
        self.assertEqual(
            subsubtopic.Migration.operations[0].state_operations[0].constraint.name,
            'personal_subsubtopic_subtopic_slug_uniq',
        )
