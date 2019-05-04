package sensors

import (
	"github.com/kpeu3i/bno055"
)

func InitIMU() *bno055.Sensor {
	sensor, err := bno055.NewSensor(0x28, 1)
	if err != nil {
		panic(err)
	}

	err = sensor.UseExternalCrystal(true)
	if err != nil {
		panic(err)
	}

	axisConfig, err := sensor.AxisConfig()
	if err != nil {
		panic(err)
	}

	return sensor
}

// Acc returns a vector with acceleration data
func (s *bno055.Sensor) Acc() *bno055.Vector {
	v, err := s.Accelerometer()
	if err != nil {
		panic(err)
	}
	return v
}

// AccX returns acceleration data for x
func (s *bno055.Sensor) AccX() float64 {
	v := s.Accelerometer()
	if err != nil {
		panic(err)
	}
	return v.X
}

// AccY returns acceleration data for x
func (s *bno055.Sensor) AccY() float64 {
	v := s.Accelerometer()
	if err != nil {
		panic(err)
	}
	return v.Y
}

// AccZ returns acceleration data for x
func (s *bno055.Sensor) AccZ() float64 {
	v := s.Accelerometer()
	if err != nil {
		panic(err)
	}
	return v.Z
}

// Gyro returns a vector with gyro data
func (s *bno055.Sensor) Gyro() *bno055.Vector {
	v, err := s.Gyroscope()
	if err != nil {
		panic(err)
	}
	return v
}

// GyroX returns pitch
func (s *bno055.Sensor) GyroX() float64 {
	v, err := s.Gyroscope()
	if err != nil {
		panic(err)
	}
	return v.X
}

// GyroY returns roll
func (s *bno055.Sensor) GyroY() float64 {
	v, err := s.Gyroscope()
	if err != nil {
		panic(err)
	}
	return v.Y
}

// GyroZ returns yaw
func (s *bno055.Sensor) GyroZ() float64 {
	v, err := s.Gyroscope()
	if err != nil {
		panic(err)
	}
	return v.Z
}
