from lib.words import find_line_index, line_to_str
def to_stamp(lines):
    stamp_index = find_line_index(lines, 'PROJETO PRANCHA')
    if stamp_index == -1:
        return

    stamp_header = lines[stamp_index]
    # Get the X coordinate of the header

    header_x = stamp_header[0][0]
    # Small threshold for X coordinate comparison
    
    # Filter lines after header that match X coordinate
    stamp = []
    for line in lines[stamp_index:]:
        if line[0][0] == header_x:
            stamp.append(line)
    
    stamp = [line_to_str(x) for x in stamp]
    return _coerce_stamp(stamp)

def to_tag(stamp):
    [project, _, _, _, _] = stamp

    if 'SINALIZAÇÃO' in project:
        return 'SCV'

    return 'ARQ'

def _coerce_stamp(texts):
    t = texts[1].split(' ')
    r = t.pop()
    p = ' '.join(t)
        
    return [
        p, r,
        texts[3],
        texts[5],
        texts[7],
    ]

