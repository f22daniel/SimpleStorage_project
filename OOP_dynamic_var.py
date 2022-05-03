
class Employee:

    num_of_emps = 0
    raise_amount = 1.06

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'

        Employee.num_of_emps += 1

    def get_values(self):
        return(f'{self.first} {self.last} | {self.pay} | {self.email}')

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)


i = 1

while True:
    _first = input('First: ')
    _last = input('Last: ')
    _pay = input('Pay: ')
    globals()[f'emp{i}'] = Employee(_first, _last, _pay )
    x = input('Press Q to end.')
    i = i + 1
    if x == 'Q':
        break

print('')
for n in range(i-1):
    print(Employee.get_values(globals()[f'emp{n+1}']))