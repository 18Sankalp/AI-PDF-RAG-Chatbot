def add_message(history, role, content):

    history.append(
        {
            "role": role,
            "content": content
        }
    )


    return history



def get_history_text(history):

    conversation = ""


    for message in history:

        conversation += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )


    return conversation