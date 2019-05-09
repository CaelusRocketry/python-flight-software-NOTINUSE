package sensors

import (
	"flight-software/modules/sensors/bno055"

	"periph.io/x/periph/conn/i2c/i2creg"
	"periph.io/x/periph/host"
)

// Output vector types
const (
	VectorAccelerometer = 0x08
	VectorMagnetometer  = 0x0E
	VectorGyroscope     = 0x14
	VectorEuler         = 0x1A
	VectorLinearAcc     = 0x28
	VectorGravity       = 0x2E
)

type IMU struct {
	dev *bno055.Dev
}

func InitIMU() *IMU {
	if _, err := host.Init(); err != nil {
		panic(err)
	}

	b, err := i2creg.Open("") // Change to actual i2c port on RPi
	if err != nil {
		panic(err)
	}

	defer b.Close()

	dev, err := bno055.NewI2C(b, 0x28)

	// Reset the device
	err = dev.Reset()
	if err != nil {
		panic(err)
	}
	// Tell the device to use the external crystal oscillator
	err = dev.SetUseExternalCrystal(true)
	if err != nil {
		panic(err)
	}

	sensor := &IMU{dev: dev}

	return sensor
}

// Acc returns a vector with acceleration data
func (s *IMU) Acc() {
	v, err := s.Accelerometer()
	if err != nil {
		panic(err)
	}
	return v
}

// AccX returns acceleration data for x
func (s *IMU) AccX() float64 {
	v := s.Accelerometer()
	if err != nil {
		panic(err)
	}
	return v.X
}

// AccY returns acceleration data for x
func (s *IMU) AccY() float64 {
	v := s.Accelerometer()
	if err != nil {
		panic(err)
	}
	return v.Y
}

// AccZ returns acceleration data for x
func (s *IMU) AccZ() float64 {
	v := s.Accelerometer()
	if err != nil {
		panic(err)
	}
	return v.Z
}

// Gyro returns a vector with gyro data
func (s *IMU) Gyro() {
	v, err := s.Gyroscope()
	if err != nil {
		panic(err)
	}
	return v
}

// GyroX returns pitch
func (s *IMU) GyroX() float64 {
	v, err := s.Gyroscope()
	if err != nil {
		panic(err)
	}
	return v.X
}

// GyroY returns roll
func (s *IMU) GyroY() float64 {
	v, err := s.Gyroscope()
	if err != nil {
		panic(err)
	}
	return v.Y
}

// GyroZ returns yaw
func (s *IMU) GyroZ() float64 {
	v, err := s.Gyroscope()
	if err != nil {
		panic(err)
	}
	return v.Z
}
