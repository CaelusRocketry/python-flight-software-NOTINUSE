package sensors

type Sensor interface {
	Name() string
	Correct() bool
	Safe() float64
	Warning() float64
	Critical() float64
	GetData() float64
	GetLevel() string
}
