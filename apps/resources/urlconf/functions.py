"""Functions, graphs, inequalities, rearranging, sequences, and substitution."""

from django.urls import path

from apps.resources.views import (
    operation_placeholder_view,
)

urlpatterns = [
    # Функциялар - "IGCSE" flat slot, none with a real page yet.
    path('algebra-functions-igcse/', operation_placeholder_view, {'operation_slug': 'algebra-functions-igcse'}, name='algebra_functions_igcse'),

    # Функциялар > Түзүү - all 7 slots, none with a real page yet.
    path('algebra-functions-forming-expressions/', operation_placeholder_view, {'operation_slug': 'algebra-functions-forming-expressions'}, name='algebra_functions_forming_expressions'),
    path('algebra-functions-forming-simple-functions/', operation_placeholder_view, {'operation_slug': 'algebra-functions-forming-simple-functions'}, name='algebra_functions_forming_simple_functions'),
    path('algebra-functions-forming-changing-subject/', operation_placeholder_view, {'operation_slug': 'algebra-functions-forming-changing-subject'}, name='algebra_functions_forming_changing_subject'),
    path('algebra-functions-forming-composite-linear/', operation_placeholder_view, {'operation_slug': 'algebra-functions-forming-composite-linear'}, name='algebra_functions_forming_composite_linear'),
    path('algebra-functions-forming-inverse/', operation_placeholder_view, {'operation_slug': 'algebra-functions-forming-inverse'}, name='algebra_functions_forming_inverse'),
    path('algebra-functions-forming-composite-inverse/', operation_placeholder_view, {'operation_slug': 'algebra-functions-forming-composite-inverse'}, name='algebra_functions_forming_composite_inverse'),
    path('algebra-functions-forming-composite-quadratics/', operation_placeholder_view, {'operation_slug': 'algebra-functions-forming-composite-quadratics'}, name='algebra_functions_forming_composite_quadratics'),

    # Функциялар > Маанисин эсептөө - all 10 slots, none with a real
    # page yet.
    path('algebra-functions-evaluating-simple-machines/', operation_placeholder_view, {'operation_slug': 'algebra-functions-evaluating-simple-machines'}, name='algebra_functions_evaluating_simple_machines'),
    path('algebra-functions-evaluating-graphing/', operation_placeholder_view, {'operation_slug': 'algebra-functions-evaluating-graphing'}, name='algebra_functions_evaluating_graphing'),
    path('algebra-functions-evaluating-equations-sequences/', operation_placeholder_view, {'operation_slug': 'algebra-functions-evaluating-equations-sequences'}, name='algebra_functions_evaluating_equations_sequences'),
    path('algebra-functions-evaluating-linear/', operation_placeholder_view, {'operation_slug': 'algebra-functions-evaluating-linear'}, name='algebra_functions_evaluating_linear'),
    path('algebra-functions-evaluating-indices/', operation_placeholder_view, {'operation_slug': 'algebra-functions-evaluating-indices'}, name='algebra_functions_evaluating_indices'),
    path('algebra-functions-evaluating-composite/', operation_placeholder_view, {'operation_slug': 'algebra-functions-evaluating-composite'}, name='algebra_functions_evaluating_composite'),
    path('algebra-functions-evaluating-inverse/', operation_placeholder_view, {'operation_slug': 'algebra-functions-evaluating-inverse'}, name='algebra_functions_evaluating_inverse'),
    path('algebra-functions-evaluating-composite-inverse/', operation_placeholder_view, {'operation_slug': 'algebra-functions-evaluating-composite-inverse'}, name='algebra_functions_evaluating_composite_inverse'),
    path('algebra-functions-evaluating-solving-equations/', operation_placeholder_view, {'operation_slug': 'algebra-functions-evaluating-solving-equations'}, name='algebra_functions_evaluating_solving_equations'),
    path('algebra-functions-evaluating-iteration/', operation_placeholder_view, {'operation_slug': 'algebra-functions-evaluating-iteration'}, name='algebra_functions_evaluating_iteration'),

    # Графиктер: абстракттуу - 5 flat slots, none with a real page yet.
    path('algebra-graphs-abstract-coordinates/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-coordinates'}, name='algebra_graphs_abstract_coordinates'),
    path('algebra-graphs-abstract-linear-calculating/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-calculating'}, name='algebra_graphs_abstract_linear_calculating'),
    path('algebra-graphs-abstract-linear-plotting/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-plotting'}, name='algebra_graphs_abstract_linear_plotting'),
    path('algebra-graphs-abstract-linear-reading/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-reading'}, name='algebra_graphs_abstract_linear_reading'),
    path('algebra-graphs-abstract-linear-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-mixed'}, name='algebra_graphs_abstract_linear_mixed'),

    # Графиктер: турмуштук - 4 flat slots, none with a real page yet.
    path('algebra-graphs-real-life-depth-time/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-depth-time'}, name='algebra_graphs_real_life_depth_time'),
    path('algebra-graphs-real-life-volume-time/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-volume-time'}, name='algebra_graphs_real_life_volume_time'),
    path('algebra-graphs-real-life-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-mixed'}, name='algebra_graphs_real_life_mixed'),
    path('algebra-graphs-real-life-mixed-distance-velocity/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-mixed-distance-velocity'}, name='algebra_graphs_real_life_mixed_distance_velocity'),

    # Барабарсыздыктар - 2 flat slots, none with a real page yet.
    path('algebra-inequalities-quadratic/', operation_placeholder_view, {'operation_slug': 'algebra-inequalities-quadratic'}, name='algebra_inequalities_quadratic'),
    path('algebra-inequalities-trial-improvement/', operation_placeholder_view, {'operation_slug': 'algebra-inequalities-trial-improvement'}, name='algebra_inequalities_trial_improvement'),

    # Өзгөртүп түзүү - 2 flat slots, none with a real page yet.
    path('algebra-manipulation-notation/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation'}, name='algebra_manipulation_notation'),
    path('algebra-manipulation-changing-subject/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-changing-subject'}, name='algebra_manipulation_changing_subject'),

    # Ырааттуулуктар - 9 flat slots, none with a real page yet.
    path('algebra-sequences-introduction/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-introduction'}, name='algebra_sequences_introduction'),
    path('algebra-sequences-with-graphs/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-with-graphs'}, name='algebra_sequences_with_graphs'),
    path('algebra-sequences-equations-functions/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-equations-functions'}, name='algebra_sequences_equations_functions'),
    path('algebra-sequences-quadratic/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-quadratic'}, name='algebra_sequences_quadratic'),
    path('algebra-sequences-linear-quadratic/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-linear-quadratic'}, name='algebra_sequences_linear_quadratic'),
    path('algebra-sequences-geometric/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-geometric'}, name='algebra_sequences_geometric'),
    path('algebra-sequences-fibonacci/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-fibonacci'}, name='algebra_sequences_fibonacci'),
    path('algebra-sequences-special/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-special'}, name='algebra_sequences_special'),
    path('algebra-sequences-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-mixed'}, name='algebra_sequences_mixed'),

    # Ордуна коюу (renamed from "Коюу") - 2 flat slots, none with a
    # real page yet.
    path('algebra-substitution-with-calculator/', operation_placeholder_view, {'operation_slug': 'algebra-substitution-with-calculator'}, name='algebra_substitution_with_calculator'),
    path('algebra-substitution-vectors/', operation_placeholder_view, {'operation_slug': 'algebra-substitution-vectors'}, name='algebra_substitution_vectors'),

    # Ордуна коюу > Белгилерди колдонуу / Даражасыз / Даража менен - 6
    # distinct Positive/Negative slots plus 1 shared Mixed slot.
    path('algebra-substitution-symbols-positive/', operation_placeholder_view, {'operation_slug': 'algebra-substitution-symbols-positive'}, name='algebra_substitution_symbols_positive'),
    path('algebra-substitution-symbols-negative/', operation_placeholder_view, {'operation_slug': 'algebra-substitution-symbols-negative'}, name='algebra_substitution_symbols_negative'),
    path('algebra-substitution-without-indices-positive/', operation_placeholder_view, {'operation_slug': 'algebra-substitution-without-indices-positive'}, name='algebra_substitution_without_indices_positive'),
    path('algebra-substitution-without-indices-negative/', operation_placeholder_view, {'operation_slug': 'algebra-substitution-without-indices-negative'}, name='algebra_substitution_without_indices_negative'),
    path('algebra-substitution-with-indices-positive/', operation_placeholder_view, {'operation_slug': 'algebra-substitution-with-indices-positive'}, name='algebra_substitution_with_indices_positive'),
    path('algebra-substitution-with-indices-negative/', operation_placeholder_view, {'operation_slug': 'algebra-substitution-with-indices-negative'}, name='algebra_substitution_with_indices_negative'),
    path('algebra-substitution-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-substitution-mixed'}, name='algebra_substitution_mixed'),

    # Графиктер: абстракттуу > Координаттар - all 6 slots, none with a
    # real page yet.
    path('algebra-graphs-abstract-coordinates-reading/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-coordinates-reading'}, name='algebra_graphs_abstract_coordinates_reading'),
    path('algebra-graphs-abstract-coordinates-reading-plotting/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-coordinates-reading-plotting'}, name='algebra_graphs_abstract_coordinates_reading_plotting'),
    path('algebra-graphs-abstract-coordinates-midpoint-endpoint/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-coordinates-midpoint-endpoint'}, name='algebra_graphs_abstract_coordinates_midpoint_endpoint'),
    path('algebra-graphs-abstract-coordinates-segments-ratio/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-coordinates-segments-ratio'}, name='algebra_graphs_abstract_coordinates_segments_ratio'),
    path('algebra-graphs-abstract-coordinates-geometric-problems/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-coordinates-geometric-problems'}, name='algebra_graphs_abstract_coordinates_geometric_problems'),
    path('algebra-graphs-abstract-coordinates-with-pythagoras/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-coordinates-with-pythagoras'}, name='algebra_graphs_abstract_coordinates_with_pythagoras'),

    # Графиктер: абстракттуу > Сызыктуу: эсептөө - 9 flat slots, none
    # with a real page yet.
    path('algebra-graphs-abstract-linear-calc-functions-graphs/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-calc-functions-graphs'}, name='algebra_graphs_abstract_linear_calc_functions_graphs'),
    path('algebra-graphs-abstract-linear-calc-gradient-intercept/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-calc-gradient-intercept'}, name='algebra_graphs_abstract_linear_calc_gradient_intercept'),
    path('algebra-graphs-abstract-linear-calc-evaluating-coordinates/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-calc-evaluating-coordinates'}, name='algebra_graphs_abstract_linear_calc_evaluating_coordinates'),
    path('algebra-graphs-abstract-linear-calc-evaluating-intersections/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-calc-evaluating-intersections'}, name='algebra_graphs_abstract_linear_calc_evaluating_intersections'),
    path('algebra-graphs-abstract-linear-calc-parallel/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-calc-parallel'}, name='algebra_graphs_abstract_linear_calc_parallel'),
    path('algebra-graphs-abstract-linear-calc-perpendicular/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-calc-perpendicular'}, name='algebra_graphs_abstract_linear_calc_perpendicular'),
    path('algebra-graphs-abstract-linear-calc-parallel-perpendicular/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-calc-parallel-perpendicular'}, name='algebra_graphs_abstract_linear_calc_parallel_perpendicular'),
    path('algebra-graphs-abstract-linear-calc-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-calc-mixed'}, name='algebra_graphs_abstract_linear_calc_mixed'),
    path('algebra-graphs-abstract-linear-calc-identifying-graphs/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-calc-identifying-graphs'}, name='algebra_graphs_abstract_linear_calc_identifying_graphs'),

    # Графиктер: абстракттуу > Сызыктуу: чиймелөө - all 8 slots, none
    # with a real page yet.
    path('algebra-graphs-abstract-linear-plot-with-functions/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-plot-with-functions'}, name='algebra_graphs_abstract_linear_plot_with_functions'),
    path('algebra-graphs-abstract-linear-plot-with-sequences/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-plot-with-sequences'}, name='algebra_graphs_abstract_linear_plot_with_sequences'),
    path('algebra-graphs-abstract-linear-plot-cover-up/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-plot-cover-up'}, name='algebra_graphs_abstract_linear_plot_cover_up'),
    path('algebra-graphs-abstract-linear-plot-gradient/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-plot-gradient'}, name='algebra_graphs_abstract_linear_plot_gradient'),
    path('algebra-graphs-abstract-linear-plot-gradient-intercept-method/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-plot-gradient-intercept-method'}, name='algebra_graphs_abstract_linear_plot_gradient_intercept_method'),
    path('algebra-graphs-abstract-linear-plot-table-of-values/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-plot-table-of-values'}, name='algebra_graphs_abstract_linear_plot_table_of_values'),
    path('algebra-graphs-abstract-linear-plot-inequalities/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-plot-inequalities'}, name='algebra_graphs_abstract_linear_plot_inequalities'),
    path('algebra-graphs-abstract-linear-plot-simultaneous/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-plot-simultaneous'}, name='algebra_graphs_abstract_linear_plot_simultaneous'),

    # Графиктер: абстракттуу > Сызыктуу: окуу - only 4 slots built so
    # far (reference screenshot was cut off, flagged to the user).
    path('algebra-graphs-abstract-linear-read-horizontal-vertical/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-read-horizontal-vertical'}, name='algebra_graphs_abstract_linear_read_horizontal_vertical'),
    path('algebra-graphs-abstract-linear-read-gradient/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-read-gradient'}, name='algebra_graphs_abstract_linear_read_gradient'),
    path('algebra-graphs-abstract-linear-read-equation/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-read-equation'}, name='algebra_graphs_abstract_linear_read_equation'),
    path('algebra-graphs-abstract-linear-read-evaluating-intersections/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-read-evaluating-intersections'}, name='algebra_graphs_abstract_linear_read_evaluating_intersections'),

    # Графиктер: абстракттуу > Квадраттык - all 5 slots, none with a
    # real page yet.
    path('algebra-graphs-abstract-quadratic-plotting/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-quadratic-plotting'}, name='algebra_graphs_abstract_quadratic_plotting'),
    path('algebra-graphs-abstract-quadratic-significant-points/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-quadratic-significant-points'}, name='algebra_graphs_abstract_quadratic_significant_points'),
    path('algebra-graphs-abstract-quadratic-turning-points/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-quadratic-turning-points'}, name='algebra_graphs_abstract_quadratic_turning_points'),
    path('algebra-graphs-abstract-quadratic-solving-by-intersection/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-quadratic-solving-by-intersection'}, name='algebra_graphs_abstract_quadratic_solving_by_intersection'),
    path('algebra-graphs-abstract-quadratic-simultaneous/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-quadratic-simultaneous'}, name='algebra_graphs_abstract_quadratic_simultaneous'),

    # Графиктер: абстракттуу > Тегеректер - both slots, none with a
    # real page yet.
    path('algebra-graphs-abstract-circles-equation/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-circles-equation'}, name='algebra_graphs_abstract_circles_equation'),
    path('algebra-graphs-abstract-circles-tangent/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-circles-tangent'}, name='algebra_graphs_abstract_circles_tangent'),

    # Графиктер: абстракттуу > Башка сызыктуу эмес - all 6 slots, none
    # with a real page yet.
    path('algebra-graphs-abstract-other-nonlinear-plotting/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-other-nonlinear-plotting'}, name='algebra_graphs_abstract_other_nonlinear_plotting'),
    path('algebra-graphs-abstract-other-nonlinear-identifying-nonlinear/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-other-nonlinear-identifying-nonlinear'}, name='algebra_graphs_abstract_other_nonlinear_identifying_nonlinear'),
    path('algebra-graphs-abstract-other-nonlinear-identifying-proportional/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-other-nonlinear-identifying-proportional'}, name='algebra_graphs_abstract_other_nonlinear_identifying_proportional'),
    path('algebra-graphs-abstract-other-nonlinear-estimating-gradient/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-other-nonlinear-estimating-gradient'}, name='algebra_graphs_abstract_other_nonlinear_estimating_gradient'),
    path('algebra-graphs-abstract-other-nonlinear-exponential-functions/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-other-nonlinear-exponential-functions'}, name='algebra_graphs_abstract_other_nonlinear_exponential_functions'),
    path('algebra-graphs-abstract-other-nonlinear-trig-functions/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-other-nonlinear-trig-functions'}, name='algebra_graphs_abstract_other_nonlinear_trig_functions'),

    # Графиктер: абстракттуу > Өзгөртүүлөр - both slots, none with a
    # real page yet.
    path('algebra-graphs-abstract-transformations-gcse/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-transformations-gcse'}, name='algebra_graphs_abstract_transformations_gcse'),
    path('algebra-graphs-abstract-transformations-igcse/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-transformations-igcse'}, name='algebra_graphs_abstract_transformations_igcse'),

    # Графиктер: турмуштук > Айландыруу графиктери - 2 confirmed slots
    # (reference screenshot was cut off after these).
    path('algebra-graphs-real-life-conversion-reading/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-conversion-reading'}, name='algebra_graphs_real_life_conversion_reading'),
    path('algebra-graphs-real-life-conversion-plotting-reading/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-conversion-plotting-reading'}, name='algebra_graphs_real_life_conversion_plotting_reading'),

    # Графиктер: турмуштук > Баа катыштары - 2 confirmed slots (cut off
    # in the reference).
    path('algebra-graphs-real-life-cost-introduction/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-cost-introduction'}, name='algebra_graphs_real_life_cost_introduction'),
    path('algebra-graphs-real-life-cost-with-equations/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-cost-with-equations'}, name='algebra_graphs_real_life_cost_with_equations'),

    # Графиктер: турмуштук > Аралык-Убакыт: турактуу ылдамдык - 2
    # confirmed slots (cut off in the reference).
    path('algebra-graphs-real-life-distance-time-constant-reading/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-distance-time-constant-reading'}, name='algebra_graphs_real_life_distance_time_constant_reading'),
    path('algebra-graphs-real-life-distance-time-constant-plotting-reading/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-distance-time-constant-plotting-reading'}, name='algebra_graphs_real_life_distance_time_constant_plotting_reading'),

    # Графиктер: турмуштук > Ылдамдык-Убакыт - all 3 slots, none with a
    # real page yet.
    path('algebra-graphs-real-life-velocity-time-distance/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-velocity-time-distance'}, name='algebra_graphs_real_life_velocity_time_distance'),
    path('algebra-graphs-real-life-velocity-time-acceleration/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-velocity-time-acceleration'}, name='algebra_graphs_real_life_velocity_time_acceleration'),
    path('algebra-graphs-real-life-velocity-time-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-velocity-time-mixed'}, name='algebra_graphs_real_life_velocity_time_mixed'),

    # Барабарсыздыктар > Сызыктуу - all 6 slots, none with a real page
    # yet.
    path('algebra-inequalities-linear-forming/', operation_placeholder_view, {'operation_slug': 'algebra-inequalities-linear-forming'}, name='algebra_inequalities_linear_forming'),
    path('algebra-inequalities-linear-evaluating/', operation_placeholder_view, {'operation_slug': 'algebra-inequalities-linear-evaluating'}, name='algebra_inequalities_linear_evaluating'),
    path('algebra-inequalities-linear-representing/', operation_placeholder_view, {'operation_slug': 'algebra-inequalities-linear-representing'}, name='algebra_inequalities_linear_representing'),
    path('algebra-inequalities-linear-solving-single/', operation_placeholder_view, {'operation_slug': 'algebra-inequalities-linear-solving-single'}, name='algebra_inequalities_linear_solving_single'),
    path('algebra-inequalities-linear-solving-single-double/', operation_placeholder_view, {'operation_slug': 'algebra-inequalities-linear-solving-single-double'}, name='algebra_inequalities_linear_solving_single_double'),
    path('algebra-inequalities-linear-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-inequalities-linear-mixed'}, name='algebra_inequalities_linear_mixed'),

    # Барабарсыздыктар > Графикалык - 2 confirmed slots (cut off in the
    # reference).
    path('algebra-inequalities-graphical-shade-wanted/', operation_placeholder_view, {'operation_slug': 'algebra-inequalities-graphical-shade-wanted'}, name='algebra_inequalities_graphical_shade_wanted'),
    path('algebra-inequalities-graphical-shade-unwanted/', operation_placeholder_view, {'operation_slug': 'algebra-inequalities-graphical-shade-unwanted'}, name='algebra_inequalities_graphical_shade_unwanted'),

    # Өзгөртүп түзүү > Туюнтма түзүү - all 3 slots, none with a real page
    # yet.
    path('algebra-manipulation-forming-function-machines/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-forming-function-machines'}, name='algebra_manipulation_forming_function_machines'),
    path('algebra-manipulation-forming-linear/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-forming-linear'}, name='algebra_manipulation_forming_linear'),
    path('algebra-manipulation-forming-quadratic/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-forming-quadratic'}, name='algebra_manipulation_forming_quadratic'),

    # Өзгөртүп түзүү > Алгебралык бөлчөктөр - all 6 slots, none with a
    # real page yet.
    path('algebra-manipulation-fractions-adding-subtracting/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-fractions-adding-subtracting'}, name='algebra_manipulation_fractions_adding_subtracting'),
    path('algebra-manipulation-fractions-multiplying-dividing/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-fractions-multiplying-dividing'}, name='algebra_manipulation_fractions_multiplying_dividing'),
    path('algebra-manipulation-fractions-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-fractions-mixed'}, name='algebra_manipulation_fractions_mixed'),
    path('algebra-manipulation-fractions-simplifying/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-fractions-simplifying'}, name='algebra_manipulation_fractions_simplifying'),
    path('algebra-manipulation-fractions-simplifying-with-factorisation/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-fractions-simplifying-with-factorisation'}, name='algebra_manipulation_fractions_simplifying_with_factorisation'),
    path('algebra-manipulation-fractions-simplifying-difference-squares/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-fractions-simplifying-difference-squares'}, name='algebra_manipulation_fractions_simplifying_difference_squares'),

    # Өзгөртүп түзүү > Формуланын өзгөрмөсүн алмаштыруу - all 4 slots,
    # none with a real page yet.
    path('algebra-manipulation-changing-subject-manipulating-formulae/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-changing-subject-manipulating-formulae'}, name='algebra_manipulation_changing_subject_manipulating_formulae'),
    path('algebra-manipulation-changing-subject-function-machine/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-changing-subject-function-machine'}, name='algebra_manipulation_changing_subject_function_machine'),
    path('algebra-manipulation-changing-subject-without-factorisation/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-changing-subject-without-factorisation'}, name='algebra_manipulation_changing_subject_without_factorisation'),
    path('algebra-manipulation-changing-subject-with-factorisation/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-changing-subject-with-factorisation'}, name='algebra_manipulation_changing_subject_with_factorisation'),

    # Өзгөртүп түзүү > Бир кашааны ачуу - all 7 slots, none with a real
    # page yet.
    path('algebra-manipulation-expand-single-without-coefficients/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-single-without-coefficients'}, name='algebra_manipulation_expand_single_without_coefficients'),
    path('algebra-manipulation-expand-single-with-coefficients/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-single-with-coefficients'}, name='algebra_manipulation_expand_single_with_coefficients'),
    path('algebra-manipulation-expand-single-with-indices/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-single-with-indices'}, name='algebra_manipulation_expand_single_with_indices'),
    path('algebra-manipulation-expand-single-multiple/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-single-multiple'}, name='algebra_manipulation_expand_single_multiple'),
    path('algebra-manipulation-expand-single-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-single-mixed'}, name='algebra_manipulation_expand_single_mixed'),
    path('algebra-manipulation-expand-single-factorisation-without-indices/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-single-factorisation-without-indices'}, name='algebra_manipulation_expand_single_factorisation_without_indices'),
    path('algebra-manipulation-expand-single-factorisation-with-indices/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-single-factorisation-with-indices'}, name='algebra_manipulation_expand_single_factorisation_with_indices'),

    # Өзгөртүп түзүү > Эки жана үч кашааны ачуу - all 7 slots, none with a
    # real page yet.
    path('algebra-manipulation-expand-double-triple-double-without-coefficients/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-double-triple-double-without-coefficients'}, name='algebra_manipulation_expand_double_triple_double_without_coefficients'),
    path('algebra-manipulation-expand-double-triple-double-with-coefficients/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-double-triple-double-with-coefficients'}, name='algebra_manipulation_expand_double_triple_double_with_coefficients'),
    path('algebra-manipulation-expand-double-triple-with-factorisation/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-double-triple-with-factorisation'}, name='algebra_manipulation_expand_double_triple_with_factorisation'),
    path('algebra-manipulation-expand-double-triple-squares/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-double-triple-squares'}, name='algebra_manipulation_expand_double_triple_squares'),
    path('algebra-manipulation-expand-double-triple-triple/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-double-triple-triple'}, name='algebra_manipulation_expand_double_triple_triple'),
    path('algebra-manipulation-expand-double-triple-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-double-triple-mixed'}, name='algebra_manipulation_expand_double_triple_mixed'),
    path('algebra-manipulation-expand-double-triple-with-surds/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-double-triple-with-surds'}, name='algebra_manipulation_expand_double_triple_with_surds'),

    # Өзгөртүп түзүү > Бир кашаага ажыратуу - both slots, none with a
    # real page yet.
    path('algebra-manipulation-factorise-single-without-indices/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-factorise-single-without-indices'}, name='algebra_manipulation_factorise_single_without_indices'),
    path('algebra-manipulation-factorise-single-with-indices/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-factorise-single-with-indices'}, name='algebra_manipulation_factorise_single_with_indices'),

    # Өзгөртүп түзүү > Эки кашаага ажыратуу - all 7 slots, none with a
    # real page yet.
    path('algebra-manipulation-factorise-double-quadratic-without-coefficients/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-factorise-double-quadratic-without-coefficients'}, name='algebra_manipulation_factorise_double_quadratic_without_coefficients'),
    path('algebra-manipulation-factorise-double-quadratic-with-coefficients/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-factorise-double-quadratic-with-coefficients'}, name='algebra_manipulation_factorise_double_quadratic_with_coefficients'),
    path('algebra-manipulation-factorise-double-with-expanding/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-factorise-double-with-expanding'}, name='algebra_manipulation_factorise_double_with_expanding'),
    path('algebra-manipulation-factorise-double-completing-square/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-factorise-double-completing-square'}, name='algebra_manipulation_factorise_double_completing_square'),
    path('algebra-manipulation-factorise-double-difference-squares/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-factorise-double-difference-squares'}, name='algebra_manipulation_factorise_double_difference_squares'),
    path('algebra-manipulation-factorise-double-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-factorise-double-mixed'}, name='algebra_manipulation_factorise_double_mixed'),
    path('algebra-manipulation-factorise-double-grouping/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-factorise-double-grouping'}, name='algebra_manipulation_factorise_double_grouping'),

    # Өзгөртүп түзүү > Белгилөө - all 14 slots, none with a real page
    # yet.
    path('algebra-manipulation-notation-adding/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-adding'}, name='algebra_manipulation_notation_adding'),
    path('algebra-manipulation-notation-adding-brackets/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-adding-brackets'}, name='algebra_manipulation_notation_adding_brackets'),
    path('algebra-manipulation-notation-adding-indices/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-adding-indices'}, name='algebra_manipulation_notation_adding_indices'),
    path('algebra-manipulation-notation-multiplying/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-multiplying'}, name='algebra_manipulation_notation_multiplying'),
    path('algebra-manipulation-notation-multiplying-adding/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-multiplying-adding'}, name='algebra_manipulation_notation_multiplying_adding'),
    path('algebra-manipulation-notation-dividing/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-dividing'}, name='algebra_manipulation_notation_dividing'),
    path('algebra-manipulation-notation-multiplying-dividing/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-multiplying-dividing'}, name='algebra_manipulation_notation_multiplying_dividing'),
    path('algebra-manipulation-notation-squared-cubed/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-squared-cubed'}, name='algebra_manipulation_notation_squared_cubed'),
    path('algebra-manipulation-notation-mixed-arithmetic/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-mixed-arithmetic'}, name='algebra_manipulation_notation_mixed_arithmetic'),
    path('algebra-manipulation-notation-negative-fractional-indices/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-negative-fractional-indices'}, name='algebra_manipulation_notation_negative_fractional_indices'),
    path('algebra-manipulation-notation-rational-with-factorisation/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-rational-with-factorisation'}, name='algebra_manipulation_notation_rational_with_factorisation'),
    path('algebra-manipulation-notation-rational-difference-squares/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-rational-difference-squares'}, name='algebra_manipulation_notation_rational_difference_squares'),
    path('algebra-manipulation-notation-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-mixed'}, name='algebra_manipulation_notation_mixed'),
    path('algebra-manipulation-notation-mixed-all/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-mixed-all'}, name='algebra_manipulation_notation_mixed_all'),

    # Өзгөртүп түзүү > Бир кашаага ажыратуу - 2 more slots found on a
    # fuller screenshot.
    path('algebra-manipulation-factorise-single-expanding-without-indices/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-factorise-single-expanding-without-indices'}, name='algebra_manipulation_factorise_single_expanding_without_indices'),
    path('algebra-manipulation-factorise-single-expanding-with-indices/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-factorise-single-expanding-with-indices'}, name='algebra_manipulation_factorise_single_expanding_with_indices'),

    # Өзгөртүп түзүү > Аралаш - both slots, none with a real page yet.
    path('algebra-manipulation-mixed-foundation/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-mixed-foundation'}, name='algebra_manipulation_mixed_foundation'),
    path('algebra-manipulation-mixed-higher/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-mixed-higher'}, name='algebra_manipulation_mixed_higher'),

    # Ырааттуулуктар > Сызыктуу - all 4 slots, none with a real page yet.
    path('algebra-sequences-linear-introduction/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-linear-introduction'}, name='algebra_sequences_linear_introduction'),
    path('algebra-sequences-linear-evaluating-terms/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-linear-evaluating-terms'}, name='algebra_sequences_linear_evaluating_terms'),
    path('algebra-sequences-linear-from-2-terms/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-linear-from-2-terms'}, name='algebra_sequences_linear_from_2_terms'),
    path('algebra-sequences-linear-summing/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-linear-summing'}, name='algebra_sequences_linear_summing'),

    # Өзгөртүп түзүү > Туюнтмаларды жөнөкөйлөтүү - all 13 slots, none
    # with a real page yet.
    path('algebra-manipulation-expressions-adding/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-adding'}, name='algebra_manipulation_expressions_adding'),
    path('algebra-manipulation-expressions-adding-brackets/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-adding-brackets'}, name='algebra_manipulation_expressions_adding_brackets'),
    path('algebra-manipulation-expressions-adding-indices/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-adding-indices'}, name='algebra_manipulation_expressions_adding_indices'),
    path('algebra-manipulation-expressions-multiplying/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-multiplying'}, name='algebra_manipulation_expressions_multiplying'),
    path('algebra-manipulation-expressions-multiplying-adding/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-multiplying-adding'}, name='algebra_manipulation_expressions_multiplying_adding'),
    path('algebra-manipulation-expressions-dividing/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-dividing'}, name='algebra_manipulation_expressions_dividing'),
    path('algebra-manipulation-expressions-multiplying-dividing/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-multiplying-dividing'}, name='algebra_manipulation_expressions_multiplying_dividing'),
    path('algebra-manipulation-expressions-squared-cubed/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-squared-cubed'}, name='algebra_manipulation_expressions_squared_cubed'),
    path('algebra-manipulation-expressions-mixed-arithmetic/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-mixed-arithmetic'}, name='algebra_manipulation_expressions_mixed_arithmetic'),
    path('algebra-manipulation-expressions-negative-fractional-indices/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-negative-fractional-indices'}, name='algebra_manipulation_expressions_negative_fractional_indices'),
    path('algebra-manipulation-expressions-rational-with-factorisation/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-rational-with-factorisation'}, name='algebra_manipulation_expressions_rational_with_factorisation'),
    path('algebra-manipulation-expressions-rational-difference-squares/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-rational-difference-squares'}, name='algebra_manipulation_expressions_rational_difference_squares'),
    path('algebra-manipulation-expressions-mixed-all/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-mixed-all'}, name='algebra_manipulation_expressions_mixed_all'),
]
