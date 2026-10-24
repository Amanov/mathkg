"""Algebra topics, including the one-step equations lesson."""

from django.urls import path

from apps.resources.views import (
    operation_placeholder_view,
    algebra_linear_var1side_noncalc_1step_view,
)

urlpatterns = [
    # Алгебра > Киришүү - all 3 flat slots, none with a real page yet.
    path('algebra-intro-definitions/', operation_placeholder_view, {'operation_slug': 'algebra-intro-definitions'}, name='algebra_intro_definitions'),
    path('algebra-intro-notation/', operation_placeholder_view, {'operation_slug': 'algebra-intro-notation'}, name='algebra_intro_notation'),
    path('algebra-intro-manipulating-formulae/', operation_placeholder_view, {'operation_slug': 'algebra-intro-manipulating-formulae'}, name='algebra_intro_manipulating_formulae'),

    # Алгебра > Киришүү > Туюнтмаларды түзүү - all 3 slots, none with a
    # real page yet.
    path('algebra-forming-expr-function-machines/', operation_placeholder_view, {'operation_slug': 'algebra-forming-expr-function-machines'}, name='algebra_forming_expr_function_machines'),
    path('algebra-forming-expr-linear/', operation_placeholder_view, {'operation_slug': 'algebra-forming-expr-linear'}, name='algebra_forming_expr_linear'),
    path('algebra-forming-expr-quadratic/', operation_placeholder_view, {'operation_slug': 'algebra-forming-expr-quadratic'}, name='algebra_forming_expr_quadratic'),

    # Алгебра > Теңдемелер: сызыктуу - all 8 flat slots, none with a
    # real page yet.
    path('algebra-linear-forming/', operation_placeholder_view, {'operation_slug': 'algebra-linear-forming'}, name='algebra_linear_forming'),
    path('algebra-linear-variable-one-side-calculator/', operation_placeholder_view, {'operation_slug': 'algebra-linear-variable-one-side-calculator'}, name='algebra_linear_variable_one_side_calculator'),
    path('algebra-linear-variable-one-side-non-calculator/', operation_placeholder_view, {'operation_slug': 'algebra-linear-variable-one-side-non-calculator'}, name='algebra_linear_variable_one_side_non_calculator'),
    path('algebra-linear-variable-both-sides/', operation_placeholder_view, {'operation_slug': 'algebra-linear-variable-both-sides'}, name='algebra_linear_variable_both_sides'),
    path('algebra-linear-rational/', operation_placeholder_view, {'operation_slug': 'algebra-linear-rational'}, name='algebra_linear_rational'),
    path('algebra-linear-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-linear-mixed'}, name='algebra_linear_mixed'),
    path('algebra-linear-inequalities/', operation_placeholder_view, {'operation_slug': 'algebra-linear-inequalities'}, name='algebra_linear_inequalities'),
    path('algebra-linear-unknown-indices/', operation_placeholder_view, {'operation_slug': 'algebra-linear-unknown-indices'}, name='algebra_linear_unknown_indices'),

    # Алгебра > Теңдемелер: квадраттык - all 13 slots, none with a real
    # page yet.
    path('algebra-quadratic-forming/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-forming'}, name='algebra_quadratic_forming'),
    path('algebra-quadratic-factorisation-double-brackets/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-factorisation-double-brackets'}, name='algebra_quadratic_factorisation_double_brackets'),
    path('algebra-quadratic-b-zero/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-b-zero'}, name='algebra_quadratic_b_zero'),
    path('algebra-quadratic-c-zero/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-c-zero'}, name='algebra_quadratic_c_zero'),
    path('algebra-quadratic-completing-square/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-completing-square'}, name='algebra_quadratic_completing_square'),
    path('algebra-quadratic-rational/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-rational'}, name='algebra_quadratic_rational'),
    path('algebra-quadratic-formula/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-formula'}, name='algebra_quadratic_formula'),
    path('algebra-quadratic-no-solution/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-no-solution'}, name='algebra_quadratic_no_solution'),
    path('algebra-quadratic-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-mixed'}, name='algebra_quadratic_mixed'),
    path('algebra-quadratic-trial-improvement/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-trial-improvement'}, name='algebra_quadratic_trial_improvement'),
    path('algebra-quadratic-iteration/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-iteration'}, name='algebra_quadratic_iteration'),
    path('algebra-quadratic-by-intersection/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-by-intersection'}, name='algebra_quadratic_by_intersection'),
    path('algebra-quadratic-inequalities/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-inequalities'}, name='algebra_quadratic_inequalities'),

    # Алгебра > Теңдемелер: системасы - all 5 flat slots, none with a
    # real page yet.
    path('algebra-simultaneous-forming/', operation_placeholder_view, {'operation_slug': 'algebra-simultaneous-forming'}, name='algebra_simultaneous_forming'),
    path('algebra-simultaneous-substitution/', operation_placeholder_view, {'operation_slug': 'algebra-simultaneous-substitution'}, name='algebra_simultaneous_substitution'),
    path('algebra-simultaneous-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-simultaneous-mixed'}, name='algebra_simultaneous_mixed'),
    path('algebra-simultaneous-graphically/', operation_placeholder_view, {'operation_slug': 'algebra-simultaneous-graphically'}, name='algebra_simultaneous_graphically'),
    path('algebra-simultaneous-linear-non-linear/', operation_placeholder_view, {'operation_slug': 'algebra-simultaneous-linear-non-linear'}, name='algebra_simultaneous_linear_non_linear'),

    # Теңдемелер: сызыктуу > Кашаа менен - all 3 slots, none with a
    # real page yet.
    path('algebra-linear-brackets-without-coefficients/', operation_placeholder_view, {'operation_slug': 'algebra-linear-brackets-without-coefficients'}, name='algebra_linear_brackets_without_coefficients'),
    path('algebra-linear-brackets-with-coefficients/', operation_placeholder_view, {'operation_slug': 'algebra-linear-brackets-with-coefficients'}, name='algebra_linear_brackets_with_coefficients'),
    path('algebra-linear-brackets-multiple/', operation_placeholder_view, {'operation_slug': 'algebra-linear-brackets-multiple'}, name='algebra_linear_brackets_multiple'),

    # Теңдемелер: сызыктуу > Түзүү - all 3 slots, none with a real page
    # yet.
    path('algebra-linear-forming-shapes-angles-real-life/', operation_placeholder_view, {'operation_slug': 'algebra-linear-forming-shapes-angles-real-life'}, name='algebra_linear_forming_shapes_angles_real_life'),
    path('algebra-linear-forming-function-machines/', operation_placeholder_view, {'operation_slug': 'algebra-linear-forming-function-machines'}, name='algebra_linear_forming_function_machines'),
    path('algebra-linear-forming-functions-sequences/', operation_placeholder_view, {'operation_slug': 'algebra-linear-forming-functions-sequences'}, name='algebra_linear_forming_functions_sequences'),

    # Теңдемелер: сызыктуу > Белгисиз бир жагында: калькулятор менен -
    # all 4 slots, none with a real page yet.
    path('algebra-linear-var1side-calc-1step/', operation_placeholder_view, {'operation_slug': 'algebra-linear-var1side-calc-1step'}, name='algebra_linear_var1side_calc_1step'),
    path('algebra-linear-var1side-calc-2step/', operation_placeholder_view, {'operation_slug': 'algebra-linear-var1side-calc-2step'}, name='algebra_linear_var1side_calc_2step'),
    path('algebra-linear-var1side-calc-3step/', operation_placeholder_view, {'operation_slug': 'algebra-linear-var1side-calc-3step'}, name='algebra_linear_var1side_calc_3step'),
    path('algebra-linear-var1side-calc-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-linear-var1side-calc-mixed'}, name='algebra_linear_var1side_calc_mixed'),

    # Теңдемелер: сызыктуу > Белгисиз бир жагында: калькуляторсуз - all
    # 4 slots, none with a real page yet.
    path('algebra-linear-var1side-noncalc-1step/', algebra_linear_var1side_noncalc_1step_view, name='algebra_linear_var1side_noncalc_1step'),
    path('algebra-linear-var1side-noncalc-2step/', operation_placeholder_view, {'operation_slug': 'algebra-linear-var1side-noncalc-2step'}, name='algebra_linear_var1side_noncalc_2step'),
    path('algebra-linear-var1side-noncalc-3step/', operation_placeholder_view, {'operation_slug': 'algebra-linear-var1side-noncalc-3step'}, name='algebra_linear_var1side_noncalc_3step'),
    path('algebra-linear-var1side-noncalc-rational/', operation_placeholder_view, {'operation_slug': 'algebra-linear-var1side-noncalc-rational'}, name='algebra_linear_var1side_noncalc_rational'),

    # Теңдемелер: сызыктуу > Белгисиз эки жагында - all 4 slots, none
    # with a real page yet.
    path('algebra-linear-var-both-sides-without-brackets/', operation_placeholder_view, {'operation_slug': 'algebra-linear-var-both-sides-without-brackets'}, name='algebra_linear_var_both_sides_without_brackets'),
    path('algebra-linear-var-both-sides-with-brackets/', operation_placeholder_view, {'operation_slug': 'algebra-linear-var-both-sides-with-brackets'}, name='algebra_linear_var_both_sides_with_brackets'),
    path('algebra-linear-var-both-sides-graphical-intersections/', operation_placeholder_view, {'operation_slug': 'algebra-linear-var-both-sides-graphical-intersections'}, name='algebra_linear_var_both_sides_graphical_intersections'),
    path('algebra-linear-var-both-sides-parallel-lines/', operation_placeholder_view, {'operation_slug': 'algebra-linear-var-both-sides-parallel-lines'}, name='algebra_linear_var_both_sides_parallel_lines'),

    # Теңдемелер: квадраттык > Көбөйтүүчүлөргө ажыратуу: эки кашаа
    # менен - both slots, none with a real page yet.
    path('algebra-quadratic-factorisation-without-coefficients/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-factorisation-without-coefficients'}, name='algebra_quadratic_factorisation_without_coefficients'),
    path('algebra-quadratic-factorisation-with-coefficients/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-factorisation-with-coefficients'}, name='algebra_quadratic_factorisation_with_coefficients'),

    # Теңдемелер: квадраттык > b = 0 - all 3 slots, none with a real
    # page yet.
    path('algebra-quadratic-b-zero-rearranging/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-b-zero-rearranging'}, name='algebra_quadratic_b_zero_rearranging'),
    path('algebra-quadratic-b-zero-difference-of-squares/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-b-zero-difference-of-squares'}, name='algebra_quadratic_b_zero_difference_of_squares'),
    path('algebra-quadratic-b-zero-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-b-zero-mixed'}, name='algebra_quadratic_b_zero_mixed'),

    # Теңдемелер: квадраттык > Рационалдык - both slots, none with a
    # real page yet.
    path('algebra-quadratic-rational-without-coefficients/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-rational-without-coefficients'}, name='algebra_quadratic_rational_without_coefficients'),
    path('algebra-quadratic-rational-with-coefficients/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-rational-with-coefficients'}, name='algebra_quadratic_rational_with_coefficients'),

    # Теңдемелер: системасы > Жоюу ыкмасы - all 3 slots, none with a
    # real page yet.
    path('algebra-simultaneous-elimination-without-balancing/', operation_placeholder_view, {'operation_slug': 'algebra-simultaneous-elimination-without-balancing'}, name='algebra_simultaneous_elimination_without_balancing'),
    path('algebra-simultaneous-elimination-with-balancing/', operation_placeholder_view, {'operation_slug': 'algebra-simultaneous-elimination-with-balancing'}, name='algebra_simultaneous_elimination_with_balancing'),
    path('algebra-simultaneous-elimination-negative-only/', operation_placeholder_view, {'operation_slug': 'algebra-simultaneous-elimination-negative-only'}, name='algebra_simultaneous_elimination_negative_only'),

    # Теңдемелер: системасы > Сызыктуу жана сызыктуу эмес - both slots,
    # none with a real page yet.
    path('algebra-simultaneous-linear-non-linear-algebraically/', operation_placeholder_view, {'operation_slug': 'algebra-simultaneous-linear-non-linear-algebraically'}, name='algebra_simultaneous_linear_non_linear_algebraically'),
    path('algebra-simultaneous-linear-non-linear-graphically/', operation_placeholder_view, {'operation_slug': 'algebra-simultaneous-linear-non-linear-graphically'}, name='algebra_simultaneous_linear_non_linear_graphically'),
]
