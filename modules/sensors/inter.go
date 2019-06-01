package sensors

type Sensor interface {
	Name() string
	Correct() bool
	Safe() float32
	Warning() float32
	Critical() float32
	GetData() float64
	GetLevel() string
}
