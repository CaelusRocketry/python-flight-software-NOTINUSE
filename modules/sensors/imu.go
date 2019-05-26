package sensors

import (
	"flight-software/modules/sensors/bno055"

	"math"

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

	highCritGyro    = 15
	highWarningGryo = 10
	lowWarningGyro  = 5
	lowCritGyro     = 0

	tiltCritial		= 3

	highCritAcc    = 15
	highWarningAcc = 10
	lowWarningAcc  = 5
	lowCritAcc     = 0
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

	// defer b.Close()

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
func (s *IMU) Acc() []float64 {
	accVector, err := s.dev.GetVector(VectorLinearAcc)
	if err != nil {
		panic(err)
	}

	return accVector
}

// AccX returns acceleration data for x
func (s *IMU) AccX() float64 {
	accVector := s.Acc()
	return accVector[0]
}

// AccY returns acceleration data for y
func (s *IMU) AccY() float64 {
	accVector := s.Acc()
	return accVector[1]
}

// AccZ returns acceleration data for z
func (s *IMU) AccZ() float64 {
	accVector := s.Acc()
	return accVector[2]
}

// Gyro returns a vector with gyro data
func (s *IMU) Gyro() []float64 {
	gyroVector, err := s.dev.GetVector(VectorGyroscope)
	for i, _ := range gyroVector {
		gyroVector[i] = gyroVector[i] * 180 / math.Pi
	}
	if err != nil {
		panic(err)
	}

	return gyroVector
}

// GyroX returns pitch
func (s *IMU) GyroX() float64 {
	gyroVector := s.Gyro()
	return gyroVector[0]
}

// GyroY returns roll
func (s *IMU) GyroY() float64 {
	gyroVector := s.Gyro()
	return gyroVector[1]
}

// GyroZ returns yaw
func (s *IMU) GyroZ() float64 {
	gyroVector := s.Gyro()
	return gyroVector[2]
}

// CheckGyro checks both gyro
func (s *IMU) CheckGyro() (bool, integer64, []float64) {
	gyroVector := s.Gyro()
	for index, elem := range gyroVector {
		if highCritGyro > elem || lowCritGyro < elem {
			return false, CRITICAL, gyroVector
		}
		if highWarningGyro > elem || lowWarningGyro < elem {
			return false, WARNING, gyroVector
		}
	}
	return true, SAFE, gyroVector
}

// CheckGyro checks both gyro
func (s *IMU) CheckGyro() (bool, integer64, []float64) {
	gyroVector := s.Gyro()
	for index, elem := range gyroVector {
		if highCritGyro > math.abs(elem) {
			return false, CRITICAL, gyroVector
		}
		if highWarningGyro > math.abs(elem) {
			return false, WARNING, gyroVector
		}
	}
	return true, SAFE, gyroVector
}

// CheckAcc checks both acc
func (s *IMU) CheckAcc() (bool, integer64, []float64) {
	accVector := s.Acc()
	for index, elem := range accVector {
		if highCritAcc > elem || lowCritAcc < elem {
			return false, CRITICAL, accVector
		}
		if highWarningAcc > elem || lowWarningAcc < elem {
			return false, WARNING, accVector
		}
	}
	return true, SAFE, accVector
}

func (s *IMU) CalcTilt() (bool, integer64, []float64) {
	var tilt := make([][]float64, 11)
	for i := range tilt {
		tilt[index] = s.Gyro()
		time.Sleep(100 * time.Miliseconds)
	}

	var dtilt := make([]float64, 10)
	for i := range 9 {
		for j := range dtilt {
			dtilt[j] = dtilt[j] + (tilt[i+1][j] - tilt[i][j])
		}
	}

	for index, val :=  dtilt {
		dtilt[index] = val / 10.0
	}

	for index, val := dtilt {
		if(val > tiltCritial) {
			return false, CRITICAL, dtilt
		}
	}

	return true, SAFE, dtilt

}

