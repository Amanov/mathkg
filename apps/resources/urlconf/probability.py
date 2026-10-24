"""Probability topics."""

from django.urls import path

from apps.resources.views import (
    operation_placeholder_view,
)

urlpatterns = [
    # Ыктымалдуулук > Бир окуя - 7 flat slots, none with a real page
    # yet.
    path('probability-single-event-probability-scale/', operation_placeholder_view, {'operation_slug': 'probability-single-event-probability-scale'}, name='probability_single_event_probability_scale'),
    path('probability-single-event-calculating/', operation_placeholder_view, {'operation_slug': 'probability-single-event-calculating'}, name='probability_single_event_calculating'),
    path('probability-single-event-will-not-happen/', operation_placeholder_view, {'operation_slug': 'probability-single-event-will-not-happen'}, name='probability_single_event_will_not_happen'),
    path('probability-single-event-addition-law-or/', operation_placeholder_view, {'operation_slug': 'probability-single-event-addition-law-or'}, name='probability_single_event_addition_law_or'),
    path('probability-single-event-exhaustive-events/', operation_placeholder_view, {'operation_slug': 'probability-single-event-exhaustive-events'}, name='probability_single_event_exhaustive_events'),
    path('probability-single-event-expectation/', operation_placeholder_view, {'operation_slug': 'probability-single-event-expectation'}, name='probability_single_event_expectation'),
    path('probability-single-event-experimental/', operation_placeholder_view, {'operation_slug': 'probability-single-event-experimental'}, name='probability_single_event_experimental'),

    # Ыктымалдуулук > Бир нече окуя - 8 flat slots, none with a real
    # page yet.
    path('probability-multiple-event-systematic-listing/', operation_placeholder_view, {'operation_slug': 'probability-multiple-event-systematic-listing'}, name='probability_multiple_event_systematic_listing'),
    path('probability-multiple-event-product-rule-for-counting/', operation_placeholder_view, {'operation_slug': 'probability-multiple-event-product-rule-for-counting'}, name='probability_multiple_event_product_rule_for_counting'),
    path('probability-multiple-event-or/', operation_placeholder_view, {'operation_slug': 'probability-multiple-event-or'}, name='probability_multiple_event_or'),
    path('probability-multiple-event-and/', operation_placeholder_view, {'operation_slug': 'probability-multiple-event-and'}, name='probability_multiple_event_and'),
    path('probability-multiple-event-and-or-with-listing/', operation_placeholder_view, {'operation_slug': 'probability-multiple-event-and-or-with-listing'}, name='probability_multiple_event_and_or_with_listing'),
    path('probability-multiple-event-sample-space-diagrams/', operation_placeholder_view, {'operation_slug': 'probability-multiple-event-sample-space-diagrams'}, name='probability_multiple_event_sample_space_diagrams'),
    path('probability-multiple-event-mixed-with-single-event/', operation_placeholder_view, {'operation_slug': 'probability-multiple-event-mixed-with-single-event'}, name='probability_multiple_event_mixed_with_single_event'),
    path('probability-multiple-event-general-addition-law/', operation_placeholder_view, {'operation_slug': 'probability-multiple-event-general-addition-law'}, name='probability_multiple_event_general_addition_law'),

    # Ыктымалдуулук > Ыктымалдуулук дарак диаграммалары - 3 flat slots,
    # none with a real page yet.
    path('probability-probability-tree-diagrams-unconditional/', operation_placeholder_view, {'operation_slug': 'probability-probability-tree-diagrams-unconditional'}, name='probability_probability_tree_diagrams_unconditional'),
    path('probability-probability-tree-diagrams-conditional/', operation_placeholder_view, {'operation_slug': 'probability-probability-tree-diagrams-conditional'}, name='probability_probability_tree_diagrams_conditional'),
    path('probability-probability-tree-diagrams-with-frequency-trees/', operation_placeholder_view, {'operation_slug': 'probability-probability-tree-diagrams-with-frequency-trees'}, name='probability_probability_tree_diagrams_with_frequency_trees'),

    # Ыктымалдуулук > Аралаш (top-level sibling to Бир окуя/Бир нече
    # окуя/etc) - 2 flat slots, none with a real page yet.
    path('probability-mixed-foundation/', operation_placeholder_view, {'operation_slug': 'probability-mixed-foundation'}, name='probability_mixed_foundation'),
    path('probability-mixed-higher/', operation_placeholder_view, {'operation_slug': 'probability-mixed-higher'}, name='probability_mixed_higher'),
]
