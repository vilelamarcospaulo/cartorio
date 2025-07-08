from lib.words import find_line_index

def to_revision(lines):
    revision_index = find_line_index(lines, 'REVISÃO DATA DESCRIÇÃO AUTORA')
    if revision_index == -1:
        return

    last_revision_line = lines[revision_index + 1]
    return last_revision_line[0][4]

