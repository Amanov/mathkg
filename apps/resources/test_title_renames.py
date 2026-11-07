"""Stored titles change. The address of the page does not."""
import importlib

from django.apps import apps
from django.test import TestCase

from apps.resources.models import MenuItem, Subtopic, Topic

_migration = importlib.import_module('apps.resources.migrations.0066_kyrgyz_topic_titles')
forward = _migration.forward
backward = _migration.backward


class TitleRenameTests(TestCase):
    def test_rename_keeps_slug_and_url_name(self):
        topic = Topic.objects.create(title='Сандар', slug='sandar-rename')
        sub = Subtopic.objects.create(
            topic=topic,
            title='Текст маселелер: тилке модели менен',
            slug='tekst-masele',
        )
        menu = MenuItem.objects.create(
            title='IGCSE',
            url_name='algebra_functions_igcse',
            slug='functions-igcse-menu',
        )
        other = MenuItem.objects.create(
            title='IGCSE',
            url_name='algebra_graphs_abstract_transformations_igcse',
            slug='graphs-igcse-menu',
        )

        forward(apps, None)

        sub.refresh_from_db()
        menu.refresh_from_db()
        other.refresh_from_db()
        self.assertEqual(sub.title, 'Тексттик маселелер: тилке модели менен')
        self.assertEqual(sub.slug, 'tekst-masele')
        self.assertEqual(sub.title_ru, 'Текстовые задачи с ленточной моделью')
        self.assertEqual(menu.title, 'Аралаш функциялар')
        self.assertEqual(menu.url_name, 'algebra_functions_igcse')
        self.assertEqual(menu.slug, 'functions-igcse-menu')
        self.assertEqual(other.title, 'Графикти чоюу')
        self.assertEqual(other.slug, 'graphs-igcse-menu')

        backward(apps, None)
        sub.refresh_from_db()
        menu.refresh_from_db()
        self.assertEqual(sub.title, 'Текст маселелер: тилке модели менен')
        self.assertEqual(sub.slug, 'tekst-masele')
        self.assertEqual(menu.title, 'IGCSE')
        self.assertEqual(menu.url_name, 'algebra_functions_igcse')
