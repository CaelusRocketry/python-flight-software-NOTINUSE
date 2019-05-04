package sensors

import (
	"fmt"
	"os"

	"os/signal"
	"syscall"
	"time"

	"github.com/kpeu3i/bno055"
)

func initIMU() {
	sensor, err := bno055.NewSensor(0x28, 1)
	if err != nil {
		panic(err)
	}

	err = sensor.UseExternalCrystal(true)
	if err != nil {
		panic(err)
	}

	status, err := sensor.Status()
	if err != nil {
		panic(err)
	}

	fmt.Printf("* Status: system=%v, system_error=%v, self_test=%v\n", status.System, status.SystemError, status.SelfTest)

	revision, err := sensor.Revision()
	if err != nil {
		panic(err)
	}

	fmt.Printf(
		"* Revision: software=%v, bootloader=%v, accelerometer=%v, gyroscope=%v, magnetometer=%v\n",
		revision.Software,
		revision.Bootloader,
		revision.Accelerometer,
		revision.Gyroscope,
		revision.Magnetometer,
	)

	axisConfig, err := sensor.AxisConfig()
	if err != nil {
		panic(err)
	}

	fmt.Printf(
		"* Axis: x=%v, y=%v, z=%v, sign_x=%v, sign_y=%v, sign_z=%v\n",
		axisConfig.X,
		axisConfig.Y,
		axisConfig.Z,
		axisConfig.SignX,
		axisConfig.SignY,
		axisConfig.SignZ,
	)

	temperature, err := sensor.Temperature()
	if err != nil {
		panic(err)
	}

	fmt.Printf("* Temperature: t=%v\n", temperature)

	signals := make(chan os.Signal, 1)
	signal.Notify(signals, syscall.SIGINT, syscall.SIGTERM)

	for {
		select {
		case <-signals:
			err := sensor.Close()
			if err != nil {
				panic(err)
			}
		default:
			vector, err := sensor.Euler()
			if err != nil {
				panic(err)
			}

			fmt.Printf("\r*** Euler angles: x=%5.3f, y=%5.3f, z=%5.3f", vector.X, vector.Y, vector.Z)
		}

		time.Sleep(100 * time.Millisecond)
	}

	// Output:
	// * Status: system=133, system_error=0, self_test=15
	// * Revision: software=785, bootloader=21, accelerometer=251, gyroscope=15, magnetometer=50
	// * Axis: x=0, y=1, z=2, sign_x=0, sign_y=0, sign_z=0
	// * Temperature: t=27
	// * Euler angles: x=2.312, y=2.000, z=91.688
}

// Acc returns a vector with acceleration data
func (s *Sensor) IMU() Vector, Vector {
	accData, accErr := s.Accelerometer()
	if accErr != nil {
		panic(accErr)
	}
	
	gyroData, gyroErr := s.Accelerometer()
	if gyrocErr != nil {
		panic(gyrocErr)
	}

	return accData, gyrocErr

}

// Acc returns a vector with acceleration data
func (s *Sensor) Acc() Vector {
	v, err := s.Accelerometer()
	if err != nil {
		panic(err)
	}
	return v
}

// AccX returns acceleration data for x
func (s *Sensor) AccX() float64 {
	v := s.Accelerometer()
	if err != nil {
		panic(err)
	}
	return v.X
}

// AccY returns acceleration data for x
func (s *Sensor) AccY() float64 {
	v := s.Accelerometer()
	if err != nil {
		panic(err)
	}
	return v.Y
}

// AccZ returns acceleration data for x
func (s *Sensor) AccZ() float64 {
	v := s.Accelerometer()
	if err != nil {
		panic(err)
	}
	return v.Z
}

// Gyro returns a vector with gyro data
func (s *Sensor) Gyro() Vector {
	v, err := s.Gyroscope()
	if err != nil {
		panic(err)
	}
	return v
}

// GyroX returns pitch
func (s *Sensor) GyroX() float64 {
	v, err := s.Gyroscope()
	if err != nil {
		panic(err)
	}
	return v.X
}

// GyroY returns roll
func (s *Sensor) GyroY() float64 {
	v, err := s.Gyroscope()
	if err != nil {
		panic(err)
	}
	return v.Y
}

// GyroZ returns yaw
func (s *Sensor) GyroZ() float64 {
	v, err := s.Gyroscope()
	if err != nil {
		panic(err)
	}
	return v.Z
}
