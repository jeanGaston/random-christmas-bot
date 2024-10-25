from random import choice

def draw_names(current_participants, history_data, draws_per_person, max_attempts=5):
    """
    Perform the Secret Santa draw considering past years' draws.
    :param current_participants: This year's participant list.
    :param history_data: Historical draw data to avoid repeats.
    :param draws_per_person: Number of people each participant should give gifts to.
    :param max_attempts: Maximum number of retry attempts before loosening exclusions. by default : 5.
    :return: The new draw results.
    """
    participants = [p[0] for p in current_participants]  # Get participant names
    already_drawn = []  # Track who has been drawn
    new_draw = []  # Store new draw results

    for attempt in range(max_attempts):
        new_draw.clear()
        already_drawn.clear()
        success = True  # Track if draw is successful in this attempt

        for i, giver in enumerate(participants):
            email = current_participants[i][1]
            # Collect previous recipients to avoid drawing the same person again
            previous_recipients = {recipient for record in history_data if record[0] == giver for recipient in record[2:]}

            # Create a set of available participants excluding the giver and previous recipients
            available_participants = set(participants) - {giver} - previous_recipients
            new_recipients = []

            # Ensure there are enough available participants for the draw
            if len(available_participants) < draws_per_person:
                success = False
                break

            # Select recipients for the current giver
            while len(new_recipients) < draws_per_person:
                selected = choice(list(available_participants))
                if already_drawn.count(selected) < draws_per_person:
                    new_recipients.append(selected)
                    already_drawn.append(selected)
                    available_participants.discard(selected)

            new_draw.append([giver, email] + new_recipients)

        # If the draw was successful, break out of attempts
        if success:
            return new_draw
        print(f"Attempt {attempt + 1} failed, retrying...")

    # If all attempts fail, raise an error
    raise ValueError("Unable to complete a valid draw after maximum attempts.")
