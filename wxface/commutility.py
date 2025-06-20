# utility functions for communicator classes (Filter, Modifier)

def build_single(mode, logic, terms):
    if (mode == "") or (len(terms) < 1):
        return []
    running = [mode]
    if logic:
        running.append(logic)
    running.append(str(len(terms)))
    running.extend(terms)
    return running
