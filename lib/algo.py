def find_repeating(seq, brk=1000000):
    length = len(seq)
    max_run = 0
    run_pos = None
    for i1 in range(length):
        i2 = i1 + 1

        item1 = grid[i1]
        while i2 < length:
            item2 = grid[i2]
            if item1 == item2:
                break
            i2 += 1

        tmp = (i1, i2)
        run = 0
        while i1 < length and i2 < length:
            item1 = grid[i1]
            item2 = grid[i2]
#            print(i1, i2, item1, item2)
            if item1 != item2:
                break
            run += 1
            i1 += 1
            i2 += 1

        if run > max_run:
            max_run = run
            run_pos = tmp
#            print(y_run, max_run)

            # if we run off the end, that's fine, but after brk, stop
            # looking...
            if max_run > brk:
                break

    return run_pos, max_run
