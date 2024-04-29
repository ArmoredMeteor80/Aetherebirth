

def format_dialog(dialog_string: str, max_line_lenght: int=65):
    """Formats a dialog string to a string list
    Line breaks can be forced using \n in the dialog
    
    Parameters:
        dialog_string: str, complete dialog string
        max_line_lenght: int, maximum length of a line if no break is used
    """
    dialog = []
    for broken_line in dialog_string.split("\n"):
        line = ""
        for word in broken_line.split():
            if len(line + word) > max_line_lenght:
                dialog.append((line + word).strip())
                line = ""
            else:
                line += f"{word} "
        if len(line) > 0:
            dialog.append(line.strip())
    return dialog


if __name__ == "__main__":
    format_dialog_test_phrase = "J'aime les chips! Les chips de tomates sont les meilleurs, mais au cormoran ça peut passer.\nTu aimes les chips ?\nVraiment ? Trop cool !"
    print(format_dialog(format_dialog_test_phrase))
    assert format_dialog(format_dialog_test_phrase) == [
        "J'aime les chips! Les chips de tomates sont les meilleurs, mais au",
        'cormoran ça peut passer.',
        'Tu aimes les chips ?',
        'Vraiment ? Trop cool !'
    ], "format_dialog test failed: Incorrect output"
