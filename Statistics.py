class Statistics():
    time_complexity = 0
    size_complexity = 0
    moves = 0
    start_time = None
    end_time = None
    delta = None

    @staticmethod
    def show_result(list_of_solution):
        i = 0

        for el in list_of_solution:
            if i == 0:
                i += 1
                print()
                continue
            print('Move N', i)
            print(el)
            print()
            i += 1

        print('Time:', Statistics.end_time - Statistics.start_time)
        print('Moves:', i - 1)
        print('Complexity in time:', Statistics.time_complexity)
        print('Complexity in size',  Statistics.size_complexity)


