from collections import defaultdict

from .models import LEARNING_GOALS, Resource


def build_topic_sections(subtopic, subsubtopic=None):

    resources = (
        Resource.objects
        .select_related("topic", "subtopic", "subsubtopic")
        .filter(
            subtopic=subtopic,
            is_active=True,
            **(
                {"subsubtopic": subsubtopic}
                if subsubtopic is not None
                else {"subsubtopic__isnull": True}
            )
        )
    )

    grouped = defaultdict(list)

    for resource in resources:

        grouped[resource.learning_goal].append(
            {
                "title": resource.title,
                "subtitle": resource.description,
                "resource": resource,
                "fallback_image": "img/GraphIllustration.png",
            }
        )

    sections = []

    learning_goal_names = dict(
        LEARNING_GOALS
    )

    for goal, blocks in grouped.items():

        sections.append(
            {
                "header": learning_goal_names.get(
                    goal,
                    goal
                ),
                "blocks": blocks,
            }
        )

    return sections