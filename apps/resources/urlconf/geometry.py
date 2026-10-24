"""Geometry topics."""

from django.urls import path

from apps.resources.views import (
    operation_placeholder_view,
)

urlpatterns = [
    # Геометрия > Бурчтар > Бурч фактылары - 6 slots, none with a real
    # page yet.
    path('geometry-angles-angle-facts-vocabulary/', operation_placeholder_view, {'operation_slug': 'geometry-angles-angle-facts-vocabulary'}, name='geometry_angles_angle_facts_vocabulary'),
    path('geometry-angles-angle-facts-around-a-point/', operation_placeholder_view, {'operation_slug': 'geometry-angles-angle-facts-around-a-point'}, name='geometry_angles_angle_facts_around_a_point'),
    path('geometry-angles-angle-facts-on-straight-lines/', operation_placeholder_view, {'operation_slug': 'geometry-angles-angle-facts-on-straight-lines'}, name='geometry_angles_angle_facts_on_straight_lines'),
    path('geometry-angles-angle-facts-vertically-opposite/', operation_placeholder_view, {'operation_slug': 'geometry-angles-angle-facts-vertically-opposite'}, name='geometry_angles_angle_facts_vertically_opposite'),
    path('geometry-angles-angle-facts-triangles/', operation_placeholder_view, {'operation_slug': 'geometry-angles-angle-facts-triangles'}, name='geometry_angles_angle_facts_triangles'),
    path('geometry-angles-angle-facts-mixed/', operation_placeholder_view, {'operation_slug': 'geometry-angles-angle-facts-mixed'}, name='geometry_angles_angle_facts_mixed'),

    # Геометрия > Бурчтар > Чийүү жана өлчөө - 4 slots, none with a
    # real page yet.
    path('geometry-angles-drawing-measuring-drawing/', operation_placeholder_view, {'operation_slug': 'geometry-angles-drawing-measuring-drawing'}, name='geometry_angles_drawing_measuring_drawing'),
    path('geometry-angles-drawing-measuring-measuring/', operation_placeholder_view, {'operation_slug': 'geometry-angles-drawing-measuring-measuring'}, name='geometry_angles_drawing_measuring_measuring'),
    path('geometry-angles-drawing-measuring-both/', operation_placeholder_view, {'operation_slug': 'geometry-angles-drawing-measuring-both'}, name='geometry_angles_drawing_measuring_both'),
    path('geometry-angles-drawing-measuring-estimating/', operation_placeholder_view, {'operation_slug': 'geometry-angles-drawing-measuring-estimating'}, name='geometry_angles_drawing_measuring_estimating'),

    # Геометрия > Бурчтар > Тегерек теоремалары - 10 slots, none with a
    # real page yet.
    path('geometry-angles-circle-theorems-vocabulary/', operation_placeholder_view, {'operation_slug': 'geometry-angles-circle-theorems-vocabulary'}, name='geometry_angles_circle_theorems_vocabulary'),
    path('geometry-angles-circle-theorems-alternate-segment/', operation_placeholder_view, {'operation_slug': 'geometry-angles-circle-theorems-alternate-segment'}, name='geometry_angles_circle_theorems_alternate_segment'),
    path('geometry-angles-circle-theorems-at-circumference/', operation_placeholder_view, {'operation_slug': 'geometry-angles-circle-theorems-at-circumference'}, name='geometry_angles_circle_theorems_at_circumference'),
    path('geometry-angles-circle-theorems-cyclic-quadrilaterals/', operation_placeholder_view, {'operation_slug': 'geometry-angles-circle-theorems-cyclic-quadrilaterals'}, name='geometry_angles_circle_theorems_cyclic_quadrilaterals'),
    path('geometry-angles-circle-theorems-tangents-chords/', operation_placeholder_view, {'operation_slug': 'geometry-angles-circle-theorems-tangents-chords'}, name='geometry_angles_circle_theorems_tangents_chords'),
    path('geometry-angles-circle-theorems-combined/', operation_placeholder_view, {'operation_slug': 'geometry-angles-circle-theorems-combined'}, name='geometry_angles_circle_theorems_combined'),
    path('geometry-angles-circle-theorems-mixed/', operation_placeholder_view, {'operation_slug': 'geometry-angles-circle-theorems-mixed'}, name='geometry_angles_circle_theorems_mixed'),
    path('geometry-angles-circle-theorems-with-pythagoras/', operation_placeholder_view, {'operation_slug': 'geometry-angles-circle-theorems-with-pythagoras'}, name='geometry_angles_circle_theorems_with_pythagoras'),
    path('geometry-angles-circle-theorems-with-trigonometry/', operation_placeholder_view, {'operation_slug': 'geometry-angles-circle-theorems-with-trigonometry'}, name='geometry_angles_circle_theorems_with_trigonometry'),
    path('geometry-angles-circle-theorems-intersecting-chords/', operation_placeholder_view, {'operation_slug': 'geometry-angles-circle-theorems-intersecting-chords'}, name='geometry_angles_circle_theorems_intersecting_chords'),

    # Геометрия > Бурчтар > Параллель сызыктар - 2 known slots
    # (screenshot was cut off), none with a real page yet.
    path('geometry-angles-parallel-lines-introduction/', operation_placeholder_view, {'operation_slug': 'geometry-angles-parallel-lines-introduction'}, name='geometry_angles_parallel_lines_introduction'),
    path('geometry-angles-parallel-lines-solving-equations/', operation_placeholder_view, {'operation_slug': 'geometry-angles-parallel-lines-solving-equations'}, name='geometry_angles_parallel_lines_solving_equations'),

    # Геометрия > Бурчтар > Көп бурчтуктар - 5 flat slots plus "Аралаш"
    # category's own 2 slots.
    path('geometry-angles-polygons-triangles/', operation_placeholder_view, {'operation_slug': 'geometry-angles-polygons-triangles'}, name='geometry_angles_polygons_triangles'),
    path('geometry-angles-polygons-quadrilaterals/', operation_placeholder_view, {'operation_slug': 'geometry-angles-polygons-quadrilaterals'}, name='geometry_angles_polygons_quadrilaterals'),
    path('geometry-angles-polygons-special-quadrilaterals/', operation_placeholder_view, {'operation_slug': 'geometry-angles-polygons-special-quadrilaterals'}, name='geometry_angles_polygons_special_quadrilaterals'),
    path('geometry-angles-polygons-regular/', operation_placeholder_view, {'operation_slug': 'geometry-angles-polygons-regular'}, name='geometry_angles_polygons_regular'),
    path('geometry-angles-polygons-irregular/', operation_placeholder_view, {'operation_slug': 'geometry-angles-polygons-irregular'}, name='geometry_angles_polygons_irregular'),
    path('geometry-angles-polygons-mixed-without-circle-theorems/', operation_placeholder_view, {'operation_slug': 'geometry-angles-polygons-mixed-without-circle-theorems'}, name='geometry_angles_polygons_mixed_without_circle_theorems'),
    path('geometry-angles-polygons-mixed-with-circle-theorems/', operation_placeholder_view, {'operation_slug': 'geometry-angles-polygons-mixed-with-circle-theorems'}, name='geometry_angles_polygons_mixed_with_circle_theorems'),

    # Геометрия > Азимут - all 5 slots, none with a real page yet.
    path('geometry-bearings-cardinal-points/', operation_placeholder_view, {'operation_slug': 'geometry-bearings-cardinal-points'}, name='geometry_bearings_cardinal_points'),
    path('geometry-bearings-measuring/', operation_placeholder_view, {'operation_slug': 'geometry-bearings-measuring'}, name='geometry_bearings_measuring'),
    path('geometry-bearings-with-scale-drawings/', operation_placeholder_view, {'operation_slug': 'geometry-bearings-with-scale-drawings'}, name='geometry_bearings_with_scale_drawings'),
    path('geometry-bearings-calculating/', operation_placeholder_view, {'operation_slug': 'geometry-bearings-calculating'}, name='geometry_bearings_calculating'),
    path('geometry-bearings-with-trigonometry/', operation_placeholder_view, {'operation_slug': 'geometry-bearings-with-trigonometry'}, name='geometry_bearings_with_trigonometry'),

    # Геометрия > Координаттар - all 6 slots, none with a real page yet.
    path('geometry-coordinates-reading/', operation_placeholder_view, {'operation_slug': 'geometry-coordinates-reading'}, name='geometry_coordinates_reading'),
    path('geometry-coordinates-reading-plotting/', operation_placeholder_view, {'operation_slug': 'geometry-coordinates-reading-plotting'}, name='geometry_coordinates_reading_plotting'),
    path('geometry-coordinates-midpoint-endpoint/', operation_placeholder_view, {'operation_slug': 'geometry-coordinates-midpoint-endpoint'}, name='geometry_coordinates_midpoint_endpoint'),
    path('geometry-coordinates-line-segments-ratio/', operation_placeholder_view, {'operation_slug': 'geometry-coordinates-line-segments-ratio'}, name='geometry_coordinates_line_segments_ratio'),
    path('geometry-coordinates-geometric-problems/', operation_placeholder_view, {'operation_slug': 'geometry-coordinates-geometric-problems'}, name='geometry_coordinates_geometric_problems'),
    path('geometry-coordinates-with-pythagoras/', operation_placeholder_view, {'operation_slug': 'geometry-coordinates-with-pythagoras'}, name='geometry_coordinates_with_pythagoras'),

    # Геометрия > Пифагор - 11 flat slots, none with a real page yet.
    path('geometry-pythagoras-introduction/', operation_placeholder_view, {'operation_slug': 'geometry-pythagoras-introduction'}, name='geometry_pythagoras_introduction'),
    path('geometry-pythagoras-finding-a-or-b/', operation_placeholder_view, {'operation_slug': 'geometry-pythagoras-finding-a-or-b'}, name='geometry_pythagoras_finding_a_or_b'),
    path('geometry-pythagoras-finding-a-b-or-c/', operation_placeholder_view, {'operation_slug': 'geometry-pythagoras-finding-a-b-or-c'}, name='geometry_pythagoras_finding_a_b_or_c'),
    path('geometry-pythagoras-isosceles-triangles/', operation_placeholder_view, {'operation_slug': 'geometry-pythagoras-isosceles-triangles'}, name='geometry_pythagoras_isosceles_triangles'),
    path('geometry-pythagoras-real-life/', operation_placeholder_view, {'operation_slug': 'geometry-pythagoras-real-life'}, name='geometry_pythagoras_real_life'),
    path('geometry-pythagoras-3d/', operation_placeholder_view, {'operation_slug': 'geometry-pythagoras-3d'}, name='geometry_pythagoras_3d'),
    path('geometry-pythagoras-coordinates/', operation_placeholder_view, {'operation_slug': 'geometry-pythagoras-coordinates'}, name='geometry_pythagoras_coordinates'),
    path('geometry-pythagoras-mixed/', operation_placeholder_view, {'operation_slug': 'geometry-pythagoras-mixed'}, name='geometry_pythagoras_mixed'),
    path('geometry-pythagoras-shape-perimeters/', operation_placeholder_view, {'operation_slug': 'geometry-pythagoras-shape-perimeters'}, name='geometry_pythagoras_shape_perimeters'),
    path('geometry-pythagoras-with-surds/', operation_placeholder_view, {'operation_slug': 'geometry-pythagoras-with-surds'}, name='geometry_pythagoras_with_surds'),
    path('geometry-pythagoras-with-circle-theorems/', operation_placeholder_view, {'operation_slug': 'geometry-pythagoras-with-circle-theorems'}, name='geometry_pythagoras_with_circle_theorems'),

    # Геометрия > Пифагор > Тригонометрия менен - 2 flat slots, none
    # with a real page yet.
    path('geometry-pythagoras-with-trigonometry-or/', operation_placeholder_view, {'operation_slug': 'geometry-pythagoras-with-trigonometry-or'}, name='geometry_pythagoras_with_trigonometry_or'),
    path('geometry-pythagoras-with-trigonometry-and/', operation_placeholder_view, {'operation_slug': 'geometry-pythagoras-with-trigonometry-and'}, name='geometry_pythagoras_with_trigonometry_and'),

    # Геометрия > Окшоштук - "Окшош 2D фигуралар" and "Тең үч
    # бурчтуктар" are flat; "Окшош үч бурчтуктар" and "Узундук, аянт
    # жана көлөм масштаб көбөйткүчтөрү" turned out to be categories
    # (see rebuild_decimals_1_digit.py) - their own leaf slots are
    # below. geometry_similarity_similar_triangles and
    # geometry_similarity_length_area_volume_scale_factors above are
    # now orphaned (no menu item points to them any more, same as
    # every other displaced_url_names case in this file).
    path('geometry-similarity-similar-2d-shapes/', operation_placeholder_view, {'operation_slug': 'geometry-similarity-similar-2d-shapes'}, name='geometry_similarity_similar_2d_shapes'),
    path('geometry-similarity-similar-triangles/', operation_placeholder_view, {'operation_slug': 'geometry-similarity-similar-triangles'}, name='geometry_similarity_similar_triangles'),
    path('geometry-similarity-congruent-triangles/', operation_placeholder_view, {'operation_slug': 'geometry-similarity-congruent-triangles'}, name='geometry_similarity_congruent_triangles'),
    path('geometry-similarity-length-area-volume-scale-factors/', operation_placeholder_view, {'operation_slug': 'geometry-similarity-length-area-volume-scale-factors'}, name='geometry_similarity_length_area_volume_scale_factors'),

    # Геометрия > Окшоштук > Окшош үч бурчтуктар - 2 flat slots, none
    # with a real page yet.
    path('geometry-similarity-similar-triangles-abstract/', operation_placeholder_view, {'operation_slug': 'geometry-similarity-similar-triangles-abstract'}, name='geometry_similarity_similar_triangles_abstract'),
    path('geometry-similarity-similar-triangles-real-life/', operation_placeholder_view, {'operation_slug': 'geometry-similarity-similar-triangles-real-life'}, name='geometry_similarity_similar_triangles_real_life'),

    # Геометрия > Окшоштук > Узундук, аянт жана көлөм масштаб
    # көбөйткүчтөрү - 3 flat slots, none with a real page yet.
    path('geometry-similarity-length-area-volume-scale-factors-length-area/', operation_placeholder_view, {'operation_slug': 'geometry-similarity-length-area-volume-scale-factors-length-area'}, name='geometry_similarity_length_area_volume_scale_factors_length_area'),
    path('geometry-similarity-length-area-volume-scale-factors-length-volume/', operation_placeholder_view, {'operation_slug': 'geometry-similarity-length-area-volume-scale-factors-length-volume'}, name='geometry_similarity_length_area_volume_scale_factors_length_volume'),
    path('geometry-similarity-length-area-volume-scale-factors-length-area-volume/', operation_placeholder_view, {'operation_slug': 'geometry-similarity-length-area-volume-scale-factors-length-area-volume'}, name='geometry_similarity_length_area_volume_scale_factors_length_area_volume'),

    # Геометрия > Өзгөртүүлөр > Чоңойтуу - 7 flat slots, none with a
    # real page yet.
    path('geometry-transformations-enlargement-positive/', operation_placeholder_view, {'operation_slug': 'geometry-transformations-enlargement-positive'}, name='geometry_transformations_enlargement_positive'),
    path('geometry-transformations-enlargement-negative/', operation_placeholder_view, {'operation_slug': 'geometry-transformations-enlargement-negative'}, name='geometry_transformations_enlargement_negative'),
    path('geometry-transformations-enlargement-fractional/', operation_placeholder_view, {'operation_slug': 'geometry-transformations-enlargement-fractional'}, name='geometry_transformations_enlargement_fractional'),
    path('geometry-transformations-enlargement-negative-fractional/', operation_placeholder_view, {'operation_slug': 'geometry-transformations-enlargement-negative-fractional'}, name='geometry_transformations_enlargement_negative_fractional'),
    path('geometry-transformations-enlargement-ray-method/', operation_placeholder_view, {'operation_slug': 'geometry-transformations-enlargement-ray-method'}, name='geometry_transformations_enlargement_ray_method'),
    path('geometry-transformations-enlargement-mixed-foundation/', operation_placeholder_view, {'operation_slug': 'geometry-transformations-enlargement-mixed-foundation'}, name='geometry_transformations_enlargement_mixed_foundation'),
    path('geometry-transformations-enlargement-mixed-higher/', operation_placeholder_view, {'operation_slug': 'geometry-transformations-enlargement-mixed-higher'}, name='geometry_transformations_enlargement_mixed_higher'),

    # Геометрия > Өзгөртүүлөр > Аралаш - 2 flat slots, none with a real
    # page yet.
    path('geometry-transformations-mixed-foundation/', operation_placeholder_view, {'operation_slug': 'geometry-transformations-mixed-foundation'}, name='geometry_transformations_mixed_foundation'),
    path('geometry-transformations-mixed-higher/', operation_placeholder_view, {'operation_slug': 'geometry-transformations-mixed-higher'}, name='geometry_transformations_mixed_higher'),

    # Геометрия > Тригонометрия - 7 flat slots, none with a real page
    # yet.
    path('geometry-trigonometry-introduction/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-introduction'}, name='geometry_trigonometry_introduction'),
    path('geometry-trigonometry-graphs/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-graphs'}, name='geometry_trigonometry_graphs'),
    path('geometry-trigonometry-choosing-a-ratio/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-choosing-a-ratio'}, name='geometry_trigonometry_choosing_a_ratio'),
    path('geometry-trigonometry-isosceles-triangles/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-isosceles-triangles'}, name='geometry_trigonometry_isosceles_triangles'),
    path('geometry-trigonometry-without-calculator/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-without-calculator'}, name='geometry_trigonometry_without_calculator'),
    path('geometry-trigonometry-with-circle-theorems/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-with-circle-theorems'}, name='geometry_trigonometry_with_circle_theorems'),
    path('geometry-trigonometry-area-rule/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-area-rule'}, name='geometry_trigonometry_area_rule'),

    # Геометрия > Тригонометрия > Синус жана косинус катыштары - 2 flat
    # slots, none with a real page yet.
    path('geometry-trigonometry-sine-cosine-ratios-lengths/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-sine-cosine-ratios-lengths'}, name='geometry_trigonometry_sine_cosine_ratios_lengths'),
    path('geometry-trigonometry-sine-cosine-ratios-angles/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-sine-cosine-ratios-angles'}, name='geometry_trigonometry_sine_cosine_ratios_angles'),

    # Геометрия > Тригонометрия > Тангенс катышы - 2 flat slots, none
    # with a real page yet.
    path('geometry-trigonometry-tangent-ratio-lengths/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-tangent-ratio-lengths'}, name='geometry_trigonometry_tangent_ratio_lengths'),
    path('geometry-trigonometry-tangent-ratio-angles/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-tangent-ratio-angles'}, name='geometry_trigonometry_tangent_ratio_angles'),

    # Геометрия > Тригонометрия > Бардык катыштар - 2 flat slots, none
    # with a real page yet.
    path('geometry-trigonometry-all-ratios-lengths/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-all-ratios-lengths'}, name='geometry_trigonometry_all_ratios_lengths'),
    path('geometry-trigonometry-all-ratios-angles/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-all-ratios-angles'}, name='geometry_trigonometry_all_ratios_angles'),

    # Геометрия > Тригонометрия > Бардык катыштар > Аралаш - 2 flat
    # slots, none with a real page yet.
    path('geometry-trigonometry-all-ratios-mixed-or/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-all-ratios-mixed-or'}, name='geometry_trigonometry_all_ratios_mixed_or'),
    path('geometry-trigonometry-all-ratios-mixed-and/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-all-ratios-mixed-and'}, name='geometry_trigonometry_all_ratios_mixed_and'),

    # Геометрия > Тригонометрия > Турмуштук маселелер - 4 flat slots,
    # none with a real page yet.
    path('geometry-trigonometry-real-life-elevation-depression/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-real-life-elevation-depression'}, name='geometry_trigonometry_real_life_elevation_depression'),
    path('geometry-trigonometry-real-life-practical-problems/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-real-life-practical-problems'}, name='geometry_trigonometry_real_life_practical_problems'),
    path('geometry-trigonometry-real-life-3d/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-real-life-3d'}, name='geometry_trigonometry_real_life_3d'),
    path('geometry-trigonometry-real-life-with-bearings/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-real-life-with-bearings'}, name='geometry_trigonometry_real_life_with_bearings'),

    # Геометрия > Тригонометрия > Синус жана косинус эрежелери - 5 flat
    # slots, none with a real page yet.
    path('geometry-trigonometry-sine-cosine-rules-sine-rule/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-sine-cosine-rules-sine-rule'}, name='geometry_trigonometry_sine_cosine_rules_sine_rule'),
    path('geometry-trigonometry-sine-cosine-rules-cosine-rule-lengths/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-sine-cosine-rules-cosine-rule-lengths'}, name='geometry_trigonometry_sine_cosine_rules_cosine_rule_lengths'),
    path('geometry-trigonometry-sine-cosine-rules-cosine-rule-angles/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-sine-cosine-rules-cosine-rule-angles'}, name='geometry_trigonometry_sine_cosine_rules_cosine_rule_angles'),
    path('geometry-trigonometry-sine-cosine-rules-cosine-rule-mixed/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-sine-cosine-rules-cosine-rule-mixed'}, name='geometry_trigonometry_sine_cosine_rules_cosine_rule_mixed'),
    path('geometry-trigonometry-sine-cosine-rules-solving-any-triangle/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-sine-cosine-rules-solving-any-triangle'}, name='geometry_trigonometry_sine_cosine_rules_solving_any_triangle'),

    # Геометрия > Векторлор - all 5 slots, none with a real page yet.
    path('geometry-vectors-translation/', operation_placeholder_view, {'operation_slug': 'geometry-vectors-translation'}, name='geometry_vectors_translation'),
    path('geometry-vectors-expressing/', operation_placeholder_view, {'operation_slug': 'geometry-vectors-expressing'}, name='geometry_vectors_expressing'),
    path('geometry-vectors-substitution/', operation_placeholder_view, {'operation_slug': 'geometry-vectors-substitution'}, name='geometry_vectors_substitution'),
    path('geometry-vectors-around-shapes/', operation_placeholder_view, {'operation_slug': 'geometry-vectors-around-shapes'}, name='geometry_vectors_around_shapes'),
    path('geometry-vectors-proofs/', operation_placeholder_view, {'operation_slug': 'geometry-vectors-proofs'}, name='geometry_vectors_proofs'),

    # Геометрия > Көлөм жана бет аянты - 3 flat slots, none with a
    # real page yet.
    path('geometry-volume-surface-area-vocabulary/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-vocabulary'}, name='geometry_volume_surface_area_vocabulary'),
    path('geometry-volume-surface-area-introduction-to-volume/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-introduction-to-volume'}, name='geometry_volume_surface_area_introduction_to_volume'),
    path('geometry-volume-surface-area-nets/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-nets'}, name='geometry_volume_surface_area_nets'),

    # Геометрия > Көлөм жана бет аянты > Конус - 2 flat slots,
    # none with a real page yet.
    path('geometry-volume-surface-area-cone-volume/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-cone-volume'}, name='geometry_volume_surface_area_cone_volume'),
    path('geometry-volume-surface-area-cone-surface-area/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-cone-surface-area'}, name='geometry_volume_surface_area_cone_surface_area'),

    # Геометрия > Көлөм жана бет аянты > Конус > Аралаш - 2 flat
    # slots, none with a real page yet.
    path('geometry-volume-surface-area-cone-mixed-foundation/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-cone-mixed-foundation'}, name='geometry_volume_surface_area_cone_mixed_foundation'),
    path('geometry-volume-surface-area-cone-mixed-higher/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-cone-mixed-higher'}, name='geometry_volume_surface_area_cone_mixed_higher'),

    # Геометрия > Көлөм жана бет аянты > Параллелепипед - 2 flat slots,
    # none with a real page yet.
    path('geometry-volume-surface-area-cuboid-volume/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-cuboid-volume'}, name='geometry_volume_surface_area_cuboid_volume'),
    path('geometry-volume-surface-area-cuboid-surface-area/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-cuboid-surface-area'}, name='geometry_volume_surface_area_cuboid_surface_area'),

    # Геометрия > Көлөм жана бет аянты > Параллелепипед > Аралаш - 2 flat
    # slots, none with a real page yet.
    path('geometry-volume-surface-area-cuboid-mixed-foundation/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-cuboid-mixed-foundation'}, name='geometry_volume_surface_area_cuboid_mixed_foundation'),
    path('geometry-volume-surface-area-cuboid-mixed-higher/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-cuboid-mixed-higher'}, name='geometry_volume_surface_area_cuboid_mixed_higher'),

    # Геометрия > Көлөм жана бет аянты > Цилиндр - 2 flat slots,
    # none with a real page yet.
    path('geometry-volume-surface-area-cylinder-volume/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-cylinder-volume'}, name='geometry_volume_surface_area_cylinder_volume'),
    path('geometry-volume-surface-area-cylinder-surface-area/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-cylinder-surface-area'}, name='geometry_volume_surface_area_cylinder_surface_area'),

    # Геометрия > Көлөм жана бет аянты > Цилиндр > Аралаш - 2 flat
    # slots, none with a real page yet.
    path('geometry-volume-surface-area-cylinder-mixed-foundation/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-cylinder-mixed-foundation'}, name='geometry_volume_surface_area_cylinder_mixed_foundation'),
    path('geometry-volume-surface-area-cylinder-mixed-higher/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-cylinder-mixed-higher'}, name='geometry_volume_surface_area_cylinder_mixed_higher'),

    # Геометрия > Көлөм жана бет аянты > Призма - 2 flat slots,
    # none with a real page yet.
    path('geometry-volume-surface-area-prism-volume/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-prism-volume'}, name='geometry_volume_surface_area_prism_volume'),
    path('geometry-volume-surface-area-prism-surface-area/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-prism-surface-area'}, name='geometry_volume_surface_area_prism_surface_area'),

    # Геометрия > Көлөм жана бет аянты > Призма > Аралаш - 2 flat
    # slots, none with a real page yet.
    path('geometry-volume-surface-area-prism-mixed-foundation/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-prism-mixed-foundation'}, name='geometry_volume_surface_area_prism_mixed_foundation'),
    path('geometry-volume-surface-area-prism-mixed-higher/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-prism-mixed-higher'}, name='geometry_volume_surface_area_prism_mixed_higher'),

    # Геометрия > Көлөм жана бет аянты > Кесилген конус - 2 flat slots,
    # none with a real page yet.
    path('geometry-volume-surface-area-frustum-volume/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-frustum-volume'}, name='geometry_volume_surface_area_frustum_volume'),
    path('geometry-volume-surface-area-frustum-surface-area/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-frustum-surface-area'}, name='geometry_volume_surface_area_frustum_surface_area'),

    # Геометрия > Көлөм жана бет аянты > Кесилген конус > Аралаш - 2 flat
    # slots, none with a real page yet.
    path('geometry-volume-surface-area-frustum-mixed-foundation/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-frustum-mixed-foundation'}, name='geometry_volume_surface_area_frustum_mixed_foundation'),
    path('geometry-volume-surface-area-frustum-mixed-higher/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-frustum-mixed-higher'}, name='geometry_volume_surface_area_frustum_mixed_higher'),

    # Геометрия > Көлөм жана бет аянты > Пирамида - 2 flat slots,
    # none with a real page yet.
    path('geometry-volume-surface-area-pyramid-volume/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-pyramid-volume'}, name='geometry_volume_surface_area_pyramid_volume'),
    path('geometry-volume-surface-area-pyramid-surface-area/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-pyramid-surface-area'}, name='geometry_volume_surface_area_pyramid_surface_area'),

    # Геометрия > Көлөм жана бет аянты > Пирамида > Аралаш - 2 flat
    # slots, none with a real page yet.
    path('geometry-volume-surface-area-pyramid-mixed-foundation/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-pyramid-mixed-foundation'}, name='geometry_volume_surface_area_pyramid_mixed_foundation'),
    path('geometry-volume-surface-area-pyramid-mixed-higher/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-pyramid-mixed-higher'}, name='geometry_volume_surface_area_pyramid_mixed_higher'),

    # Геометрия > Көлөм жана бет аянты > Сфера - 2 flat slots,
    # none with a real page yet.
    path('geometry-volume-surface-area-sphere-volume/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-sphere-volume'}, name='geometry_volume_surface_area_sphere_volume'),
    path('geometry-volume-surface-area-sphere-surface-area/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-sphere-surface-area'}, name='geometry_volume_surface_area_sphere_surface_area'),

    # Геометрия > Көлөм жана бет аянты > Сфера > Аралаш - 2 flat
    # slots, none with a real page yet.
    path('geometry-volume-surface-area-sphere-mixed-foundation/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-sphere-mixed-foundation'}, name='geometry_volume_surface_area_sphere_mixed_foundation'),
    path('geometry-volume-surface-area-sphere-mixed-higher/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-sphere-mixed-higher'}, name='geometry_volume_surface_area_sphere_mixed_higher'),

    # Геометрия > Көлөм жана бет аянты > Цилиндр жана призма - 2 flat
    # slots, none with a real page yet.
    path('geometry-volume-surface-area-cylinder-prism-volume/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-cylinder-prism-volume'}, name='geometry_volume_surface_area_cylinder_prism_volume'),
    path('geometry-volume-surface-area-cylinder-prism-surface-area/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-cylinder-prism-surface-area'}, name='geometry_volume_surface_area_cylinder_prism_surface_area'),

    # Геометрия > Көлөм жана бет аянты > Цилиндр жана призма > Аралаш -
    # 2 flat slots, none with a real page yet.
    path('geometry-volume-surface-area-cylinder-prism-mixed-foundation/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-cylinder-prism-mixed-foundation'}, name='geometry_volume_surface_area_cylinder_prism_mixed_foundation'),
    path('geometry-volume-surface-area-cylinder-prism-mixed-higher/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-cylinder-prism-mixed-higher'}, name='geometry_volume_surface_area_cylinder_prism_mixed_higher'),

    # Геометрия > Көлөм жана бет аянты > Аралаш (top-level sibling to
    # Конус/Параллелепипед/etc) - 2 flat slots, none with a real page
    # yet.
    path('geometry-volume-surface-area-mixed-foundation/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-mixed-foundation'}, name='geometry_volume_surface_area_mixed_foundation'),
    path('geometry-volume-surface-area-mixed-higher/', operation_placeholder_view, {'operation_slug': 'geometry-volume-surface-area-mixed-higher'}, name='geometry_volume_surface_area_mixed_higher'),

    # Геометрия > Бурчтар > Аралаш - all 2 slots.
    path('geometry-angles-mixed-without-circle-theorems/', operation_placeholder_view, {'operation_slug': 'geometry-angles-mixed-without-circle-theorems'}, name='geometry_angles_mixed_without_circle_theorems'),
    path('geometry-angles-mixed-with-circle-theorems/', operation_placeholder_view, {'operation_slug': 'geometry-angles-mixed-with-circle-theorems'}, name='geometry_angles_mixed_with_circle_theorems'),

    # Геометрия > Аянт жана периметр > Тегеректер - all 10 slots.
    path('geometry-area-perimeter-circles-vocabulary/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-circles-vocabulary'}, name='geometry_area_perimeter_circles_vocabulary'),
    path('geometry-area-perimeter-circles-area/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-circles-area'}, name='geometry_area_perimeter_circles_area'),
    path('geometry-area-perimeter-circles-area-in-terms-of-pi/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-circles-area-in-terms-of-pi'}, name='geometry_area_perimeter_circles_area_in_terms_of_pi'),
    path('geometry-area-perimeter-circles-circumference/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-circles-circumference'}, name='geometry_area_perimeter_circles_circumference'),
    path('geometry-area-perimeter-circles-area-circumference/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-circles-area-circumference'}, name='geometry_area_perimeter_circles_area_circumference'),
    path('geometry-area-perimeter-circles-arc-length/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-circles-arc-length'}, name='geometry_area_perimeter_circles_arc_length'),
    path('geometry-area-perimeter-circles-sector-area/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-circles-sector-area'}, name='geometry_area_perimeter_circles_sector_area'),
    path('geometry-area-perimeter-circles-arcs-sectors/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-circles-arcs-sectors'}, name='geometry_area_perimeter_circles_arcs_sectors'),
    path('geometry-area-perimeter-circles-mixed/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-circles-mixed'}, name='geometry_area_perimeter_circles_mixed'),
    path('geometry-area-perimeter-circles-comparative-pie-charts/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-circles-comparative-pie-charts'}, name='geometry_area_perimeter_circles_comparative_pie_charts'),

    # Геометрия > Аянт жана периметр > Татаал: түз сызыктуу - all 3
    # slots.
    path('geometry-area-perimeter-compound-rectilinear-area/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-compound-rectilinear-area'}, name='geometry_area_perimeter_compound_rectilinear_area'),
    path('geometry-area-perimeter-compound-rectilinear-perimeter/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-compound-rectilinear-perimeter'}, name='geometry_area_perimeter_compound_rectilinear_perimeter'),
    path('geometry-area-perimeter-compound-rectilinear-mixed/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-compound-rectilinear-mixed'}, name='geometry_area_perimeter_compound_rectilinear_mixed'),

    # Геометрия > Аянт жана периметр > Татаал: көп бурчтуктуу - all 3
    # slots.
    path('geometry-area-perimeter-compound-polygonal-area/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-compound-polygonal-area'}, name='geometry_area_perimeter_compound_polygonal_area'),
    path('geometry-area-perimeter-compound-polygonal-perimeter/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-compound-polygonal-perimeter'}, name='geometry_area_perimeter_compound_polygonal_perimeter'),
    path('geometry-area-perimeter-compound-polygonal-perimeter-with-pythagoras/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-compound-polygonal-perimeter-with-pythagoras'}, name='geometry_area_perimeter_compound_polygonal_perimeter_with_pythagoras'),

    # Геометрия > Аянт жана периметр > Татаал: тегеректер менен - all
    # 3 slots.
    path('geometry-area-perimeter-compound-with-circles-area/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-compound-with-circles-area'}, name='geometry_area_perimeter_compound_with_circles_area'),
    path('geometry-area-perimeter-compound-with-circles-perimeter/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-compound-with-circles-perimeter'}, name='geometry_area_perimeter_compound_with_circles_perimeter'),
    path('geometry-area-perimeter-compound-with-circles-mixed/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-compound-with-circles-mixed'}, name='geometry_area_perimeter_compound_with_circles_mixed'),

    # Геометрия > Аянт жана периметр > Төрт бурчтуктар - 6 slots.
    path('geometry-area-perimeter-quadrilaterals-vocabulary/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-quadrilaterals-vocabulary'}, name='geometry_area_perimeter_quadrilaterals_vocabulary'),
    path('geometry-area-perimeter-quadrilaterals-rectangle-area/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-quadrilaterals-rectangle-area'}, name='geometry_area_perimeter_quadrilaterals_rectangle_area'),
    path('geometry-area-perimeter-quadrilaterals-rectangle-perimeter/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-quadrilaterals-rectangle-perimeter'}, name='geometry_area_perimeter_quadrilaterals_rectangle_perimeter'),
    path('geometry-area-perimeter-quadrilaterals-rectangle-area-perimeter/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-quadrilaterals-rectangle-area-perimeter'}, name='geometry_area_perimeter_quadrilaterals_rectangle_area_perimeter'),
    path('geometry-area-perimeter-quadrilaterals-parallelogram/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-quadrilaterals-parallelogram'}, name='geometry_area_perimeter_quadrilaterals_parallelogram'),
    path('geometry-area-perimeter-quadrilaterals-trapezium/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-quadrilaterals-trapezium'}, name='geometry_area_perimeter_quadrilaterals_trapezium'),

    # Геометрия > Аянт жана периметр > Үч бурчтуктар - 2 known slots.
    path('geometry-area-perimeter-triangles-area/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-triangles-area'}, name='geometry_area_perimeter_triangles_area'),
    path('geometry-area-perimeter-triangles-area-using-sine-rule/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-triangles-area-using-sine-rule'}, name='geometry_area_perimeter_triangles_area_using_sine_rule'),

    # Геометрия > Аянт жана периметр > Аралаш - all 4 slots.
    path('geometry-area-perimeter-mixed-polygons/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-mixed-polygons'}, name='geometry_area_perimeter_mixed_polygons'),
    path('geometry-area-perimeter-mixed-polygons-with-pythagoras/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-mixed-polygons-with-pythagoras'}, name='geometry_area_perimeter_mixed_polygons_with_pythagoras'),
    path('geometry-area-perimeter-mixed-polygons-circles/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-mixed-polygons-circles'}, name='geometry_area_perimeter_mixed_polygons_circles'),
    path('geometry-area-perimeter-mixed-polygons-circles-with-pythagoras/', operation_placeholder_view, {'operation_slug': 'geometry-area-perimeter-mixed-polygons-circles-with-pythagoras'}, name='geometry_area_perimeter_mixed_polygons_circles_with_pythagoras'),

    # Геометрия > Классификациялоо жана терминология > Фигураларды
    # классификациялоо - 4 known slots.
    path('geometry-classifying-vocabulary-classifying-shapes-diagonals/', operation_placeholder_view, {'operation_slug': 'geometry-classifying-vocabulary-classifying-shapes-diagonals'}, name='geometry_classifying_vocabulary_classifying_shapes_diagonals'),
    path('geometry-classifying-vocabulary-classifying-shapes-symmetry/', operation_placeholder_view, {'operation_slug': 'geometry-classifying-vocabulary-classifying-shapes-symmetry'}, name='geometry_classifying_vocabulary_classifying_shapes_symmetry'),
    path('geometry-classifying-vocabulary-classifying-shapes-quadrilaterals/', operation_placeholder_view, {'operation_slug': 'geometry-classifying-vocabulary-classifying-shapes-quadrilaterals'}, name='geometry_classifying_vocabulary_classifying_shapes_quadrilaterals'),
    path('geometry-classifying-vocabulary-classifying-shapes-2d-shapes/', operation_placeholder_view, {'operation_slug': 'geometry-classifying-vocabulary-classifying-shapes-2d-shapes'}, name='geometry_classifying_vocabulary_classifying_shapes_2d_shapes'),

    # Геометрия > Классификациялоо жана терминология > Терминология -
    # all 5 slots.
    path('geometry-classifying-vocabulary-vocabulary-angles/', operation_placeholder_view, {'operation_slug': 'geometry-classifying-vocabulary-vocabulary-angles'}, name='geometry_classifying_vocabulary_vocabulary_angles'),
    path('geometry-classifying-vocabulary-vocabulary-circles/', operation_placeholder_view, {'operation_slug': 'geometry-classifying-vocabulary-vocabulary-circles'}, name='geometry_classifying_vocabulary_vocabulary_circles'),
    path('geometry-classifying-vocabulary-vocabulary-2d-shapes/', operation_placeholder_view, {'operation_slug': 'geometry-classifying-vocabulary-vocabulary-2d-shapes'}, name='geometry_classifying_vocabulary_vocabulary_2d_shapes'),
    path('geometry-classifying-vocabulary-vocabulary-3d-shapes/', operation_placeholder_view, {'operation_slug': 'geometry-classifying-vocabulary-vocabulary-3d-shapes'}, name='geometry_classifying_vocabulary_vocabulary_3d_shapes'),
    path('geometry-classifying-vocabulary-vocabulary-sketching-diagrams/', operation_placeholder_view, {'operation_slug': 'geometry-classifying-vocabulary-vocabulary-sketching-diagrams'}, name='geometry_classifying_vocabulary_vocabulary_sketching_diagrams'),

    # Геометрия > Курулуштар > Бурчтар - all 4 slots.
    path('geometry-construction-angles-drawing/', operation_placeholder_view, {'operation_slug': 'geometry-construction-angles-drawing'}, name='geometry_construction_angles_drawing'),
    path('geometry-construction-angles-measuring/', operation_placeholder_view, {'operation_slug': 'geometry-construction-angles-measuring'}, name='geometry_construction_angles_measuring'),
    path('geometry-construction-angles-both/', operation_placeholder_view, {'operation_slug': 'geometry-construction-angles-both'}, name='geometry_construction_angles_both'),
    path('geometry-construction-angles-estimating/', operation_placeholder_view, {'operation_slug': 'geometry-construction-angles-estimating'}, name='geometry_construction_angles_estimating'),

    # Геометрия > Курулуштар > Көп бурчтуктар - 2 known slots.
    path('geometry-construction-polygons-triangles/', operation_placeholder_view, {'operation_slug': 'geometry-construction-polygons-triangles'}, name='geometry_construction_polygons_triangles'),
    path('geometry-construction-polygons-quadrilaterals/', operation_placeholder_view, {'operation_slug': 'geometry-construction-polygons-quadrilaterals'}, name='geometry_construction_polygons_quadrilaterals'),

    # Геометрия > Курулуштар > Бисектрисалар - all 3 slots.
    path('geometry-construction-bisectors-line/', operation_placeholder_view, {'operation_slug': 'geometry-construction-bisectors-line'}, name='geometry_construction_bisectors_line'),
    path('geometry-construction-bisectors-angle/', operation_placeholder_view, {'operation_slug': 'geometry-construction-bisectors-angle'}, name='geometry_construction_bisectors_angle'),
    path('geometry-construction-bisectors-mixed/', operation_placeholder_view, {'operation_slug': 'geometry-construction-bisectors-mixed'}, name='geometry_construction_bisectors_mixed'),
]
