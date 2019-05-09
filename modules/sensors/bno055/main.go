/*
The MIT License (MIT)

Copyright (c) 2015 Gaurav Hirlekar
Copyright (c) 2018 Brian Starkey

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
// Go port of https://github.com/ghirlekar/bno055-python-i2c

package bno055

import (
	"bytes"
	"encoding/binary"
	"errors"
	"fmt"
	"time"

	"periph.io/x/periph/conn"
	"periph.io/x/periph/conn/i2c"
)

const (
	BNO055_ADDRESS_A = 0x28
	BNO055_ADDRESS_B = 0x29
	BNO055_ID        = 0xA0

	// Power mode settings
	POWER_MODE_NORMAL   = 0x00
	POWER_MODE_LOWPOWER = 0x01
	POWER_MODE_SUSPEND  = 0x02

	// Operation mode settings
	OPERATION_MODE_CONFIG       = 0x00
	OPERATION_MODE_ACCONLY      = 0x01
	OPERATION_MODE_MAGONLY      = 0x02
	OPERATION_MODE_GYRONLY      = 0x03
	OPERATION_MODE_ACCMAG       = 0x04
	OPERATION_MODE_ACCGYRO      = 0x05
	OPERATION_MODE_MAGGYRO      = 0x06
	OPERATION_MODE_AMG          = 0x07
	OPERATION_MODE_IMUPLUS      = 0x08
	OPERATION_MODE_COMPASS      = 0x09
	OPERATION_MODE_M4G          = 0x0A
	OPERATION_MODE_NDOF_FMC_OFF = 0x0B
	OPERATION_MODE_NDOF         = 0x0C

	// Output vector type
	VECTOR_ACCELEROMETER = 0x08
	VECTOR_MAGNETOMETER  = 0x0E
	VECTOR_GYROSCOPE     = 0x14
	VECTOR_EULER         = 0x1A
	VECTOR_LINEARACCEL   = 0x28
	VECTOR_GRAVITY       = 0x2E

	// REGISTER DEFINITION START
	BNO055_PAGE_ID_ADDR = 0x07

	BNO055_CHIP_ID_ADDR       = 0x00
	BNO055_ACCEL_REV_ID_ADDR  = 0x01
	BNO055_MAG_REV_ID_ADDR    = 0x02
	BNO055_GYRO_REV_ID_ADDR   = 0x03
	BNO055_SW_REV_ID_LSB_ADDR = 0x04
	BNO055_SW_REV_ID_MSB_ADDR = 0x05
	BNO055_BL_REV_ID_ADDR     = 0x06

	// Accel data register
	BNO055_ACCEL_DATA_X_LSB_ADDR = 0x08
	BNO055_ACCEL_DATA_X_MSB_ADDR = 0x09
	BNO055_ACCEL_DATA_Y_LSB_ADDR = 0x0A
	BNO055_ACCEL_DATA_Y_MSB_ADDR = 0x0B
	BNO055_ACCEL_DATA_Z_LSB_ADDR = 0x0C
	BNO055_ACCEL_DATA_Z_MSB_ADDR = 0x0D

	// Mag data register
	BNO055_MAG_DATA_X_LSB_ADDR = 0x0E
	BNO055_MAG_DATA_X_MSB_ADDR = 0x0F
	BNO055_MAG_DATA_Y_LSB_ADDR = 0x10
	BNO055_MAG_DATA_Y_MSB_ADDR = 0x11
	BNO055_MAG_DATA_Z_LSB_ADDR = 0x12
	BNO055_MAG_DATA_Z_MSB_ADDR = 0x13

	// Gyro data registers
	BNO055_GYRO_DATA_X_LSB_ADDR = 0x14
	BNO055_GYRO_DATA_X_MSB_ADDR = 0x15
	BNO055_GYRO_DATA_Y_LSB_ADDR = 0x16
	BNO055_GYRO_DATA_Y_MSB_ADDR = 0x17
	BNO055_GYRO_DATA_Z_LSB_ADDR = 0x18
	BNO055_GYRO_DATA_Z_MSB_ADDR = 0x19

	// Euler data registers
	BNO055_EULER_H_LSB_ADDR = 0x1A
	BNO055_EULER_H_MSB_ADDR = 0x1B
	BNO055_EULER_R_LSB_ADDR = 0x1C
	BNO055_EULER_R_MSB_ADDR = 0x1D
	BNO055_EULER_P_LSB_ADDR = 0x1E
	BNO055_EULER_P_MSB_ADDR = 0x1F

	// Quaternion data registers
	BNO055_QUATERNION_DATA_W_LSB_ADDR = 0x20
	BNO055_QUATERNION_DATA_W_MSB_ADDR = 0x21
	BNO055_QUATERNION_DATA_X_LSB_ADDR = 0x22
	BNO055_QUATERNION_DATA_X_MSB_ADDR = 0x23
	BNO055_QUATERNION_DATA_Y_LSB_ADDR = 0x24
	BNO055_QUATERNION_DATA_Y_MSB_ADDR = 0x25
	BNO055_QUATERNION_DATA_Z_LSB_ADDR = 0x26
	BNO055_QUATERNION_DATA_Z_MSB_ADDR = 0x27

	// Linear acceleration data registers
	BNO055_LINEAR_ACCEL_DATA_X_LSB_ADDR = 0x28
	BNO055_LINEAR_ACCEL_DATA_X_MSB_ADDR = 0x29
	BNO055_LINEAR_ACCEL_DATA_Y_LSB_ADDR = 0x2A
	BNO055_LINEAR_ACCEL_DATA_Y_MSB_ADDR = 0x2B
	BNO055_LINEAR_ACCEL_DATA_Z_LSB_ADDR = 0x2C
	BNO055_LINEAR_ACCEL_DATA_Z_MSB_ADDR = 0x2D

	// Gravity data registers
	BNO055_GRAVITY_DATA_X_LSB_ADDR = 0x2E
	BNO055_GRAVITY_DATA_X_MSB_ADDR = 0x2F
	BNO055_GRAVITY_DATA_Y_LSB_ADDR = 0x30
	BNO055_GRAVITY_DATA_Y_MSB_ADDR = 0x31
	BNO055_GRAVITY_DATA_Z_LSB_ADDR = 0x32
	BNO055_GRAVITY_DATA_Z_MSB_ADDR = 0x33

	// Temperature data register
	BNO055_TEMP_ADDR = 0x34

	// Status registers
	BNO055_CALIB_STAT_ADDR      = 0x35
	BNO055_SELFTEST_RESULT_ADDR = 0x36
	BNO055_INTR_STAT_ADDR       = 0x37

	BNO055_SYS_CLK_STAT_ADDR = 0x38
	BNO055_SYS_STAT_ADDR     = 0x39
	BNO055_SYS_ERR_ADDR      = 0x3A

	// Unit selection register
	BNO055_UNIT_SEL_ADDR    = 0x3B
	BNO055_DATA_SELECT_ADDR = 0x3C

	// Mode registers
	BNO055_OPR_MODE_ADDR = 0x3D
	BNO055_PWR_MODE_ADDR = 0x3E

	BNO055_SYS_TRIGGER_ADDR = 0x3F
	BNO055_TEMP_SOURCE_ADDR = 0x40

	// Axis remap registers
	BNO055_AXIS_MAP_CONFIG_ADDR = 0x41
	BNO055_AXIS_MAP_SIGN_ADDR   = 0x42

	// SIC registers
	BNO055_SIC_MATRIX_0_LSB_ADDR = 0x43
	BNO055_SIC_MATRIX_0_MSB_ADDR = 0x44
	BNO055_SIC_MATRIX_1_LSB_ADDR = 0x45
	BNO055_SIC_MATRIX_1_MSB_ADDR = 0x46
	BNO055_SIC_MATRIX_2_LSB_ADDR = 0x47
	BNO055_SIC_MATRIX_2_MSB_ADDR = 0x48
	BNO055_SIC_MATRIX_3_LSB_ADDR = 0x49
	BNO055_SIC_MATRIX_3_MSB_ADDR = 0x4A
	BNO055_SIC_MATRIX_4_LSB_ADDR = 0x4B
	BNO055_SIC_MATRIX_4_MSB_ADDR = 0x4C
	BNO055_SIC_MATRIX_5_LSB_ADDR = 0x4D
	BNO055_SIC_MATRIX_5_MSB_ADDR = 0x4E
	BNO055_SIC_MATRIX_6_LSB_ADDR = 0x4F
	BNO055_SIC_MATRIX_6_MSB_ADDR = 0x50
	BNO055_SIC_MATRIX_7_LSB_ADDR = 0x51
	BNO055_SIC_MATRIX_7_MSB_ADDR = 0x52
	BNO055_SIC_MATRIX_8_LSB_ADDR = 0x53
	BNO055_SIC_MATRIX_8_MSB_ADDR = 0x54

	// Accelerometer Offset registers
	ACCEL_OFFSET_X_LSB_ADDR = 0x55
	ACCEL_OFFSET_X_MSB_ADDR = 0x56
	ACCEL_OFFSET_Y_LSB_ADDR = 0x57
	ACCEL_OFFSET_Y_MSB_ADDR = 0x58
	ACCEL_OFFSET_Z_LSB_ADDR = 0x59
	ACCEL_OFFSET_Z_MSB_ADDR = 0x5A

	// Magnetometer Offset registers
	MAG_OFFSET_X_LSB_ADDR = 0x5B
	MAG_OFFSET_X_MSB_ADDR = 0x5C
	MAG_OFFSET_Y_LSB_ADDR = 0x5D
	MAG_OFFSET_Y_MSB_ADDR = 0x5E
	MAG_OFFSET_Z_LSB_ADDR = 0x5F
	MAG_OFFSET_Z_MSB_ADDR = 0x60

	// Gyroscope Offset registers
	GYRO_OFFSET_X_LSB_ADDR = 0x61
	GYRO_OFFSET_X_MSB_ADDR = 0x62
	GYRO_OFFSET_Y_LSB_ADDR = 0x63
	GYRO_OFFSET_Y_MSB_ADDR = 0x64
	GYRO_OFFSET_Z_LSB_ADDR = 0x65
	GYRO_OFFSET_Z_MSB_ADDR = 0x66

	// Radius registers
	ACCEL_RADIUS_LSB_ADDR = 0x67
	ACCEL_RADIUS_MSB_ADDR = 0x68
	MAG_RADIUS_LSB_ADDR   = 0x69
	MAG_RADIUS_MSB_ADDR   = 0x6A
)

func NewI2C(b i2c.Bus, addr uint8) (*Dev, error) {
	switch addr {
	case 0x29, 0x28:
	default:
		return nil, errors.New("bno055: given address not supported by device")
	}
	d := &Dev{d: &i2c.Dev{Bus: b, Addr: uint16(addr)}, name: "BNO055"}

	id := []byte{0}
	err := d.readReg(BNO055_CHIP_ID_ADDR, id)
	if err != nil {
		return nil, err
	} else if id[0] != BNO055_ID {
		return nil, fmt.Errorf("bno055: Unexpected device ID %2x", id[0])
	}

	err = d.SetMode(OPERATION_MODE_CONFIG)
	if err != nil {
		return nil, err
	}

	err = d.Reset()
	if err != nil {
		return nil, err
	}

	err = d.writeReg(BNO055_PWR_MODE_ADDR, []byte{POWER_MODE_NORMAL})
	if err != nil {
		return nil, err
	}

	err = d.setPage(0)
	if err != nil {
		return nil, err
	}

	err = d.SetMode(OPERATION_MODE_NDOF)
	if err != nil {
		return nil, err
	}

	return d, nil
}

func (d *Dev) Ping() bool {
	id := []byte{0}
	err := d.readReg(BNO055_CHIP_ID_ADDR, id)
	if err != nil {
		return false
	}

	return id[0] == BNO055_ID
}

func (d *Dev) Dump(reg, num uint8) []byte {
	data := make([]byte, num)

	d.readReg(reg, data)

	return data
}

func (d *Dev) Reset() error {
	d.writeReg(BNO055_SYS_TRIGGER_ADDR, []byte{0x20})
	time.Sleep(1 * time.Second)
	for i := 0; i < 10; i++ {
		pong := d.Ping()
		if pong {
			return nil
		}
		time.Sleep(10 * time.Millisecond)
	}

	return fmt.Errorf("Reset failed")
}

func (d *Dev) setPage(page uint8) error {
	return d.writeReg(BNO055_PAGE_ID_ADDR, []byte{page})
}

func (d *Dev) SetMode(mode uint8) error {
	err := d.writeReg(BNO055_OPR_MODE_ADDR, []byte{mode})
	if err == nil {
		d.mode = mode
	}
	time.Sleep(30 * time.Millisecond)
	return err
}

func (d *Dev) SetUseExternalCrystal(external bool) error {
	prev := d.mode
	err := d.SetMode(OPERATION_MODE_CONFIG)
	if err != nil {
		return err
	}

	err = d.setPage(0)
	if err != nil {
		return err
	}

	if external {
		err = d.writeReg(BNO055_SYS_TRIGGER_ADDR, []byte{0x80})
	} else {
		err = d.writeReg(BNO055_SYS_TRIGGER_ADDR, []byte{0})
	}

	err2 := d.SetMode(prev)
	if err2 != nil {
		return err
	}

	return err
}

func (d *Dev) GetSystemStatus() (stat, syserr, selftest uint8, err error) {
	data := []byte{0, 0}

	err = d.setPage(0)
	if err != nil {
		return 0, 0, 0, err
	}

	err = d.readReg(BNO055_SYS_STAT_ADDR, data)
	if err != nil {
		return 0, 0, 0, err
	}
	stat = data[0]
	syserr = data[1]

	data = data[:1]
	err = d.readReg(BNO055_SELFTEST_RESULT_ADDR, data)
	if err != nil {
		return 0, 0, 0, err
	}
	selftest = data[0]

	return stat, syserr, selftest, nil
}

func (d *Dev) GetRevisionInfo() (accel, mag, gyro uint8, sw uint16, bl uint8, err error) {
	data := []byte{0, 0, 0}

	err = d.readReg(BNO055_ACCEL_REV_ID_ADDR, data)
	if err != nil {
		return 0, 0, 0, 0, 0, err
	}
	accel = data[0]
	mag = data[1]
	gyro = data[2]

	data = data[:2]
	err = d.readReg(BNO055_SW_REV_ID_LSB_ADDR, data)
	if err != nil {
		return 0, 0, 0, 0, 0, err
	}
	sw = uint16(data[0]) | uint16(data[1])<<8

	data = data[:1]
	err = d.readReg(BNO055_BL_REV_ID_ADDR, data)
	if err != nil {
		return 0, 0, 0, 0, 0, err
	}
	bl = data[0]

	return accel, mag, gyro, sw, bl, err
}

func (d *Dev) GetCalibration() (calib uint8, err error) {
	data := []byte{0}

	err = d.readReg(BNO055_CALIB_STAT_ADDR, data)

	return data[0], err
}

func (d *Dev) GetTemp() (temp uint8, err error) {
	data := []byte{0}

	err = d.readReg(BNO055_TEMP_ADDR, data)

	return data[0], err
}

func scaleVec(indata []int16, scale float64) []float64 {
	outdata := make([]float64, len(indata))
	for i, d := range indata {
		outdata[i] = float64(d) / scale
	}
	return outdata
}

func (d *Dev) GetVector(vectype uint8) ([]float64, error) {
	data := make([]byte, 6, 6)
	err := d.readReg(vectype, data)
	if err != nil {
		return nil, err
	}

	vec := make([]int16, 3, 3)
	buf := bytes.NewBuffer(data)
	binary.Read(buf, binary.LittleEndian, vec)

	switch vectype {
	case VECTOR_MAGNETOMETER:
		return scaleVec(vec, 16.0), nil
	case VECTOR_GYROSCOPE:
		return scaleVec(vec, 900.0), nil
	case VECTOR_EULER:
		return scaleVec(vec, 16.0), nil
	case VECTOR_GRAVITY:
		return scaleVec(vec, 100.0), nil
	default:
		return scaleVec(vec, 1.0), nil
	}
}

func (d *Dev) GetQuaternion() ([]float64, error) {
	data := make([]byte, 8, 8)
	err := d.readReg(BNO055_QUATERNION_DATA_W_LSB_ADDR, data)
	if err != nil {
		return nil, err
	}
	vec := make([]int16, 4, 4)
	buf := bytes.NewBuffer(data)
	binary.Read(buf, binary.LittleEndian, vec)

	return scaleVec(vec, float64(1.0/(1<<14))), nil
}

type Dev struct {
	d    conn.Conn
	name string
	mode uint8
}

func (d *Dev) String() string {
	return fmt.Sprintf("%s{%s}", d.name, d.d)
}

func (d *Dev) Halt() error {
	return d.SetMode(OPERATION_MODE_CONFIG)
}

func (d *Dev) readReg(reg uint8, data []byte) error {
	err := d.d.Tx([]byte{reg}, data)
	return err
}

func (d *Dev) writeReg(reg uint8, data []byte) error {
	write := make([]byte, 1, len(data)+1)
	write[0] = reg
	write = append(write, data...)

	return d.d.Tx(write, nil)
}

var _ conn.Resource = &Dev{}
