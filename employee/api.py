
from employee import ma





class EmployeeData(ma.Schema):
    class Meta:
        fields = (
                    'id',
                    'firstName',
                    'lastName',
                    'address',
                    'email',
                    'phoneNumber',
                    'dob'
                 )


allEmployeeSchema = EmployeeData(many=True)
singleEmployeeSchema = EmployeeData()

