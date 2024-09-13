import csv


class NoblePoint:
    def __init__(self, in_data):
        self.in_data = in_data
        self.general_columns = ['playerName', 'eventDay', 'eventType', 'ballType']
        self.criteria_points_attendance = {'present': 2, 'presentTamCancel': 1, 'unavailable': 0,
                                           'absentWithContact': -1, 'absentNoContact': -2}

    def nobility_criteria_reader(self):
        with open(self.in_data, newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                yield row

    def get_noble_point_attendance(self, criteria_nobility):
        noble_attendance = {}
        for field_name in criteria_nobility:
            if field_name in self.general_columns:
                noble_attendance[field_name] = criteria_nobility[field_name]
            elif field_name in self.criteria_points_attendance:
                if criteria_nobility[field_name] == 'Yes':
                    noble_attendance['npAttendance'] = self.criteria_points_attendance[field_name]
                else:
                    continue
        return noble_attendance

    def __get_noble_point_runs(self, value):
        noble_point_runs = 0
        if 0 < value <= 15:
            noble_point_runs = 0.5 + value * 0.05
        elif 16 < value <= 30:
            noble_point_runs = 1 + value * 0.05
        elif 31 < value <= 50:
            noble_point_runs = 1.5 + value * 0.05
        elif 51 < value <= 70:
            noble_point_runs = 2 + value * 0.05
        elif 71 < value <= 85:
            noble_point_runs = 2.5 + value * 0.05
        elif 86 < value <= 99:
            noble_point_runs = 3 + value * 0.05
        elif value >= 100:
            noble_point_runs = 3.5 + value * 0.05
        return noble_point_runs

    def __get_noble_point_wickets(self, value):
        return value * 0.9

    def __get_noble_point_catches(self, value):
        return value * 0.5

    def __get_empty_performance(self):
        return {
            'npTotalPerform': 0.0, 'runs': 0, 'npRuns': 0.0,
            'wickets': 0, 'npWickets': 0.0, 'catches': 0, 'npCatches': 0.0
        }

    def get_noble_point_performance(self, criteria_nobility):
        performance_functions = {
            'runs': self.__get_noble_point_runs,
            'wickets': self.__get_noble_point_wickets,
            'catches': self.__get_noble_point_catches
        }
        noble_performance = {'npTotalPerform': 0.0}
        for field_name in criteria_nobility:
            if field_name in performance_functions:
                if criteria_nobility[field_name] != 'None':
                    noble_performance[field_name] = criteria_nobility[field_name]
                    noble_performance[f'np{field_name.capitalize()}'] = performance_functions[field_name](
                        int(criteria_nobility[field_name])
                    )
                else:
                    continue
                noble_performance['npTotalPerform'] += noble_performance[f'np{field_name.capitalize()}']
        return noble_performance

    def get_noble_point_total(self, criteria_nobility):
        noble_points = {'npTotal': 0.0}
        for field_name in criteria_nobility:
            if criteria_nobility[field_name] == 'Training':
                noble_points.update(self.get_noble_point_attendance(criteria_nobility))
                noble_points.update(self.__get_empty_performance())
            elif criteria_nobility[field_name] == 'Match Practice':
                noble_points.update(self.get_noble_point_attendance(criteria_nobility))
                noble_points.update(self.get_noble_point_performance(criteria_nobility))
                noble_points['npTotal'] += noble_points['npTotalPerform']
            else:
                continue
        noble_points['npTotal'] += noble_points['npAttendance']
        return noble_points

    def write_noble_points(self, reader_obj):
        headers = ['playerName', 'eventDay', 'eventType', 'ballType',
                   'runs', 'npRuns', 'wickets', 'npWickets', 'catches', 'npCatches',
                   'npTotalPerform', 'npAttendance', 'npTotal']
        with open('test.csv', 'w', newline='') as csv_out:
            writer = csv.DictWriter(csv_out, fieldnames=headers)
            writer.writeheader()
            for row in reader_obj:
                writer.writerow(self.get_noble_point_total(row))


if __name__ == '__main__':
    np = NoblePoint(in_data='nobility-attendance-data-in-cricket.csv')
    nobility_reader = np.nobility_criteria_reader()
    np.write_noble_points(nobility_reader)
