/*
Copyright (c) 2018 Forrest Sibley <My^Name^Without^The^Surname@ieee.org>

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

package max31856

import (
	//"sync"
	"errors"
	"fmt"
	"time"

	"github.com/mvpninjas/go-bitflag"
	"github.com/the-sibyl/sysfsGPIO"
)

type MAX31856 struct {
	dev               *spi.Device
	spidevPath        string
	spiClockSpeed     int64
	drdyTimeoutPeriod time.Duration
}

// Add functionality for DRDY pin
func Setup(spidevPath string, spiClockSpeed int64, drdyPin int, drdyTimeoutPeriod time.Duration) (MAX31856, error) {

	m := MAX31856{
		spidevPath:        spidevPath,
		spiClockSpeed:     spiClockSpeed,
		drdyTimeoutPeriod: drdyTimeoutPeriod,
	}

	o := spi.Devfs{
		Dev:      m.spidevPath,
		Mode:     spi.Mode1,
		MaxSpeed: m.spiClockSpeed,
	}

	// TOOD: implement closing for this

	dev, err := spi.Open(&o)

	if err != nil {
		return m, err
	}

	m.dev = dev

	var cr0 bitflag.Flag
	cr0.Set(CMODE)
	cr0.Set(OCFAULT0)
	cr0.Set(OCFAULT1)

	m.SetFlags(CR0_WR, cr0)

	// Get default values from the register
	mask, err := m.GetFlags(MASK_RD)
	if err != nil {
		return m, err
	}
	// Masks are active low. Unset the flags for the signals that need to be considered as faults.
	mask.Unset(OPEN)
	mask.Unset(OVUV)
	m.SetFlags(MASK_WR, mask)

	// TODO: Add DRDY interrupt code

	drdy, err := sysfsGPIO.InitPin(drdyPin, "in")
	if err != nil {
		return m, err
	}
	drdy.SetTriggerEdge("rising")
	drdy.AddPinInterrupt()

	// Do SOMETHING with the ISR........need to think this out!

	return m, nil
}

// TODO: Implement fault register polling. The board that I have has the FAULT pin hardwired to an LED. I need to be certain that waiting for data from the chip will not end in a deadlock. It might be prudent to add a timeout.

// Intended to be placed into a Goroutine
func (m *MAX31856) GetTempAuto() {
	// Todo: Implement an output channel for data and an input channel to exit or perform flow control

	// Step 1: Set up the chip for auto-capture
	// Step 2: Wait for DRDY interrupt
	// Step 3: Push new data onto the channel
	// Step 4: Unset the auto-capture
}

// Intended to be called once per measurement
func (m *MAX31856) GetTempOnce() (float32, error) {
	// Step 1: Request temperature
	temperature, err := m.getTemp()
	// Step 2: Wait for DRDY interrupt
	// Step 3: Get data off SPI bus
	// Step 4: Check for faults ?
	// Step 5: Return data
	return temperature, err
}

// Internal function to get temperature. Return a float32 containing the temperature in degrees centigrade.
func (m *MAX31856) getTemp() (float32, error) {

	readValue := make([]byte, 4)

	dataReady := make(chan bool, 1)

	// Wait for the DRDY bit to go high
	go func() {
		dataReady <- true
	}()

	// TODO: Add code to actually check for DRDY. It is bypassed here.
	select {
	case <-time.After(m.drdyTimeoutPeriod):
		return 0, errors.New("Timeout Error")
	case <-dataReady:
		fmt.Println("Data is ready")
	}

	m.dev.SetCSChange(false)

	// Read 0xC, 0xD, 0xE. The address auto-increments on the chip.
	m.dev.Tx([]byte{
		0xC, 0x0, 0x0, 0x0,
	}, readValue)

	// Discard the first byte, save the rest, and shift them to their proper positions. The data are in two's
	// complement, and the math here works out nicely.
	temp := int16(readValue[1])<<8 | int16(readValue[2])
	linearTempDegC := float32(temp) * 0.0625

	return linearTempDegC, nil
}

// Read from the Fault Status Register and return a simple binary result
func (m *MAX31856) CheckForFaults() (bool, error) {
	faultFlags, err := m.GetFlags(SR_RD)
	fault := faultFlags != 0
	return fault, err
}

// Reset the faults register
func (m *MAX31856) ResetFaults() error {
	// Read the CR0 register
	cr0, err := m.GetFlags(CR0_RD)
	if err != nil {
		return err
	}
	// Set the FAULTCLR bit in CR0
	cr0.Set(FAULTCLR)
	// Write back out to CR0
	err = m.SetFlags(CR0_WR, cr0)
	return err
}

// Write to a register using a bitflag.Flag type for convenience
func (m *MAX31856) SetFlags(address byte, value bitflag.Flag) error {
	if address < 0x80 || address > 0x8B {
		return errors.New("Invalid write address")
	}

	m.dev.SetCSChange(false)
	m.dev.Tx([]byte{address, byte(value)}, nil)

	fmt.Println([]byte{address, byte(value)})
	fmt.Println("Writing config")

	return nil
}

// Get register values and store them in a bitflag.Flag type for convenience
func (m *MAX31856) GetFlags(address byte) (bitflag.Flag, error) {
	if address >= 0x80 && address <= 0x8B {
		return 0, errors.New("Invalid read address")
	}

	readValue := make([]byte, 2)

	m.dev.SetCSChange(false)
	m.dev.Tx([]byte{address, byte(0)}, readValue)

	return bitflag.Flag(readValue[1]), nil
}
