from django.test import TestCase
from django.urls import reverse

from apps.resources.filenames import canonical_filename, resource_for_title
from apps.resources.models import Resource, SubSubtopic, Subtopic, Topic


class FilenameAliasTests(TestCase):
    def test_three_spellings_only(self):
        self.assertEqual(
            canonical_filename('4-Amal-BagyttalganSandarMenenLabirinthA4.pdf'),
            '4-Amal-BagyttalganSandarMenenLabirintA4.pdf',
        )
        self.assertEqual(
            canonical_filename('EkiOrunduuKoshuuJoopTorchosu.pptx'),
            'EkiOrunduuKoshuuJooptor.pptx',
        )
        self.assertEqual(
            canonical_filename('Ekvivalenettuuluk_BOP_KatanyTap.pptx'),
            'Ekvivalenttuuluk_BOP_KatanyTap.pptx',
        )
        self.assertEqual(canonical_filename('6-klass-labirint.pdf'), '6-klass-labirint.pdf')

    def test_lookup_uses_the_live_spelling(self):
        live = Resource.objects.create(
            title='Ekvivalenettuuluk_BOP_KatanyTap.pptx',
            file='resources/files/Ekvivalenettuuluk_BOP_KatanyTap.pptx',
            category='worksheet',
            is_active=True,
        )
        resources = {live.title: live}
        found = resource_for_title(resources, 'Ekvivalenttuuluk_BOP_KatanyTap.pptx')
        self.assertEqual(found.id, live.id)
        self.assertEqual(resource_for_title(resources, live.title).id, live.id)


class MissingContinuumPageTests(TestCase):
    def test_two_continuum_paths_open_with_a_grade_badge(self):
        cases = (
            ('proportion', 'percentages-non-calculator', 'mixed', '6–7 кл.'),
            ('algebra', 'manipulation', 'manipulation-proofs', '8–9 кл.'),
        )
        for topic, sub, leaf, badge in cases:
            url = reverse('subsubtopic_detail', args=[topic, sub, leaf])
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200, url)
            self.assertContains(resp, f'topic-page__grade"><span>{badge}</span>')
            self.assertContains(resp, 'даярдалууда')
