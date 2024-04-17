class Depo:
    def __init__(self, id=0, x_coordinate=0, y_coordinate=0, demand=0, timeWindow_start=0, timeWindow_end=0, serviceTime=0):
        self.id = id
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.demand = demand
        self.timeWindow_start = timeWindow_start
        self.timeWindow_end = timeWindow_end
        self.serviceTime = serviceTime

    def __repr__(self):
        return f'Depo(id={self.id}, x_coordinate={self.x_coordinate}, y_coordinate={self.y_coordinate}, demand={self.demand}, timeWindow_start={self.timeWindow_start}, timeWindow_end={self.timeWindow_end}, serviceTime={self.serviceTime})'
