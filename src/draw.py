from random import choice

def draw_names(previous_draw, draws_per_person):
    """
    Perform the Secret Santa draw considering past draws.
    :param previous_draw: Last year's draw data (list of participants and recipients).
    :param draws_per_person: Number of people each participant should give gifts to.
    :return: The new draw results.
    """
    participants = [a[0] for a in previous_draw]  # Get participant names
    already_drawn = []  # Track who has been drawn
    new_draw = []  # Store new draw results

    for i in range(len(participants)):
        last_year_r1 = previous_draw[i][2]
        last_year_r2 = previous_draw[i][3]
        giver = previous_draw[i][0]
        email = previous_draw[i][1]

        available_participants = participants.copy()
        try:
            available_participants.remove(giver)
            available_participants.remove(last_year_r1)
            available_participants.remove(last_year_r2)
        except ValueError:
            pass

        new_recipients = []
        while len(new_recipients) < draws_per_person:
            selected = choice(available_participants)
            if already_drawn.count(selected) >= draws_per_person:
                available_participants.remove(selected)
            else:
                new_recipients.append(selected)
                already_drawn.append(selected)
                available_participants.remove(selected)

        new_draw.append([giver, email] + new_recipients)

    return new_draw
