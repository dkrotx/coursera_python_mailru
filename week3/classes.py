import csv
import sys
import os.path


class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[-1]

    def __repr__(self):
        ext = self.get_photo_file_ext()
        return f"brand: {self.brand}, photo_file_name={self.photo_file_name} ({ext}) carrying={self.carrying}"


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = "car"
        self.passenger_seats_count = int(passenger_seats_count)

    def __repr__(self):
        return "car: {0}, passenger_seats_count={1}".format(super().__repr__(), self.passenger_seats_count)


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = "truck"
        self.body_width, self.body_height, self.body_length = Truck.parse_body_volume(body_whl)

    def get_body_volume(self):
        return self.body_width * self.body_height * self.body_length

    @staticmethod
    def parse_body_volume(s):
        """ parse body volume expressed as WxHxL (floats) """
        if not s:
            return [0.0]*3

        res = list(map(float, s.split('x')))
        if len(res) != 3:
            raise ValueError(f"bad body-volume format: {s}")
        return res

    def __repr__(self):        
        return "truck: {0}, body_width={1} body_height={2} body_length={3} volume={4}".format(super().__repr__(), self.body_width, self.body_height, self.body_length, self.get_body_volume())


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = "spec_machine"
        self.extra = extra

    def __repr__(self):
        return 'spec_machine: {0}, extra="{1}"'.format(super().__repr__(), self.extra)


class CarsFactory:
    required_fields = ["brand", "photo_file_name", "carrying"]

    @staticmethod
    def from_dict(props):
        required = {fld: props[fld] for fld in CarsFactory.required_fields}
        
        try:
            t = props.get("car_type")
            if t == "car":
                return Car(**required, passenger_seats_count = props["passenger_seats_count"])
            elif t == "truck":
                return Truck(**required, body_whl = props["body_whl"])
            elif t == "spec_machine":
                return SpecMachine(**required, extra = props["extra"])
        except ValueError:
            pass

        return None


def get_car_list(csv_filename):
    cars = []
    with open(csv_filename) as fd:
        for rec in csv.DictReader(fd, delimiter=';'):
            car = CarsFactory.from_dict(rec)
            if car:
                cars.append(car)

    return cars


if __name__ == '__main__':
    print(get_car_list(sys.argv[1]))