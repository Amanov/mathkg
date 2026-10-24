"""Data topics."""

from django.urls import path

from apps.resources.views import (
    operation_placeholder_view,
)

urlpatterns = [
    # Дата > Талдоо - 4 flat slots, none with a real page yet.
    path('data-analysing-median/', operation_placeholder_view, {'operation_slug': 'data-analysing-median'}, name='data_analysing_median'),
    path('data-analysing-from-a-bar-chart/', operation_placeholder_view, {'operation_slug': 'data-analysing-from-a-bar-chart'}, name='data_analysing_from_a_bar_chart'),
    path('data-analysing-choosing-an-average/', operation_placeholder_view, {'operation_slug': 'data-analysing-choosing-an-average'}, name='data_analysing_choosing_an_average'),
    path('data-analysing-comparing-using-mmmr/', operation_placeholder_view, {'operation_slug': 'data-analysing-comparing-using-mmmr'}, name='data_analysing_comparing_using_mmmr'),

    # Дата > Талдоо > Орточо - 3 flat slots, none with a real page yet.
    path('data-analysing-mean-from-a-list/', operation_placeholder_view, {'operation_slug': 'data-analysing-mean-from-a-list'}, name='data_analysing_mean_from_a_list'),
    path('data-analysing-mean-reverse/', operation_placeholder_view, {'operation_slug': 'data-analysing-mean-reverse'}, name='data_analysing_mean_reverse'),
    path('data-analysing-mean-adjusting/', operation_placeholder_view, {'operation_slug': 'data-analysing-mean-adjusting'}, name='data_analysing_mean_adjusting'),

    # Дата > Талдоо > Мода жана диапазон - 2 flat slots, none with a
    # real page yet.
    path('data-analysing-mode-range-mode/', operation_placeholder_view, {'operation_slug': 'data-analysing-mode-range-mode'}, name='data_analysing_mode_range_mode'),
    path('data-analysing-mode-range-range/', operation_placeholder_view, {'operation_slug': 'data-analysing-mode-range-range'}, name='data_analysing_mode_range_range'),

    # Дата > Талдоо > Кварталдар - 3 flat slots, none with a real page
    # yet.
    path('data-analysing-quartiles-introduction/', operation_placeholder_view, {'operation_slug': 'data-analysing-quartiles-introduction'}, name='data_analysing_quartiles_introduction'),
    path('data-analysing-quartiles-with-box-plots/', operation_placeholder_view, {'operation_slug': 'data-analysing-quartiles-with-box-plots'}, name='data_analysing_quartiles_with_box_plots'),
    path('data-analysing-quartiles-box-plots/', operation_placeholder_view, {'operation_slug': 'data-analysing-quartiles-box-plots'}, name='data_analysing_quartiles_box_plots'),

    # Дата > Чогултуу - 6 flat slots, none with a real page yet.
    path('data-collecting-introduction/', operation_placeholder_view, {'operation_slug': 'data-collecting-introduction'}, name='data_collecting_introduction'),
    path('data-collecting-vocabulary/', operation_placeholder_view, {'operation_slug': 'data-collecting-vocabulary'}, name='data_collecting_vocabulary'),
    path('data-collecting-types-of-data/', operation_placeholder_view, {'operation_slug': 'data-collecting-types-of-data'}, name='data_collecting_types_of_data'),
    path('data-collecting-questionnaires/', operation_placeholder_view, {'operation_slug': 'data-collecting-questionnaires'}, name='data_collecting_questionnaires'),
    path('data-collecting-stratified-sampling/', operation_placeholder_view, {'operation_slug': 'data-collecting-stratified-sampling'}, name='data_collecting_stratified_sampling'),
    path('data-collecting-capture-recapture/', operation_placeholder_view, {'operation_slug': 'data-collecting-capture-recapture'}, name='data_collecting_capture_recapture'),

    # Дата > Жыштык таблицалары > Топтоштурулбаган берилиштер -
    # "Топтоштурулган берилиштер" turned out to be a category, its own
    # url_name entry below is now orphaned (see rebuild_decimals_1_digit.py).
    path('data-frequency-tables-grouped-data/', operation_placeholder_view, {'operation_slug': 'data-frequency-tables-grouped-data'}, name='data_frequency_tables_grouped_data'),
    path('data-frequency-tables-ungrouped-data-creating-reading/', operation_placeholder_view, {'operation_slug': 'data-frequency-tables-ungrouped-data-creating-reading'}, name='data_frequency_tables_ungrouped_data_creating_reading'),
    path('data-frequency-tables-ungrouped-data-calculating-averages/', operation_placeholder_view, {'operation_slug': 'data-frequency-tables-ungrouped-data-calculating-averages'}, name='data_frequency_tables_ungrouped_data_calculating_averages'),

    # Дата > Жыштык таблицалары > Топтоштурулган берилиштер - 2 flat
    # slots, none with a real page yet.
    path('data-frequency-tables-grouped-data-creating-reading/', operation_placeholder_view, {'operation_slug': 'data-frequency-tables-grouped-data-creating-reading'}, name='data_frequency_tables_grouped_data_creating_reading'),
    path('data-frequency-tables-grouped-data-calculating-averages/', operation_placeholder_view, {'operation_slug': 'data-frequency-tables-grouped-data-calculating-averages'}, name='data_frequency_tables_grouped_data_calculating_averages'),

    # Дата > Жыштык таблицалары > Эки багыттуу таблицалар - 3 flat
    # slots, none with a real page yet.
    path('data-frequency-tables-two-way-tables-creating-reading/', operation_placeholder_view, {'operation_slug': 'data-frequency-tables-two-way-tables-creating-reading'}, name='data_frequency_tables_two_way_tables_creating_reading'),
    path('data-frequency-tables-two-way-tables-with-probability/', operation_placeholder_view, {'operation_slug': 'data-frequency-tables-two-way-tables-with-probability'}, name='data_frequency_tables_two_way_tables_with_probability'),
    path('data-frequency-tables-two-way-tables-with-bar-charts/', operation_placeholder_view, {'operation_slug': 'data-frequency-tables-two-way-tables-with-bar-charts'}, name='data_frequency_tables_two_way_tables_with_bar_charts'),

    # Дата > Көрсөтүү - 6 flat slots, none with a real page yet.
    path('data-representing-frequency-polygons/', operation_placeholder_view, {'operation_slug': 'data-representing-frequency-polygons'}, name='data_representing_frequency_polygons'),
    path('data-representing-histograms/', operation_placeholder_view, {'operation_slug': 'data-representing-histograms'}, name='data_representing_histograms'),
    path('data-representing-line-graphs-time-series/', operation_placeholder_view, {'operation_slug': 'data-representing-line-graphs-time-series'}, name='data_representing_line_graphs_time_series'),
    path('data-representing-pictograms/', operation_placeholder_view, {'operation_slug': 'data-representing-pictograms'}, name='data_representing_pictograms'),
    path('data-representing-scatter-graphs/', operation_placeholder_view, {'operation_slug': 'data-representing-scatter-graphs'}, name='data_representing_scatter_graphs'),
    path('data-representing-stem-leaf-diagrams/', operation_placeholder_view, {'operation_slug': 'data-representing-stem-leaf-diagrams'}, name='data_representing_stem_leaf_diagrams'),

    # Дата > Көрсөтүү > Тилке диаграммалары - 6 flat slots, none with a
    # real page yet.
    path('data-representing-bar-charts-single/', operation_placeholder_view, {'operation_slug': 'data-representing-bar-charts-single'}, name='data_representing_bar_charts_single'),
    path('data-representing-bar-charts-dual/', operation_placeholder_view, {'operation_slug': 'data-representing-bar-charts-dual'}, name='data_representing_bar_charts_dual'),
    path('data-representing-bar-charts-composite/', operation_placeholder_view, {'operation_slug': 'data-representing-bar-charts-composite'}, name='data_representing_bar_charts_composite'),
    path('data-representing-bar-charts-vertical-line-charts/', operation_placeholder_view, {'operation_slug': 'data-representing-bar-charts-vertical-line-charts'}, name='data_representing_bar_charts_vertical_line_charts'),
    path('data-representing-bar-charts-calculating-averages/', operation_placeholder_view, {'operation_slug': 'data-representing-bar-charts-calculating-averages'}, name='data_representing_bar_charts_calculating_averages'),
    path('data-representing-bar-charts-with-two-way-tables/', operation_placeholder_view, {'operation_slug': 'data-representing-bar-charts-with-two-way-tables'}, name='data_representing_bar_charts_with_two_way_tables'),

    # Дата > Көрсөтүү > Куту диаграммалары - 3 flat slots, none with a
    # real page yet.
    path('data-representing-box-plots-with-quartiles/', operation_placeholder_view, {'operation_slug': 'data-representing-box-plots-with-quartiles'}, name='data_representing_box_plots_with_quartiles'),
    path('data-representing-box-plots-creating-reading/', operation_placeholder_view, {'operation_slug': 'data-representing-box-plots-creating-reading'}, name='data_representing_box_plots_creating_reading'),
    path('data-representing-box-plots-with-graphs/', operation_placeholder_view, {'operation_slug': 'data-representing-box-plots-with-graphs'}, name='data_representing_box_plots_with_graphs'),

    # Дата > Көрсөтүү > Топтолгон жыштык графиктери - 2 flat slots, none
    # with a real page yet.
    path('data-representing-cumulative-frequency-graphs-introduction/', operation_placeholder_view, {'operation_slug': 'data-representing-cumulative-frequency-graphs-introduction'}, name='data_representing_cumulative_frequency_graphs_introduction'),
    path('data-representing-cumulative-frequency-graphs-with-box-plots/', operation_placeholder_view, {'operation_slug': 'data-representing-cumulative-frequency-graphs-with-box-plots'}, name='data_representing_cumulative_frequency_graphs_with_box_plots'),

    # Дата > Көрсөтүү > Жыштык дарактары - 3 flat slots, none with a
    # real page yet.
    path('data-representing-frequency-trees-introduction/', operation_placeholder_view, {'operation_slug': 'data-representing-frequency-trees-introduction'}, name='data_representing_frequency_trees_introduction'),
    path('data-representing-frequency-trees-with-fpr/', operation_placeholder_view, {'operation_slug': 'data-representing-frequency-trees-with-fpr'}, name='data_representing_frequency_trees_with_fpr'),
    path('data-representing-frequency-trees-with-probability-trees/', operation_placeholder_view, {'operation_slug': 'data-representing-frequency-trees-with-probability-trees'}, name='data_representing_frequency_trees_with_probability_trees'),

    # Дата > Көрсөтүү > Тегерек диаграммалар - 3 flat slots, none with a
    # real page yet.
    path('data-representing-pie-charts-reading/', operation_placeholder_view, {'operation_slug': 'data-representing-pie-charts-reading'}, name='data_representing_pie_charts_reading'),
    path('data-representing-pie-charts-scaling-method/', operation_placeholder_view, {'operation_slug': 'data-representing-pie-charts-scaling-method'}, name='data_representing_pie_charts_scaling_method'),
    path('data-representing-pie-charts-proportional-method/', operation_placeholder_view, {'operation_slug': 'data-representing-pie-charts-proportional-method'}, name='data_representing_pie_charts_proportional_method'),

    # Дата > Көрсөтүү > Аралаш (top-level sibling to Тилке диаграммалары/
    # Куту диаграммалары/etc) - 2 flat slots, none with a real page yet.
    path('data-representing-mixed-foundation/', operation_placeholder_view, {'operation_slug': 'data-representing-mixed-foundation'}, name='data_representing_mixed_foundation'),
    path('data-representing-mixed-higher/', operation_placeholder_view, {'operation_slug': 'data-representing-mixed-higher'}, name='data_representing_mixed_higher'),

    # Дата > Көрсөтүү > Венн диаграммалары - 5 flat slots, none with a
    # real page yet.
    path('data-representing-venn-diagrams-creating-reading/', operation_placeholder_view, {'operation_slug': 'data-representing-venn-diagrams-creating-reading'}, name='data_representing_venn_diagrams_creating_reading'),
    path('data-representing-venn-diagrams-with-probability/', operation_placeholder_view, {'operation_slug': 'data-representing-venn-diagrams-with-probability'}, name='data_representing_venn_diagrams_with_probability'),
    path('data-representing-venn-diagrams-sets-with-notation/', operation_placeholder_view, {'operation_slug': 'data-representing-venn-diagrams-sets-with-notation'}, name='data_representing_venn_diagrams_sets_with_notation'),
    path('data-representing-venn-diagrams-sets-with-notation-igcse/', operation_placeholder_view, {'operation_slug': 'data-representing-venn-diagrams-sets-with-notation-igcse'}, name='data_representing_venn_diagrams_sets_with_notation_igcse'),
    path('data-representing-venn-diagrams-notation-probability/', operation_placeholder_view, {'operation_slug': 'data-representing-venn-diagrams-notation-probability'}, name='data_representing_venn_diagrams_notation_probability'),
]
