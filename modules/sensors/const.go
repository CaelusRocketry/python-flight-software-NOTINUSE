package sensors

// constants for the levels of danger when returning sensor checks
// Temperature sensors: 0) LOX Tube, 1) Fuel Tube, 2) LOX Pipe, 3) Fule Pipe, 4) Combustion chamber
// Pressure sensors: 0) LOX Tube, 1) Fuel Tube, 2) LOX Pipe, 3) Fule Pipe, 4) Combustion chamber
// IMU sensor: 0) IMU

var TempConsts []Levels
var PressureConsts []Levels
var IMUConsts []Levels

type Levels struct {
	SAFE     float64
	WARNING  float64
	CRITICAL float64
}

func setConstants(){
	TempConsts = append(TempConsts, Levels{SAFE: 1, WARNING: 2, CRITICAL: 3})
	TempConsts = append(TempConsts, Levels{SAFE: 1, WARNING: 2, CRITICAL: 3})
	TempConsts = append(TempConsts, Levels{SAFE: 1, WARNING: 2, CRITICAL: 3})
	TempConsts = append(TempConsts, Levels{SAFE: 1, WARNING: 2, CRITICAL: 3})
	TempConsts = append(TempConsts, Levels{SAFE: 1, WARNING: 2, CRITICAL: 3})
	
	PressureConsts = append(PressureConsts, Levels{SAFE: 1, WARNING: 2, CRITICAL: 3})
	PressureConsts = append(PressureConsts, Levels{SAFE: 1, WARNING: 2, CRITICAL: 3})
	PressureConsts = append(PressureConsts, Levels{SAFE: 1, WARNING: 2, CRITICAL: 3})
	PressureConsts = append(PressureConsts, Levels{SAFE: 1, WARNING: 2, CRITICAL: 3})
	PressureConsts = append(PressureConsts, Levels{SAFE: 1, WARNING: 2, CRITICAL: 3})
		
	IMUConsts = append(IMUConsts, Levels{SAFE: 1, WARNING: 2, CRITICAL: 3})
}